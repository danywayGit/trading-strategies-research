# SWING3 Stage 1 Optimization — vectorbt v2 Design Spec

**Date:** 2026-05-31
**Status:** Approved — ready for implementation
**Scope:** `run_swing3_stage1_parallel_v2.py` — drop-in replacement for the existing v1 script using vectorbt for the inner optimization loop

---

## 1. Problem

`run_swing3_stage1_parallel.py` (v1) takes multiple hours to complete SWING3 Stage 1 (39 symbols × 3 directions × 4 SL types = 468 tasks). The bottleneck is `engine.run_optimization()`, which calls `bt.optimize()` and runs 243–729 parameter combinations sequentially on CPU via backtesting.py's bar-by-bar simulation. The RTX 4090 is idle throughout.

The outer `ProcessPoolExecutor` (one process per task) already solves cross-task parallelism. The problem is the inner loop: each process still runs hundreds of sequential backtests.

---

## 2. Solution

Replace the inner `engine.run_optimization()` + `engine.run_walk_forward()` calls with a vectorbt-based optimizer that:

1. Groups the 243–729 parameter combos by their **indicator parameters** (81 unique combinations of `st_period × st_factor × adx_threshold × ema_filter`)
2. Computes indicators **once per group** instead of once per combo
3. Runs `vbt.Portfolio.from_signals()` with SL/TP variants **stacked as columns** — vectorbt evaluates 3–9 SL variants per call in vectorized numpy

**Expected speedup:** 40–80× per task (minutes → seconds). Full SWING3 Stage 1 with 14 workers: ~10–15 min vs ~3 hours.

---

## 3. File

**New file:** `optimization/wave1/run_swing3_stage1_parallel_v2.py`

The original `run_swing3_stage1_parallel.py` is untouched. Results written to the same `results/SWING3/stage1/` directory using the same filename convention. The `note` field in each JSON includes `"v2/vectorbt"` to mark the source.

---

## 4. Architecture

### 4.1 Outer Shell (unchanged from v1)

- Same `SYMBOLS`, `DIRECTIONS`, `SL_TYPES`, `GRIDS` constants
- Same pre-download step (`_predownload_all`) in the main process
- Same `ProcessPoolExecutor` with `max_workers = cpu_count - 2`
- Same skip-already-done logic (re-run errors, skip clean results)
- Same `_make_result()` helper and `NumpyEncoder`

### 4.2 Worker Function — `_worker_v2(task)`

```
Input:  (sym, direction, sl_type)
Output: result dict (same schema as v1)

Steps:
  1. Load OHLCV via engine.get_data()
  2. Split data: split_idx = int(len(data) * 0.7)
     train_data = data.iloc[:split_idx]
     test_data  = data.iloc[split_idx:]
  3. Run _optimize_vbt(train_data, direction, sl_type, GRIDS[sl_type])
     → returns (best_params, best_sharpe, best_num_trades, best_win_rate, best_max_dd)
  4. If best_num_trades < 30: return FAIL result
  5. Run _eval_single(test_data, direction, sl_type, best_params)
     → returns (oos_sharpe, oos_trades)
  6. verdict = "PASS" if oos_sharpe > 0 else "FAIL"
  7. Return result dict
```

### 4.3 Indicator Computation

**`_compute_supertrend(high, low, close, period, factor) → (direction, st_level)`**
- Computes ATR via `pd.Series.rolling(period).mean()` on True Range (matches TradingView default)
- Iterative Supertrend state machine compiled with `@numba.jit(nopython=True)` for the loop
- Returns two numpy arrays: `direction` (-1 bullish / +1 bearish) and `st_level`
- Called once per indicator combo — Numba JIT cache means first call compiles, subsequent calls are native speed

**`_compute_adx(high, low, close, period=14) → adx`**
- Wilder-smoothed DX via rolling mean on numpy — matches backtesting.py's `_calculate_adx`
- Pure numpy, no talib/ta dependency

**`_compute_ema(close, period) → ema`**
- `pd.Series(close).ewm(span=period, adjust=False).mean().values`

