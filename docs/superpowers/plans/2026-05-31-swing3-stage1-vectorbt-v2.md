# SWING3 Stage 1 vectorbt v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `optimization/wave1/run_swing3_stage1_parallel_v2.py` — a drop-in replacement for the v1 script that uses vectorbt's vectorized portfolio simulation instead of backtesting.py's sequential bar-by-bar optimizer, targeting a 40–80× speedup.

**Architecture:** The outer process-pool structure is copied unchanged from v1. The inner `_worker()` function is replaced with `_worker_v2()` that: (1) computes indicators once per 81 unique indicator-param combos, (2) calls `vbt.Portfolio.from_signals()` with SL/TP variants stacked as 2D column arrays so vectorbt evaluates them all in one vectorized call, (3) runs a manual 70/30 walk-forward split to produce OOS Sharpe. Output JSON schema is identical to v1.

**Tech Stack:** Python 3.x, vectorbt 0.28.1, numba 0.56.4, numpy, pandas, BacktestingMCP engine (data loading only)

**Spec:** `docs/superpowers/specs/2026-05-31-swing3-stage1-vectorbt-v2-design.md`

---

## File Map

| File | Action | Purpose |
|---|---|---|
| `optimization/wave1/run_swing3_stage1_parallel_v2.py` | **Create** | The new v2 script — all implementation lives here |
| `optimization/wave1/run_swing3_stage1_parallel.py` | Read-only reference | Copy constants, outer shell, `_make_result`, `NumpyEncoder` |
| `results/SWING3/stage1/` | Shared output dir | Same JSON files as v1, `note` field contains `"v2/vectorbt"` |

---

## Task 1: Scaffold the v2 script — outer shell only

**Files:**
- Create: `optimization/wave1/run_swing3_stage1_parallel_v2.py`

- [ ] **Step 1: Create the file with imports and constants**

Copy the header block from `run_swing3_stage1_parallel.py` verbatim (lines 1–90), then replace the `GRIDS` dict `sl_mode` keys with a comment. The only constant that changes is adding `V2_NOTE = "v2/vectorbt"`.

```python
#!/usr/bin/env python3
"""
SWING3 Stage 1 optimization — vectorbt v2 (PARALLEL).

Replaces bt.optimize() with vbt.Portfolio.from_signals(), computing
indicators once per 81 unique indicator-param combos and evaluating
SL variants as vectorized columns.

Usage:
    python run_swing3_stage1_parallel_v2.py              # auto-detect workers
    python run_swing3_stage1_parallel_v2.py --workers 8
    python run_swing3_stage1_parallel_v2.py --skip-download
"""
import json
import sys
import os
import numpy as np
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed, BrokenExecutor

import numba
import vectorbt as vbt

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage1")
V2_NOTE = "v2/vectorbt"

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO"
]
LIMITED_DATA = {"ENA", "TAO"}

DIRECTIONS = ["both", "long", "short"]
SL_TYPES   = ["embedded", "fixed_pct", "fixed_signal", "atr"]

# Indicator params — same values as v1, controls the 81-combo outer loop
INDICATOR_PARAMS = {
    "st_period":     [7, 10, 14],
    "st_factor":     [2.0, 3.0, 4.0],
    "adx_threshold": [20, 25, 30],
    "ema_filter":    [50, 100, 200],
}

# SL-only params per sl_type (inner dimension swept per vbt call)
SL_PARAMS = {
    "embedded":     {"atr_stop_mult":   [1.5, 2.5, 3.5]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.5, 3.5],
                     "take_profit_pct": [3.0, 6.0, 9.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.5, 3.5],
                     "take_profit_pct": [3.0, 6.0, 9.0]},
    "atr":          {"atr_stop_mult":   [1.5, 2.5, 3.5],
                     "rr_ratio":        [1.5, 2.5, 3.5]},
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray):  return obj.tolist()
        return super().default(obj)


def _make_result(symbol, direction, sl_type, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy":         "swing3_supertrend_adx",
        "symbol":           symbol,
        "timeframe":        "1h",
        "direction":        direction,
        "sl_type":          sl_type,
        "stage":            1,
        "test_window":      "2022-01-01/2024-12-31",
        "best_params":      best_params,
        "train_sharpe":     round(train_sharpe, 4) if train_sharpe is not None else None,
        "oos_sharpe":       round(oos_sharpe, 4)   if oos_sharpe  is not None else None,
        "num_trades":       num_trades,
        "win_rate_pct":     round(win_rate, 2)     if win_rate    is not None else None,
        "max_drawdown_pct": round(max_dd, 2)       if max_dd      is not None else None,
        "verdict":          verdict,
        "note":             note,
    }
```

