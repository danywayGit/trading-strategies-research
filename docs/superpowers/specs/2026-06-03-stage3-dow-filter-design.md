# Stage 3 — DOW Filter Design Spec

**Date:** 2026-06-03
**Status:** Approved
**Scope:** 10 strategies · 2,314 Stage 2 passing combos · 8 DOW masks · entry masking

---

## 1. Objective

For each Stage 2 passing combo, test whether restricting entries to a specific day-of-week produces meaningfully better OOS Sharpe than trading every day. If yes, record that DOW mask as the winner for that combo. If no DOW mask improves on "ALL" by a sufficient margin, record "ALL" (no filter).

Results feed Stage 4, which collects the best combo+DOW per strategy for the final SUMMARY.md.

---

## 2. Input

All Stage 2 PASS JSONs across 10 strategies: `results/{STRATEGY}/stage2/{SYMBOL}_{TF}_{DIR}_{SL}.json`

No additional Sharpe filter applied — all 2,314 combos advance. Stage 2 already required OOS Sharpe > 0.

**Strategies:** SWING2, SWING3, SWING4, SWING5, EMA_REJ_V1, DC1, VR1, AGGR_PULLBACK, MO1, VP1

---

## 3. DOW Masks

8 masks applied to each combo:

| Mask | Days (Python weekday) | Description |
|---|---|---|
| ALL | None (no filter) | Baseline — entries on any day |
| MON-FRI | {0,1,2,3,4} | Weekdays only |
| SAT-SUN | {5,6} | Weekends only |
| MON | {0} | Monday only |
| TUE | {1} | Tuesday only |
| WED | {2} | Wednesday only |
| THU | {3} | Thursday only |
| FRI | {4} | Friday only |

**Masking approach:** Entry masking only. `long_entries` and `short_entries` are zeroed on bars whose day-of-week does not match the mask. Exit signals (`long_exits`, `short_exits`) and SL/TP remain active on all bars — positions opened on a matching day can close on any day. This reflects live trading behavior for 24/7 crypto futures.

---

## 4. Winner Selection Rule

```
candidates = [mask for mask in DOW_MASKS if dow_results[mask].num_trades >= 20]
best = max(candidates, key=lambda m: dow_results[m].oos_sharpe)

if best != "ALL" and dow_results[best].oos_sharpe > dow_results["ALL"].oos_sharpe + 0.10:
    winner = best
else:
    winner = "ALL"
```

- **Minimum trades:** 20 (per mask, in OOS period)
- **Minimum lift:** +0.10 absolute Sharpe above ALL
- If no candidate has ≥20 trades (extreme case), winner defaults to "ALL"

The +0.10 absolute threshold is preferred over a relative percentage because relative math breaks near zero Sharpe and produces inconsistent bars across the combo population.

---

## 5. Architecture — Approach A

10 per-strategy scripts sharing a `stage3_utils.py` module. Stage 3 scripts are significantly thinner than Stage 2 (~200 lines each vs ~600) because no optimization loop is needed — only evaluation.

### File structure

```
optimization/
├── wave2/                              # existing Stage 2 scripts
└── wave3/                              # NEW
    ├── stage3_utils.py
    ├── run_swing2_stage3_parallel_v2.py
    ├── run_swing3_stage3_parallel_v2.py
    ├── run_swing4_stage3_parallel_v2.py
    ├── run_swing5_stage3_parallel_v2.py
    ├── run_ema_rej_v1_stage3_parallel_v2.py
    ├── run_dc1_stage3_parallel_v2.py
    ├── run_vr1_stage3_parallel_v2.py
    ├── run_aggr_pullback_stage3_parallel_v2.py
    ├── run_mo1_stage3_parallel_v2.py
    ├── run_vp1_stage3_parallel_v2.py
    └── generate_stage3_summary.py

results/
├── {STRATEGY}/stage3/{SYMBOL}_{TF}_{DIR}_{SL}_dow.json
└── stage3_summarized/{STRATEGY}_stage3_summary.md
```

---

## 6. `stage3_utils.py` Contract

### Constants

```python
DOW_MASKS = {
    "ALL":     None,
    "MON-FRI": {0,1,2,3,4},
    "SAT-SUN": {5,6},
    "MON": {0}, "TUE": {1}, "WED": {2}, "THU": {3}, "FRI": {4},
}
MIN_TRADES = 20
MIN_LIFT   = 0.10
```

### `load_stage2_passing(strategy_id, results_base)`

Reads all `results/{STRATEGY}/stage2/*.json`, returns list of dicts for PASS results:
```python
{
    "symbol": "BTCUSDT",
    "timeframe": "4h",
    "direction": "both",
    "sl_type": "atr",
    "best_params": {...},
    "stage2_oos_sharpe": 0.87,
}
```

### `select_winner(dow_results)`

Takes `dow_results` dict `{mask_name: {"oos_sharpe": float|None, "num_trades": int}}`.
Returns `(winner_mask, winner_sharpe, winner_trades, dow_improved)`.