**`_compute_atr(high, low, close, period=14) → atr`**
- True range rolling mean (same formula as Supertrend ATR)

### 4.4 Signal Generation

**`_make_signals(st_dir, adx, ema, close, adx_threshold, direction)`**

```python
flip_bull = (st_dir[1:] == -1) & (st_dir[:-1] == 1)   # bearish→bullish
flip_bear = (st_dir[1:] ==  1) & (st_dir[:-1] == -1)  # bullish→bearish
adx_ok    = adx[1:] > adx_threshold
above_ema = close[1:] > ema[1:]
below_ema = close[1:] < ema[1:]

long_entries  = flip_bull & adx_ok & above_ema   (if direction in ['long','both'])
short_entries = flip_bear & adx_ok & below_ema   (if direction in ['short','both'])
long_exits    = flip_bear
short_exits   = flip_bull
```

Result arrays are prepended with one `False` to restore original length alignment.

### 4.5 vectorbt Portfolio Simulation per SL Type

For each of the 81 indicator combos, one `vbt.Portfolio.from_signals()` call covers all SL variants as array columns.

**`embedded`** — 3 combos per vbt call (atr_stop_mult sweep):
```python
# sl_stop expressed as fraction of close at each bar
sl_cols = np.column_stack([atr * m / close for m in [1.5, 2.5, 3.5]])
pf = vbt.Portfolio.from_signals(
    close, entries, exits,
    sl_stop=sl_cols,           # shape (n_bars, 3)
    freq='1h',
)
# pf has 3 columns → 3 Sharpe values
```

**`fixed_pct`** — 9 combos per vbt call (3 SL × 3 TP, no signal exit):
```python
# Explicitly enumerate all 9 (sl, tp) pairs — vectorbt 0.28.x does not auto-meshgrid
combos = list(product([0.015, 0.025, 0.035], [0.030, 0.060, 0.090]))  # 9 pairs
sl_arr = np.array([c[0] for c in combos])  # shape (9,) — scalar per column, same for all bars
tp_arr = np.array([c[1] for c in combos])

# entries/exits tiled to (n_bars, 9) so vectorbt sees one column per combo
entries_2d = np.tile(entries[:, None], (1, 9))
pf = vbt.Portfolio.from_signals(
    close, entries_2d, exits=None,
    sl_stop=sl_arr, tp_stop=tp_arr,
    freq='1h',
)
# pf has 9 columns → 9 Sharpe values
```

**`fixed_signal`** — 9 combos per vbt call (same as fixed_pct but signal exits remain):
```python
exits_2d = np.tile(exits[:, None], (1, 9))
pf = vbt.Portfolio.from_signals(
    close, entries_2d, exits_2d,   # ST flip exits active alongside SL/TP
    sl_stop=sl_arr, tp_stop=tp_arr,
    freq='1h',
)
```

**`atr`** — 9 combos per vbt call (3 atr_mult × 3 rr_ratio, stacked):
```python
combos = list(product([1.5, 2.5, 3.5], [1.5, 2.5, 3.5]))  # 9 pairs
sl_cols = np.column_stack([atr * m / close for m, _ in combos])
tp_cols = np.column_stack([atr * m * r / close for m, r in combos])
pf = vbt.Portfolio.from_signals(
    close, entries, exits=None,
    sl_stop=sl_cols,   # shape (n_bars, 9)
    tp_stop=tp_cols,   # shape (n_bars, 9)
    freq='1h',
)
```

**Short positions:** For `direction='both'`, vectorbt's `from_signals()` accepts `short_entries` and `short_exits` as separate parameters. The same 2D tiling approach applies. For `direction='long'` only `entries`/`exits` are passed; for `direction='short'` only `short_entries`/`short_exits` are passed with `entries=False`.

**ATR stop approximation:** `sl_stop = atr * mult / close` expresses the stop as a fraction of the *current bar's* close. vectorbt applies it as a fraction of the *entry bar's* close. These differ slightly bar-to-bar but the approximation is acceptable for Stage 1 screening.