- [ ] **Step 2: Add the `_worker_v2` stub and `main()` function**

```python
def _worker_v2(task):
    """Placeholder — replaced in Task 7."""
    sym, direction, sl_type = task
    symbol_usdt = sym + "USDT"
    raise NotImplementedError(f"_worker_v2 not yet implemented for {symbol_usdt}")


def _predownload_all(symbols):
    import sys
    sys.path.insert(0, str(VENV_SITE_PACKAGES))
    sys.path.insert(0, str(BACKTESTING_MCP))
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame
    start, end = datetime(2022, 1, 1), datetime(2024, 12, 31)
    print(f"Pre-downloading {len(symbols)} symbols (1H)...")
    for sym in symbols:
        symbol_usdt = sym + "USDT"
        try:
            data = engine.get_data(symbol_usdt, TimeFrame.H1, start, end)
            print(f"  {symbol_usdt}: {len(data)} bars")
        except Exception as e:
            print(f"  {symbol_usdt}: ERROR — {e}")
    print()


def main():
    parser = argparse.ArgumentParser(description="SWING3 Stage 1 v2 parallel optimization")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if not args.skip_download:
        _predownload_all(SYMBOLS)

    all_tasks, skipped = [], 0
    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fname = f"{symbol_usdt}_1h_{direction}_{sl_type}.json"
                fpath = RESULTS_DIR / fname
                if fpath.exists():
                    try:
                        data = json.loads(fpath.read_text())
                        note = str(data.get("note", ""))
                        if "WORKER CRASH" in note or "OPT ERROR" in note:
                            all_tasks.append((sym, direction, sl_type))
                            continue
                    except Exception:
                        pass
                    skipped += 1
                else:
                    all_tasks.append((sym, direction, sl_type))

    total = len(SYMBOLS) * len(DIRECTIONS) * len(SL_TYPES)
    print(f"SWING3 Stage 1 v2 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do.")
        return

    done = skipped
    passed = 0

    remaining = list(all_tasks)
    while remaining:
        batch = remaining[:]
        remaining = []
        try:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(_worker_v2, task): task for task in batch}
                for future in as_completed(futures):
                    task = futures[future]
                    sym, direction, sl_type = task
                    symbol_usdt = sym + "USDT"
                    fname = f"{symbol_usdt}_1h_{direction}_{sl_type}.json"
                    fpath = RESULTS_DIR / fname
                    try:
                        result = future.result()
                    except BrokenExecutor:
                        for t, fut in futures.items():
                            if not fut.done():
                                remaining.append(futures[fut])
                        break
                    except Exception as e:
                        print(f"WORKER CRASH [{symbol_usdt} {direction} {sl_type}]: {e}")
                        result = _make_result(symbol_usdt, direction, sl_type,
                                              note=f"WORKER CRASH: {e}")
                    with open(fpath, "w") as f:
                        json.dump(result, f, indent=2, cls=NumpyEncoder)
                    done += 1
                    if result.get("verdict") == "PASS":
                        passed += 1
                    print(f"[{done}/{total}] {result['verdict']} | {fname}")
        except BrokenExecutor:
            print("Pool broken, restarting...")

    print(f"\n{'='*60}")
    print(f"DONE: {done}/{total} combos. Passed: {passed}")


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
```

- [ ] **Step 3: Verify the scaffold loads and prints the task list**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe ..\trading-strategies-research\optimization\wave1\run_swing3_stage1_parallel_v2.py --skip-download --workers 1 2>&1 | head -5
```

Expected output: script prints task count and then crashes on `NotImplementedError` (that's fine at this stage).

- [ ] **Step 4: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: scaffold SWING3 stage1 vectorbt v2 script (outer shell only)"
```

---

## Task 2: Implement indicator helper functions

**Files:**
- Modify: `optimization/wave1/run_swing3_stage1_parallel_v2.py` — add after imports, before `_worker_v2`

These functions must be defined at module level (not inside a function) so numba can compile them.

- [ ] **Step 1: Add the numba-compiled Supertrend inner loop**

Insert this block after the `VENV_SITE_PACKAGES` line and before `NumpyEncoder`:

```python
# ── Indicator helpers ────────────────────────────────────────────────────────

@numba.njit(cache=True)
def _supertrend_loop(close, upper_band, lower_band):
    """Iterative Supertrend state machine — compiled to native code by numba."""
    n = len(close)
    direction = np.empty(n, dtype=np.float64)
    st_level  = np.empty(n, dtype=np.float64)
    direction[:] = np.nan
    st_level[:] = np.nan

    # Find the first bar where bands are valid
    start = 0
    for i in range(n):
        if not np.isnan(upper_band[i]) and not np.isnan(lower_band[i]):
            start = i
            break

    direction[start] = -1.0          # start bullish
    st_level[start]  = lower_band[start]

    for i in range(start + 1, n):
        ub = upper_band[i]
        lb = lower_band[i]
        c  = close[i]
        if np.isnan(ub) or np.isnan(lb):
            direction[i] = direction[i - 1]
            st_level[i]  = st_level[i - 1]
            continue
        prev_dir   = direction[i - 1]
        prev_level = st_level[i - 1]
        if prev_dir == -1.0:          # currently bullish
            curr_lb = max(lb, prev_level)
            if c < curr_lb:
                direction[i] = 1.0    # flip bearish
                st_level[i]  = ub
            else:
                direction[i] = -1.0
                st_level[i]  = curr_lb
        else:                          # currently bearish
            curr_ub = min(ub, prev_level)
            if c > curr_ub:
                direction[i] = -1.0   # flip bullish
                st_level[i]  = lb
            else:
                direction[i] = 1.0
                st_level[i]  = curr_ub

    return direction, st_level


def _compute_supertrend(high, low, close, period, factor):
    """
    Returns (direction, st_level, atr) as float64 numpy arrays.
    direction: -1 = bullish, +1 = bearish (matches backtesting.py SWING3 convention).
    atr: simple rolling mean of True Range, same formula as _calculate_supertrend in SWING3.
    """
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    hl2 = (h + l) / 2.0
    tr  = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(period).mean().values

    upper = (hl2 + factor * pd.Series(atr)).values
    lower = (hl2 - factor * pd.Series(atr)).values

    direction, st_level = _supertrend_loop(
        close.astype(np.float64),
        upper.astype(np.float64),
        lower.astype(np.float64),
    )
    return direction, st_level, atr


def _compute_adx(high, low, close, period=14):
    """
    Wilder-smoothed ADX approximation using pandas ewm (alpha=1/period).
    Close enough for Stage 1 screening — exact Wilder initialization differs
    only in the first ~100 bars of a 26,000-bar dataset.
    Returns float64 numpy array same length as input.
    """
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    up   = h.diff()
    down = -l.diff()
    pdm  = np.where((up > down) & (up > 0), up, 0.0)
    mdm  = np.where((down > up) & (down > 0), down, 0.0)
    tr   = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    alpha = 1.0 / period
    tr_s  = tr.ewm(alpha=alpha, adjust=False).mean() * period
    pdm_s = pd.Series(pdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    mdm_s = pd.Series(mdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    with np.errstate(divide='ignore', invalid='ignore'):
        pdi = 100.0 * pdm_s / tr_s
        mdi = 100.0 * mdm_s / tr_s
        dx  = 100.0 * (pdi - mdi).abs() / (pdi + mdi)
    dx = dx.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    adx = dx.ewm(alpha=alpha, adjust=False).mean()
    return adx.fillna(0.0).values.astype(np.float64)


def _compute_ema(close, period):
    """Standard EWM EMA. Returns float64 numpy array."""
    return pd.Series(close).ewm(span=period, adjust=False).mean().values.astype(np.float64)
```

- [ ] **Step 2: Validate indicator outputs against the SWING3 strategy class**

Run this one-off script to compare v2 indicator output against what the existing SWING3 backtesting.py strategy computes on the same data:

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys
sys.path.insert(0, r'venv\Lib\site-packages')
sys.path.insert(0, '.')
import numpy as np
import pandas as pd
from datetime import datetime
from src.core.backtesting_engine import engine
from config.settings import TimeFrame
from src.strategies.swing3_supertrend_adx import _calculate_supertrend, _calculate_adx, calculate_ema

# Load data
data = engine.get_data('BTCUSDT', TimeFrame.H1, datetime(2022,1,1), datetime(2022,3,1))
h, l, c = data.High.values, data.Low.values, data.Close.values

# v1 results
v1_dir, v1_level = _calculate_supertrend(pd.Series(h), pd.Series(l), pd.Series(c), period=10, factor=3.0)
v1_adx = _calculate_adx(pd.Series(h), pd.Series(l), pd.Series(c), period=14)

# v2 results (import from v2 script)
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import _compute_supertrend, _compute_adx

v2_dir, v2_level, v2_atr = _compute_supertrend(h, l, c, period=10, factor=3.0)
v2_adx = _compute_adx(h, l, c, period=14)