### `run_stage3_parallel(strategy_id, home_tf, results_base, symbols, worker_fn, backtesting_mcp, workers, skip_download)`

- Calls `load_stage2_passing` to build task list
- Each task: `{"sym": str, "tf": str, "direction": str, "sl_type": str, "best_params": dict, "stage2_oos_sharpe": float}`
- Skips tasks where output JSON already exists and has no error note (resume support)
- Dispatches via `ProcessPoolExecutor` with `BrokenExecutor` retry loop
- Writes JSON to `results/{STRATEGY}/stage3/`
- Prints progress per task

---

## 7. Per-Strategy Script Structure

### What is copied from the Stage 2 counterpart (verbatim)

- All indicator computation functions (numba JIT, signal helpers, etc.)
- `_eval_single` → adapted to `_eval_single_dow` (see below)
- `STRATEGY_ID`, `HOME_TF`, `RESULTS_BASE`, `TF_MAP`, `TF_FREQ_MAP`, `VENV_SITE_PACKAGES`
- `SYMBOLS`, `LIMITED_DATA`

### What is NOT copied

- `_optimize_vbt` — no param grid search in Stage 3
- `_build_sl_params_list` — not needed
- `_run_vbt_portfolio` — called directly inside `_eval_single_dow`
- `INDICATOR_PARAMS`, `SL_PARAM_GRID` — not needed (params come from Stage 2 JSON)

### `_eval_single_dow` signature

```python
def _eval_single_dow(data, direction, sl_type, best_params, dow_days, freq="1h"):
```

Identical to `_eval_single` except: after signals are generated and before vectorbt runs, entry signals are masked:

```python
if dow_days is not None:
    dow_bool = pd.Series(data.index).dt.dayofweek.isin(dow_days).values
    le = le & dow_bool
    se = se & dow_bool
# lx, sx, sl_stop, tp_stop unchanged
```

### `_worker_v2(task)` flow

```
task = {"sym", "tf", "direction", "sl_type", "best_params", "stage2_oos_sharpe"}

1. Load 3-year data at task["tf"]
2. Split 70/30, take OOS slice (test_data)
3. For each mask_name, days in DOW_MASKS:
       sharpe, trades = _eval_single_dow(test_data, ..., dow_days=days, freq=TF_FREQ_MAP[tf])
       dow_results[mask_name] = {"oos_sharpe": sharpe, "num_trades": trades}
4. winner_mask, winner_sharpe, winner_trades, dow_improved = select_winner(dow_results)
5. Return result dict
```

### `main()` delegates to `run_stage3_parallel`

```
python run_swing3_stage3_parallel_v2.py
python run_swing3_stage3_parallel_v2.py --workers 8
python run_swing3_stage3_parallel_v2.py --skip-download
```

---

## 8. JSON Output Format

**Path:** `results/{STRATEGY}/stage3/{SYMBOL}_{TF}_{DIR}_{SL}_dow.json`

```json
{
  "strategy": "swing3_supertrend_adx",
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "direction": "both",
  "sl_type": "atr",
  "stage": 3,
  "best_params": {"st_period": 10, "st_factor": 4.0, "...": "..."},
  "stage2_oos_sharpe": 0.87,
  "dow_results": {
    "ALL":     {"oos_sharpe": 0.87, "num_trades": 38},
    "MON-FRI": {"oos_sharpe": 1.12, "num_trades": 27},
    "SAT-SUN": {"oos_sharpe": 0.45, "num_trades": 11},
    "MON":     {"oos_sharpe": 0.95, "num_trades": 8},
    "TUE":     {"oos_sharpe": 1.05, "num_trades": 9},
    "WED":     {"oos_sharpe": 0.78, "num_trades": 7},
    "THU":     {"oos_sharpe": 1.31, "num_trades": 6},
    "FRI":     {"oos_sharpe": 0.92, "num_trades": 8}
  },
  "winner_mask": "MON-FRI",
  "winner_sharpe": 1.12,
  "winner_trades": 27,
  "dow_improved": true,
  "note": "v2/vectorbt"
}
```

`dow_improved: true` means a specific DOW mask beat ALL by ≥0.10 Sharpe with ≥20 trades.
`dow_improved: false` means ALL was kept as winner.

---

## 9. `generate_stage3_summary.py`

Usage: `python generate_stage3_summary.py <STRATEGY_ID | ALL>`

Reads all `*_dow.json` for a strategy, writes `results/stage3_summarized/{STRATEGY}_stage3_summary.md` containing:

1. **Header** — total combos, DOW improvement rate (% of combos where a DOW mask beat ALL)
2. **DOW mask distribution table** — how often each mask won across all combos
3. **Top combos table** — ranked by winner_sharpe: Symbol, TF, Direction, SL, Winner Mask, Winner Sharpe, Stage2 Sharpe, Trades, DOW Improved

---

## 10. What Comes Next (Stage 4)

Stage 4 reads the Stage 3 JSON files to collect the best combo+DOW per strategy and produces SUMMARY.md + parameter sensitivity. Out of scope for this spec.