Portfolio settings (all sl_types):
- `init_cash=1_000_000`
- `fees=0.0005` (0.05% taker, matching Binance Futures default)
- `freq='1h'`

### 4.6 Stats Extraction

After each `pf` call, extract per-column stats:
```python
stats = pf.stats()
sharpes    = stats['Sharpe Ratio']        # Series, one value per column
n_trades   = stats['Total Trades']
win_rates  = stats['Win Rate [%]']
max_dds    = stats['Max. Drawdown [%]']
```

Find the column with the highest Sharpe (using `idxmax()`). Map column index back to param combo to reconstruct `best_params` dict.

### 4.7 Walk-Forward (OOS Evaluation)

After finding `best_params` on `train_data`, re-run the same indicator computation and single portfolio simulation on `test_data`:

```python
def _eval_single(data, direction, sl_type, best_params):
    st_dir, adx, ema, atr = compute_indicators(data, best_params)
    entries, exits = make_signals(st_dir, adx, ema, data.Close, best_params, direction)
    pf = vbt.Portfolio.from_signals(close, entries, exits, sl_stop=..., ...)
    return pf.stats()['Sharpe Ratio'], pf.stats()['Total Trades']
```

This is a single vectorbt call on the 30% test window — negligible cost.

---

## 5. Parameter Grid (unchanged from v1)

```python
GRIDS = {
    "embedded":     {st_period, st_factor, adx_threshold, ema_filter, atr_stop_mult},
    "fixed_pct":    {st_period, st_factor, adx_threshold, ema_filter, stop_loss_pct, take_profit_pct},
    "fixed_signal": {st_period, st_factor, adx_threshold, ema_filter, stop_loss_pct, take_profit_pct},
    "atr":          {st_period, st_factor, adx_threshold, ema_filter, atr_stop_mult, rr_ratio},
}
```

Identical values to v1. The indicator-param grouping splits each grid into 81 indicator combos × 3–9 SL combos.

---

## 6. Output Format (unchanged from v1)

```json
{
  "strategy":          "swing3_supertrend_adx",
  "symbol":            "BTCUSDT",
  "timeframe":         "1h",
  "direction":         "both",
  "sl_type":           "embedded",
  "stage":             1,
  "test_window":       "2022-01-01/2024-12-31",
  "best_params":       {"st_period": 10, "st_factor": 3.0, ...},
  "train_sharpe":      1.23,
  "oos_sharpe":        0.87,
  "num_trades":        84,
  "win_rate_pct":      52.4,
  "max_drawdown_pct": -18.2,
  "verdict":           "PASS",
  "note":              "v2/vectorbt"
}
```

Filenames identical to v1: `{SYMBOL}_1h_{direction}_{sl_type}.json`. The v2 script will **not overwrite** existing v1 results unless they contain an error note — same skip logic as v1.

---

## 7. Dependencies

All already installed in BacktestingMCP venv:
- `vectorbt==0.28.1`
- `numba==0.56.4`
- `cupy==13.6.0` (available but not required for correctness — vectorbt uses numpy by default)
- `numpy`, `pandas` (already present)

No new packages needed.

---

## 8. Expected Performance

| Phase | v1 (backtesting.py) | v2 (vectorbt) |
|---|---|---|
| Per combo | ~0.4s (bar-by-bar) | ~0.005s (vectorized) |
| Per task (e.g. `embedded`) | ~97s (243 × 0.4s) | ~2–3s (81 vbt calls × ~0.03s) |
| Per task (e.g. `fixed_pct`) | ~292s (729 × 0.4s) | ~4–6s |
| Full stage1 (468 tasks, 14 workers) | ~2.5–3h | ~10–15 min |

---

## 9. Out of Scope

- Modifying BacktestingMCP's engine or strategy classes
- GPU/CuPy acceleration (pure numpy vectorbt is already sufficient)
- Porting other strategies (SWING4, SWING5, etc.) — v2 establishes the pattern; those scripts are separate work
- Stage 2, 3, 4 pipelines