# Compare last 100 bars (past warmup period)
corr_dir   = np.corrcoef(np.nan_to_num(v1_dir.values[-100:]),   np.nan_to_num(v2_dir[-100:]))[0,1]
corr_adx   = np.corrcoef(np.nan_to_num(v1_adx.values[-100:]),   np.nan_to_num(v2_adx[-100:]))[0,1]
print(f'Supertrend direction correlation: {corr_dir:.6f}  (expect > 0.999)')
print(f'ADX correlation:                  {corr_adx:.6f}  (expect > 0.99)')
"
```

Expected output: both correlations above 0.999 for Supertrend direction, > 0.99 for ADX.
If ADX correlation is lower (0.95+), that's acceptable — Wilder init differs only in early bars.

- [ ] **Step 3: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: add numba Supertrend + ADX/EMA indicator helpers for v2"
```

---

## Task 3: Implement signal generation

**Files:**
- Modify: `optimization/wave1/run_swing3_stage1_parallel_v2.py` — add after indicator helpers

- [ ] **Step 1: Add `_make_signals`**

```python
def _make_signals(st_dir, adx, ema, close, adx_threshold, direction):
    """
    Generate boolean entry/exit arrays for vectorbt.
    Returns (long_entries, long_exits, short_entries, short_exits) — all shape (n,).
    Index 0 is always False (no previous bar for flip detection).

    Supertrend convention (matches SWING3 strategy):
      direction == -1  →  bullish (price above Supertrend)
      direction == +1  →  bearish (price below Supertrend)
    """
    n = len(close)
    long_entries  = np.zeros(n, dtype=bool)
    long_exits    = np.zeros(n, dtype=bool)
    short_entries = np.zeros(n, dtype=bool)
    short_exits   = np.zeros(n, dtype=bool)

    prev = st_dir[:-1]
    curr = st_dir[1:]
    valid = ~(np.isnan(prev) | np.isnan(curr))

    flip_bull = valid & (curr == -1.0) & (prev ==  1.0)   # bearish → bullish
    flip_bear = valid & (curr ==  1.0) & (prev == -1.0)   # bullish → bearish

    adx_ok    = adx[1:]    > adx_threshold
    above_ema = close[1:]  > ema[1:]
    below_ema = close[1:]  < ema[1:]

    if direction in ("long", "both"):
        long_entries[1:]  = flip_bull & adx_ok & above_ema
        long_exits[1:]    = flip_bear

    if direction in ("short", "both"):
        short_entries[1:] = flip_bear & adx_ok & below_ema
        short_exits[1:]   = flip_bull

    return long_entries, long_exits, short_entries, short_exits
```

- [ ] **Step 2: Quick sanity check — count signals on BTCUSDT 2022**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys; sys.path.insert(0, r'venv\Lib\site-packages'); sys.path.insert(0, '.')
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import _compute_supertrend, _compute_adx, _compute_ema, _make_signals
from src.core.backtesting_engine import engine
from config.settings import TimeFrame
from datetime import datetime
import numpy as np

data = engine.get_data('BTCUSDT', TimeFrame.H1, datetime(2022,1,1), datetime(2022,12,31))
h, l, c = data.High.values, data.Low.values, data.Close.values

st_dir, _, atr = _compute_supertrend(h, l, c, 10, 3.0)
adx = _compute_adx(h, l, c)
ema = _compute_ema(c, 100)

le, lx, se, sx = _make_signals(st_dir, adx, ema, c, 25, 'both')
print(f'Long entries: {le.sum()}, exits: {lx.sum()}')
print(f'Short entries: {se.sum()}, exits: {sx.sum()}')
"
```

Expected: 5–30 entries per side over a full year. If 0, ADX threshold is too high or data is too short.

- [ ] **Step 3: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: add _make_signals — vectorbt-ready boolean entry/exit arrays"
```

---

## Task 4: Implement `_run_vbt_portfolio` — vectorbt call per indicator combo

**Files:**
- Modify: `optimization/wave1/run_swing3_stage1_parallel_v2.py` — add after `_make_signals`

This function receives pre-computed signals for ONE indicator combo and evaluates all SL variants simultaneously via a single vectorbt call.

- [ ] **Step 1: Add `_build_sl_params_list` helper**

```python
def _build_sl_params_list(sl_type):
    """
    Returns a list of dicts, one per SL/TP combo for the given sl_type.
    Order must be stable — used to map vbt column index back to param dict.
    """
    p = SL_PARAMS[sl_type]
    if sl_type == "embedded":
        return [{"atr_stop_mult": m} for m in p["atr_stop_mult"]]
    elif sl_type in ("fixed_pct", "fixed_signal"):
        return [
            {"stop_loss_pct": sl, "take_profit_pct": tp}
            for sl, tp in product(p["stop_loss_pct"], p["take_profit_pct"])
        ]
    elif sl_type == "atr":
        return [
            {"atr_stop_mult": m, "rr_ratio": r}
            for m, r in product(p["atr_stop_mult"], p["rr_ratio"])
        ]
    raise ValueError(f"Unknown sl_type: {sl_type}")
```

- [ ] **Step 2: Add `_run_vbt_portfolio`**

```python
def _run_vbt_portfolio(close_series, long_entries, long_exits,
                       short_entries, short_exits,
                       sl_type, sl_params_list, atr):
    """
    Run one vbt.Portfolio.from_signals() call covering all SL combos as columns.

    close_series : pd.Series indexed by timestamp
    long_entries / long_exits / short_entries / short_exits : 1D bool numpy arrays
    sl_type      : "embedded" | "fixed_pct" | "fixed_signal" | "atr"
    sl_params_list: list of dicts from _build_sl_params_list()
    atr          : 1D float64 array (ATR values, same length as close)

    Returns pd.DataFrame with one row per SL combo:
      columns: sharpe, trades, win_rate, max_dd
    """
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)

    # Tile signals to (n_bars, n_combos) so each column is one SL variant
    le_2d = np.tile(long_entries[:, None],  (1, n_combos))
    lx_2d = np.tile(long_exits[:, None],    (1, n_combos))
    se_2d = np.tile(short_entries[:, None], (1, n_combos))
    sx_2d = np.tile(short_exits[:, None],   (1, n_combos))

    # Build stop arrays depending on sl_type
    if sl_type == "embedded":
        sl_2d = np.column_stack([
            np.clip(np.where(close_arr > 0, atr * p["atr_stop_mult"] / close_arr, 0.05), 1e-6, 1.0)
            for p in sl_params_list
        ])  # (n_bars, n_combos)
        pf = vbt.Portfolio.from_signals(
            close=close_series,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_2d,
            init_cash=1_000_000, fees=0.0005, freq="1h",
        )

    elif sl_type == "fixed_pct":
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            close=close_series,
            entries=le_2d,
            exits=np.zeros_like(le_2d),          # no signal exit in fixed_pct mode
            short_entries=se_2d,
            short_exits=np.zeros_like(se_2d),
            sl_stop=sl_arr, tp_stop=tp_arr,
            init_cash=1_000_000, fees=0.0005, freq="1h",
        )

    elif sl_type == "fixed_signal":
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            close=close_series,
            entries=le_2d, exits=lx_2d,          # signal exits active
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_arr, tp_stop=tp_arr,
            init_cash=1_000_000, fees=0.0005, freq="1h",
        )

    elif sl_type == "atr":
        sl_2d = np.column_stack([
            np.clip(np.where(close_arr > 0, atr * p["atr_stop_mult"] / close_arr, 0.05), 1e-6, 1.0)
            for p in sl_params_list
        ])
        tp_2d = np.column_stack([
            np.clip(np.where(close_arr > 0, atr * p["atr_stop_mult"] * p["rr_ratio"] / close_arr, 0.1), 1e-6, 5.0)
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            close=close_series,
            entries=le_2d,
            exits=np.zeros_like(le_2d),
            short_entries=se_2d,
            short_exits=np.zeros_like(se_2d),
            sl_stop=sl_2d, tp_stop=tp_2d,
            init_cash=1_000_000, fees=0.0005, freq="1h",
        )
    else:
        raise ValueError(f"Unknown sl_type: {sl_type}")

    # Extract stats — vectorbt 0.28.x returns pd.Series per metric for multi-column pf
    sharpe   = pf.sharpe_ratio()
    n_trades = pf.trades.count()
    wr       = pf.trades.win_rate * 100.0   # fraction → percent
    max_dd   = pf.max_drawdown() * 100.0    # fraction → percent

    def _to_series(x):
        return x if isinstance(x, pd.Series) else pd.Series([x])

    return pd.DataFrame({
        "sharpe":   _to_series(sharpe).values,
        "trades":   _to_series(n_trades).values,
        "win_rate": _to_series(wr).values,
        "max_dd":   _to_series(max_dd).values,
    })
```

> **Note:** If `pf.sharpe_ratio()`, `pf.trades.win_rate`, or `pf.max_drawdown()` raise `AttributeError` in your exact vectorbt 0.28.1 build, use `pf.stats()` as a fallback:
> ```python
> s = pf.stats()
> # Multi-column: s is a DataFrame (rows=cols, stats as columns)
> # Single-column: s is a pd.Series
> if isinstance(s, pd.Series):
>     sharpe, n_trades, wr, max_dd = s['Sharpe Ratio'], s['Total Trades'], s['Win Rate [%]'], s['Max. Drawdown [%]']
> else:
>     sharpe   = s['Sharpe Ratio']
>     n_trades = s['Total Trades']
>     wr       = s['Win Rate [%]']
>     max_dd   = s['Max. Drawdown [%]']
> ```

- [ ] **Step 3: Smoke-test the portfolio runner on BTCUSDT/both/embedded**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys; sys.path.insert(0, r'venv\Lib\site-packages'); sys.path.insert(0, '.')
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import *
from src.core.backtesting_engine import engine
from config.settings import TimeFrame
from datetime import datetime
import pandas as pd

data = engine.get_data('BTCUSDT', TimeFrame.H1, datetime(2022,1,1), datetime(2022,12,31))
h, l, c = data.High.values, data.Low.values, data.Close.values
close_s = pd.Series(c, index=data.index)

st_dir, _, atr = _compute_supertrend(h, l, c, 10, 3.0)
adx = _compute_adx(h, l, c)
ema = _compute_ema(c, 100)
le, lx, se, sx = _make_signals(st_dir, adx, ema, c, 25, 'both')

sl_list = _build_sl_params_list('embedded')
result_df = _run_vbt_portfolio(close_s, le, lx, se, sx, 'embedded', sl_list, atr)
print(result_df)
"
```

Expected: a 3-row DataFrame (one per `atr_stop_mult` value) with non-NaN sharpe values and trade counts > 0. If trade counts are all 0, revisit the signal generation step.

- [ ] **Step 4: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: add _run_vbt_portfolio — vectorized SL sweep via vbt.Portfolio.from_signals"
```

---

## Task 5: Implement `_optimize_vbt` — the 81-combo indicator loop

**Files:**
- Modify: `optimization/wave1/run_swing3_stage1_parallel_v2.py` — add after `_run_vbt_portfolio`

- [ ] **Step 1: Add `_optimize_vbt`**

```python
def _optimize_vbt(data, direction, sl_type):
    """
    Run the full parameter optimization on `data` (train slice or full slice).

    Loops over all 81 unique indicator-param combos. For each combo, computes
    indicators once, then calls _run_vbt_portfolio() for all SL variants in one
    vectorbt call (3–9 combos per call).

    Returns (best_params, best_sharpe, best_trades, best_win_rate, best_max_dd)
    or None if no combo produces >= 30 trades.
    """
    h = data.High.values
    l = data.Low.values
    c = data.Close.values
    close_s = pd.Series(c, index=data.index)

    sl_params_list = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_params = None
    best_trades = 0
    best_wr     = 0.0
    best_dd     = 0.0

    ip = INDICATOR_PARAMS
    for st_period, st_factor, adx_threshold, ema_filter in product(
        ip["st_period"], ip["st_factor"], ip["adx_threshold"], ip["ema_filter"]
    ):
        # Compute indicators once for this combo
        st_dir, _, atr = _compute_supertrend(h, l, c, st_period, st_factor)
        adx             = _compute_adx(h, l, c)            # period fixed at 14
        ema             = _compute_ema(c, ema_filter)

        le, lx, se, sx  = _make_signals(st_dir, adx, ema, c, adx_threshold, direction)

        # Skip combos with no signals at all (saves a vbt call)
        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_params_list, atr)
        except Exception as e:
            print(f"    vbt error [{st_period},{st_factor},{adx_threshold},{ema_filter}]: {e}")
            continue

        for row_idx, sl_p in enumerate(sl_params_list):
            row = stats_df.iloc[row_idx]
            sharpe   = float(row["sharpe"])   if np.isfinite(row["sharpe"])   else -np.inf
            n_trades = int(row["trades"])
            wr       = float(row["win_rate"]) if np.isfinite(row["win_rate"]) else 0.0
            dd       = float(row["max_dd"])   if np.isfinite(row["max_dd"])   else 0.0

            if n_trades < 30:
                continue
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_trades = n_trades
                best_wr     = wr
                best_dd     = dd
                best_params = {
                    "st_period":     st_period,
                    "st_factor":     st_factor,
                    "adx_threshold": adx_threshold,
                    "ema_filter":    ema_filter,
                    "direction":     direction,
                    **sl_p,
                }

    if best_params is None:
        return None
    return best_params, best_sharpe, best_trades, best_wr, best_dd
```

- [ ] **Step 2: Test `_optimize_vbt` on one task — time it**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys, time
sys.path.insert(0, r'venv\Lib\site-packages'); sys.path.insert(0, '.')
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import _optimize_vbt
from src.core.backtesting_engine import engine
from config.settings import TimeFrame
from datetime import datetime

data = engine.get_data('BTCUSDT', TimeFrame.H1, datetime(2022,1,1), datetime(2024,12,31))
split_idx = int(len(data) * 0.7)
train = data.iloc[:split_idx]

t0 = time.perf_counter()
result = _optimize_vbt(train, 'both', 'embedded')
elapsed = time.perf_counter() - t0

print(f'Elapsed: {elapsed:.2f}s')
if result:
    params, sharpe, trades, wr, dd = result
    print(f'Best: sharpe={sharpe:.4f} trades={trades} wr={wr:.1f}% dd={dd:.1f}%')
    print(f'Params: {params}')
else:
    print('No combo passed the 30-trade filter')
"
```

Expected: completes in **< 30 seconds** (vs ~97s for v1 `embedded`). If > 60s, check that numba compiled correctly (first run triggers JIT compilation — time a second run).

- [ ] **Step 3: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: add _optimize_vbt — 81-combo indicator loop with vectorbt inner sweep"
```

---

## Task 6: Implement `_eval_single` and wire up `_worker_v2`

**Files:**
- Modify: `optimization/wave1/run_swing3_stage1_parallel_v2.py` — replace the `_worker_v2` stub

- [ ] **Step 1: Add `_eval_single`**

Insert this before `_worker_v2`:

```python
def _eval_single(data, direction, sl_type, best_params):
    """
    Evaluate a single parameter combo on `data` (the OOS test slice).
    Returns (oos_sharpe, oos_trades) — or (None, 0) on error.
    """
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s = pd.Series(c, index=data.index)

    try:
        st_dir, _, atr = _compute_supertrend(h, l, c,
                                              best_params["st_period"],
                                              best_params["st_factor"])
        adx = _compute_adx(h, l, c)
        ema = _compute_ema(c, best_params["ema_filter"])
        le, lx, se, sx = _make_signals(st_dir, adx, ema, c,
                                        best_params["adx_threshold"], direction)

        # Build a single-element sl_params_list from best_params
        if sl_type == "embedded":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct":   best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        elif sl_type == "atr":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")

        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr)
        row = stats_df.iloc[0]
        oos_sharpe = float(row["sharpe"])  if np.isfinite(row["sharpe"])   else None
        oos_trades = int(row["trades"])
        return oos_sharpe, oos_trades
    except Exception as e:
        print(f"    _eval_single error: {e}", flush=True)
        return None, 0
```

- [ ] **Step 2: Replace the `_worker_v2` stub with the full implementation**

```python
def _worker_v2(task):
    """
    Vectorbt-based optimization worker. Drop-in replacement for _worker() in v1.
    Each spawned process sets up its own sys.path (no shared state with parent).
    """
    sym, direction, sl_type = task
    import sys
    sys.path.insert(0, str(VENV_SITE_PACKAGES))
    sys.path.insert(0, str(BACKTESTING_MCP))

    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame

    symbol_usdt = sym + "USDT"
    note = (V2_NOTE + " ~9 months data") if sym in LIMITED_DATA else V2_NOTE
    log_prefix = f"[{symbol_usdt} {direction} {sl_type}]"

    print(f"{log_prefix} Loading data...", flush=True)
    try:
        data = engine.get_data(symbol_usdt, TimeFrame.H1,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        print(f"{log_prefix} DATA ERROR: {e}", flush=True)
        return _make_result(symbol_usdt, direction, sl_type, note=f"DATA ERROR: {e}")

    if data.empty or len(data) < 500:
        return _make_result(symbol_usdt, direction, sl_type, note="insufficient data")

    split_idx  = int(len(data) * 0.7)
    train_data = data.iloc[:split_idx]
    test_data  = data.iloc[split_idx:]

    print(f"{log_prefix} Optimizing on {len(train_data)} train bars...", flush=True)
    try:
        opt = _optimize_vbt(train_data, direction, sl_type)
    except Exception as e:
        print(f"{log_prefix} OPT ERROR: {e}", flush=True)
        return _make_result(symbol_usdt, direction, sl_type, note=f"OPT ERROR: {e}")

    if opt is None:
        return _make_result(symbol_usdt, direction, sl_type,
                            note=note + " | no combo passed 30-trade filter")

    best_params, train_sharpe, num_trades, win_rate, max_dd = opt
    print(f"{log_prefix} Best train: sharpe={train_sharpe:.4f} trades={num_trades}", flush=True)

    if num_trades < 30:
        return _make_result(symbol_usdt, direction, sl_type,
                            best_params=best_params, train_sharpe=train_sharpe,
                            num_trades=num_trades, win_rate=win_rate, max_dd=max_dd,
                            note=note + f" | num_trades={num_trades} < 30")

    print(f"{log_prefix} Evaluating OOS on {len(test_data)} bars...", flush=True)
    oos_sharpe, oos_trades = _eval_single(test_data, direction, sl_type, best_params)

    verdict = "PASS" if (oos_sharpe is not None and oos_sharpe > 0) else "FAIL"
    oos_str = f"{oos_sharpe:.4f}" if oos_sharpe is not None else "None"
    print(f"{log_prefix} OOS sharpe={oos_str} => {verdict}", flush=True)

    return _make_result(
        symbol_usdt, direction, sl_type,
        best_params=best_params, train_sharpe=train_sharpe,
        oos_sharpe=oos_sharpe, num_trades=num_trades,
        win_rate=win_rate, max_dd=max_dd,
        verdict=verdict, note=note,
    )
```

- [ ] **Step 3: Commit**

```bash
git add optimization/wave1/run_swing3_stage1_parallel_v2.py
git commit -m "feat: implement _eval_single and _worker_v2 — full v2 worker pipeline"
```

---

## Task 7: End-to-end smoke test + timing comparison

**Files:**
- No code changes — validation only

- [ ] **Step 1: Run a single task end-to-end and inspect the JSON output**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys, json
sys.path.insert(0, r'venv\Lib\site-packages'); sys.path.insert(0, '.')
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import _worker_v2
import time

t0 = time.perf_counter()
result = _worker_v2(('BTC', 'both', 'embedded'))
elapsed = time.perf_counter() - t0

print(f'Elapsed: {elapsed:.2f}s')
print(json.dumps(result, indent=2))
"
```

Expected:
- Elapsed: **< 30s** (first run includes numba JIT compile ~5–10s; subsequent runs < 10s)
- JSON has all required fields: `verdict`, `oos_sharpe`, `train_sharpe`, `num_trades`, `best_params`, `note` contains `"v2/vectorbt"`
- `best_params` includes `st_period`, `st_factor`, `adx_threshold`, `ema_filter`, `direction`, and the SL param(s) for `embedded`

- [ ] **Step 2: Compare verdict against v1 result for the same task**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
type results\SWING3\stage1\BTCUSDT_1h_both_embedded.json
```

Compare `verdict` and `oos_sharpe` sign. The exact numbers will differ (vectorbt vs backtesting.py simulation), but PASS/FAIL should match for BTC (the cleaner signal set). If they diverge, check that `_make_signals` flip conventions match the SWING3 strategy's `st_flipped_bull`/`st_flipped_bear` logic.

- [ ] **Step 3: Run a small batch to check parallelism and timing**

Run 12 tasks (one full symbol across all direction+sl_type combos) with 4 workers:

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe -c "
import sys, time, json
from pathlib import Path
sys.path.insert(0, r'venv\Lib\site-packages'); sys.path.insert(0, '.')
sys.path.insert(0, r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\optimization\wave1')
from run_swing3_stage1_parallel_v2 import _worker_v2, DIRECTIONS, SL_TYPES
from concurrent.futures import ProcessPoolExecutor, as_completed

tasks = [('ETH', d, s) for d in DIRECTIONS for s in SL_TYPES]  # 12 tasks
t0 = time.perf_counter()
with ProcessPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(_worker_v2, t): t for t in tasks}
    for fut in as_completed(futures):
        t = futures[fut]
        r = fut.result()
        print(f'{t[0]} {t[1]} {t[2]}: {r[\"verdict\"]} oos={r[\"oos_sharpe\"]}')
elapsed = time.perf_counter() - t0
print(f'12 tasks in {elapsed:.1f}s ({elapsed/12:.1f}s/task avg)')
"
```

Expected: 12 tasks in **< 3 min** with 4 workers. If any task crashes, the exception message will be printed — fix before running full stage1.

- [ ] **Step 4: Run the full stage1 (when ready)**

```powershell
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
.\venv\Scripts\python.exe ..\trading-strategies-research\optimization\wave1\run_swing3_stage1_parallel_v2.py --skip-download
```

The `--skip-download` flag skips re-downloading data that's already in the DB from v1 runs.

- [ ] **Step 5: Commit results**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
git add results/SWING3/stage1/
git commit -m "results: SWING3 stage1 v2/vectorbt optimization run"
```

---

## Self-Review Checklist

- [x] **Spec coverage:** All 9 spec sections covered — outer shell (4.1), worker (4.2), indicators (4.3), signals (4.4), vbt portfolios per sl_type (4.5), stats extraction (4.6), walk-forward (4.7), parameter grid (5), output format (6)
- [x] **No placeholders:** Every step has exact code or exact commands
- [x] **Type consistency:** `_build_sl_params_list` → `_run_vbt_portfolio` → `_optimize_vbt` → `_eval_single` → `_worker_v2` — all consistent parameter names (`sl_params_list`, `best_params`, `sl_type`)
- [x] **`_make_result` signature:** Called identically in `_worker_v2` as it is in v1
- [x] **Limited data note:** `LIMITED_DATA = {"ENA", "TAO"}` is in the scaffold, `note` field in `_worker_v2` includes the warning
- [x] **vectorbt API fallback:** Task 4 step 2 includes a note on using `pf.stats()` if direct attribute accessors differ in the installed build
