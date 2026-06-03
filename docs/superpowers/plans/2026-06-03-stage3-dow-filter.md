# Stage 3 DOW Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** For each of the 2,314 Stage 2 passing combos, test 8 day-of-week entry masks and record which mask (or ALL) produces the best OOS Sharpe, writing one JSON result per combo and a markdown summary per strategy.

**Architecture:** Approach A — `stage3_utils.py` owns Stage 2 loading, DOW mask constants, winner selection, parallel dispatch, and JSON I/O. Each of 10 per-strategy scripts copies only its indicator functions + `_eval_single_dow` from Stage 2, runs 8 DOW evaluations per combo, and delegates orchestration to `run_stage3_parallel`. Scripts are ~200 lines each (no optimization loop).

**Tech Stack:** Python 3.x, vectorbt, numba (SWING3/SWING4 only), `ProcessPoolExecutor`, BacktestingMCP engine

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `optimization/wave3/stage3_utils.py` | Create | DOW masks, Stage 2 loading, winner selection, executor, JSON I/O |
| `optimization/wave3/tests/__init__.py` | Create | Package marker |
| `optimization/wave3/tests/test_stage3_utils.py` | Create | Unit tests for utils |
| `optimization/wave3/run_swing3_stage3_parallel_v2.py` | Create | SWING3 — 1h reference script |
| `optimization/wave3/run_swing5_stage3_parallel_v2.py` | Create | SWING5 — 1h |
| `optimization/wave3/run_ema_rej_v1_stage3_parallel_v2.py` | Create | EMA_REJ_V1 — 1h |
| `optimization/wave3/run_vr1_stage3_parallel_v2.py` | Create | VR1 — 1h |
| `optimization/wave3/run_vp1_stage3_parallel_v2.py` | Create | VP1 — 1h |
| `optimization/wave3/run_swing2_stage3_parallel_v2.py` | Create | SWING2 — 4h reference script |
| `optimization/wave3/run_swing4_stage3_parallel_v2.py` | Create | SWING4 — 4h |
| `optimization/wave3/run_dc1_stage3_parallel_v2.py` | Create | DC1 — 4h |
| `optimization/wave3/run_aggr_pullback_stage3_parallel_v2.py` | Create | AGGR_PULLBACK — 4h |
| `optimization/wave3/run_mo1_stage3_parallel_v2.py` | Create | MO1 — 4h |
| `optimization/wave3/generate_stage3_summary.py` | Create | Summary markdown generator |

---

## Task 1: Create `stage3_utils.py` with unit tests

**Files:**
- Create: `optimization/wave3/stage3_utils.py`
- Create: `optimization/wave3/tests/__init__.py`
- Create: `optimization/wave3/tests/test_stage3_utils.py`

- [ ] **Step 1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force "optimization/wave3/tests"
```

- [ ] **Step 2: Write failing tests**

Create `optimization/wave3/tests/test_stage3_utils.py`:

```python
# Run with: python -m pytest tests/test_stage3_utils.py -v
# Requires: pip install pytest  (or use BacktestingMCP venv which has pytest)
import json
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from stage3_utils import DOW_MASKS, MIN_TRADES, MIN_LIFT, select_winner, load_stage2_passing


def _write_stage2_json(base, strategy_id, symbol, tf, direction, sl_type,
                       oos_sharpe, best_params=None, verdict="PASS"):
    d = base / strategy_id / "stage2"
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": symbol, "timeframe": tf, "direction": direction,
        "sl_type": sl_type, "oos_sharpe": oos_sharpe, "verdict": verdict,
        "best_params": best_params or {"p": 1},
    }
    (d / f"{symbol}_{tf}_{direction}_{sl_type}.json").write_text(json.dumps(payload))


def _make_dow_results(all_s=0.8, monf_s=1.1, monf_t=25, all_t=38):
    return {
        "ALL":     {"oos_sharpe": all_s,  "num_trades": all_t},
        "MON-FRI": {"oos_sharpe": monf_s, "num_trades": monf_t},
        "SAT-SUN": {"oos_sharpe": 0.3,   "num_trades": 12},
        "MON":     {"oos_sharpe": 0.9,   "num_trades": 8},
        "TUE":     {"oos_sharpe": 0.95,  "num_trades": 9},
        "WED":     {"oos_sharpe": 0.7,   "num_trades": 7},
        "THU":     {"oos_sharpe": 1.0,   "num_trades": 6},
        "FRI":     {"oos_sharpe": 0.85,  "num_trades": 8},
    }


def test_select_winner_picks_best_with_improvement():
    results = _make_dow_results(all_s=0.8, monf_s=1.1, monf_t=25)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "MON-FRI"
    assert sharpe == 1.1
    assert trades == 25
    assert improved is True


def test_select_winner_defaults_to_all_insufficient_lift():
    # MON-FRI is 0.09 above ALL — below 0.10 threshold
    results = _make_dow_results(all_s=0.8, monf_s=0.89, monf_t=25)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_defaults_to_all_insufficient_trades():
    # MON-FRI has only 15 trades — below MIN_TRADES=20
    results = _make_dow_results(all_s=0.8, monf_s=1.5, monf_t=15)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_boundary_exact_lift():
    # Exactly 0.10 above ALL — should NOT be accepted (must be strictly greater)
    results = _make_dow_results(all_s=0.8, monf_s=0.90, monf_t=25)
    mask, _, _, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_boundary_above_lift():
    # 0.101 above ALL — should be accepted
    results = _make_dow_results(all_s=0.8, monf_s=0.901, monf_t=25)
    mask, _, _, improved = select_winner(results)
    assert mask == "MON-FRI"
    assert improved is True


def test_select_winner_all_has_no_trades_defaults_gracefully():
    results = {k: {"oos_sharpe": None, "num_trades": 0} for k in DOW_MASKS}
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_dow_masks_has_8_entries():
    assert len(DOW_MASKS) == 8


def test_dow_masks_all_is_none():
    assert DOW_MASKS["ALL"] is None


def test_dow_masks_weekdays():
    assert DOW_MASKS["MON-FRI"] == {0, 1, 2, 3, 4}


def test_load_stage2_passing_reads_pass_only():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage2_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr", 0.8)
        _write_stage2_json(tmp, "SWING3", "ETHUSDT", "4h", "long", "embedded", 0.3, verdict="FAIL")
        result = load_stage2_passing("SWING3", tmp)
        assert len(result) == 1
        assert result[0]["symbol"] == "BTCUSDT"
        assert result[0]["stage2_oos_sharpe"] == 0.8
        assert "best_params" in result[0]


def test_load_stage2_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_stage2_passing("NONEXISTENT", Path(tmp))
        assert result == []
```

- [ ] **Step 3: Run tests to confirm they fail**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -m pytest tests/test_stage3_utils.py -v
```

Expected: `ModuleNotFoundError: No module named 'stage3_utils'`

- [ ] **Step 4: Implement `stage3_utils.py`**

Create `optimization/wave3/stage3_utils.py`:

```python
#!/usr/bin/env python3
"""
Shared machinery for Stage 3 DOW filter scripts.

Exports:
    DOW_MASKS    — 8 entry masks keyed by name
    MIN_TRADES   — minimum OOS trades for a mask to be a candidate (20)
    MIN_LIFT     — minimum absolute Sharpe improvement over ALL (0.10)
    load_stage2_passing(strategy_id, results_base) -> list[dict]
    select_winner(dow_results) -> (mask, sharpe, trades, improved)
    run_stage3_parallel(strategy_id, results_base, symbols, worker_fn,
                        backtesting_mcp, workers, skip_download)
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed, BrokenExecutor
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import numpy as np

DOW_MASKS = {
    "ALL":     None,
    "MON-FRI": {0, 1, 2, 3, 4},
    "SAT-SUN": {5, 6},
    "MON":     {0},
    "TUE":     {1},
    "WED":     {2},
    "THU":     {3},
    "FRI":     {4},
}

MIN_TRADES = 20
MIN_LIFT   = 0.10

TF_ENUM_NAME = {
    "15m": "M15",
    "1h":  "H1",
    "4h":  "H4",
    "12h": "H12",
}

_START = datetime(2022, 1, 1)
_END   = datetime(2024, 12, 31)


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):  return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray):  return obj.tolist()
        return super().default(obj)


def load_stage2_passing(strategy_id: str, results_base: Path) -> list:
    """Return list of dicts for every Stage 2 PASS result for this strategy."""
    stage2_dir = results_base / strategy_id / "stage2"
    passing = []
    if not stage2_dir.exists():
        return passing
    for fpath in stage2_dir.glob("*.json"):
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
            continue
        if data.get("verdict") != "PASS":
            continue
        sym = data.get("symbol", "")
        if not sym.endswith("USDT"):
            continue
        passing.append({
            "symbol":            sym,
            "timeframe":         data.get("timeframe", ""),
            "direction":         data.get("direction", ""),
            "sl_type":           data.get("sl_type", ""),
            "best_params":       data.get("best_params") or {},
            "stage2_oos_sharpe": data.get("oos_sharpe"),
        })
    return passing


def select_winner(dow_results: dict) -> tuple:
    """
    Given {mask_name: {"oos_sharpe": float|None, "num_trades": int}},
    return (winner_mask, winner_sharpe, winner_trades, dow_improved).

    A non-ALL mask wins only if:
      - it has >= MIN_TRADES trades, AND
      - its Sharpe is strictly > ALL Sharpe + MIN_LIFT
    Otherwise ALL is returned with dow_improved=False.
    """
    all_data   = dow_results.get("ALL", {})
    all_sharpe = all_data.get("oos_sharpe") or 0.0
    all_trades = all_data.get("num_trades", 0)

    candidates = {
        name: data for name, data in dow_results.items()
        if name != "ALL"
        and data.get("num_trades", 0) >= MIN_TRADES
        and data.get("oos_sharpe") is not None
    }

    if candidates:
        best = max(candidates, key=lambda m: candidates[m]["oos_sharpe"])
        best_sharpe = candidates[best]["oos_sharpe"]
        best_trades = candidates[best]["num_trades"]
        if best_sharpe > all_sharpe + MIN_LIFT:
            return (best, best_sharpe, best_trades, True)

    return ("ALL", all_data.get("oos_sharpe"), all_trades, False)


def _predownload(strategy_id: str, results_base: Path, backtesting_mcp: Path) -> None:
    """Download unique TFs present in Stage 2 passing combos for this strategy."""
    passing = load_stage2_passing(strategy_id, results_base)
    if not passing:
        return
    tfs = sorted({c["timeframe"] for c in passing})
    syms = sorted({c["symbol"].replace("USDT", "") for c in passing})

    sys.path.insert(0, str(backtesting_mcp / "venv" / "Lib" / "site-packages"))
    sys.path.insert(0, str(backtesting_mcp))
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame

    for tf in tfs:
        tf_enum = getattr(TimeFrame, TF_ENUM_NAME[tf])
        print(f"Pre-downloading {len(syms)} symbols ({tf})...")
        for sym in syms:
            symbol_usdt = sym + "USDT"
            try:
                d = engine.get_data(symbol_usdt, tf_enum, _START, _END)
                print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
            except Exception as e:
                print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
        print()


def run_stage3_parallel(
    strategy_id: str,
    results_base: Path,
    symbols: list,
    worker_fn: Callable,
    backtesting_mcp: Path,
    workers: Optional[int] = None,
    skip_download: bool = False,
) -> None:
    if workers is None:
        workers = max(1, (os.cpu_count() or 4) - 2)

    stage3_dir = results_base / strategy_id / "stage3"
    stage3_dir.mkdir(parents=True, exist_ok=True)

    if not skip_download:
        _predownload(strategy_id, results_base, backtesting_mcp)

    passing = load_stage2_passing(strategy_id, results_base)
    print(f"\n{strategy_id} Stage 3 — {len(passing)} Stage 2 passing combos")

    all_tasks, done = [], 0
    for combo in passing:
        sym       = combo["symbol"].replace("USDT", "")
        tf        = combo["timeframe"]
        direction = combo["direction"]
        sl_type   = combo["sl_type"]
        fname = f"{combo['symbol']}_{tf}_{direction}_{sl_type}_dow.json"
        fpath = stage3_dir / fname
        if fpath.exists():
            try:
                note = str(json.loads(fpath.read_text(encoding="utf-8")).get("note", ""))
                if not any(e in note for e in ("WORKER CRASH", "DOW ERROR", "DATA ERROR")):
                    done += 1
                    continue
            except Exception:
                pass
        all_tasks.append({
            "sym":               sym,
            "tf":                tf,
            "direction":         direction,
            "sl_type":           sl_type,
            "best_params":       combo["best_params"],
            "stage2_oos_sharpe": combo["stage2_oos_sharpe"],
        })

    total = len(passing)
    print(f"Tasks: {len(all_tasks)} to run, {done} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do — all results already on disk.")
        return

    remaining = list(all_tasks)
    while remaining:
        try:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(worker_fn, task): task for task in remaining}
                completed_tasks = []
                for future in as_completed(futures):
                    task = futures[future]
                    completed_tasks.append(task)
                    try:
                        result = future.result()
                    except Exception as e:
                        result = {
                            "symbol":    task["sym"] + "USDT",
                            "timeframe": task["tf"],
                            "direction": task["direction"],
                            "sl_type":   task["sl_type"],
                            "note":      f"WORKER CRASH: {e}",
                        }

                    sym_usdt  = result.get("symbol", "?")
                    tf_r      = result.get("timeframe", "?")
                    direction = result.get("direction", "?")
                    sl_type   = result.get("sl_type", "?")
                    winner    = result.get("winner_mask", "?")
                    improved  = result.get("dow_improved", False)

                    fname = f"{sym_usdt}_{tf_r}_{direction}_{sl_type}_dow.json"
                    (stage3_dir / fname).write_text(
                        json.dumps(result, indent=2, cls=_NumpyEncoder),
                        encoding="utf-8",
                    )
                    done += 1
                    print(
                        f"[{done}/{total}] {sym_usdt} {tf_r} {direction} {sl_type}"
                        f" → winner={winner} improved={improved}",
                        flush=True,
                    )
                remaining = []
        except BrokenExecutor:
            completed_set = {(t["sym"], t["tf"], t["direction"], t["sl_type"])
                             for t in completed_tasks}
            remaining = [t for t in remaining
                         if (t["sym"], t["tf"], t["direction"], t["sl_type"])
                         not in completed_set]
            print(f"Pool broken — restarting with {len(remaining)} remaining", flush=True)

    print(f"\n{strategy_id} Stage 3 complete")
```

- [ ] **Step 5: Run tests — confirm 11 pass**

```powershell
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -m pytest tests/test_stage3_utils.py -v
```

Expected:
```
11 passed in 0.XX s
```

- [ ] **Step 6: Commit**

```powershell
git add optimization/wave3/stage3_utils.py optimization/wave3/tests/
git commit -m "feat: stage3_utils — DOW masks, Stage 2 loading, winner selection, parallel executor"
```

---

## Task 2: Create `run_swing3_stage3_parallel_v2.py` (1h reference template)

**Files:**
- Source: `optimization/wave2/run_swing3_stage2_parallel_v2.py`
- Create: `optimization/wave3/run_swing3_stage3_parallel_v2.py`

- [ ] **Step 1: Copy Stage 2 script as starting point**

```powershell
Copy-Item optimization/wave2/run_swing3_stage2_parallel_v2.py `
          optimization/wave3/run_swing3_stage3_parallel_v2.py
```

- [ ] **Step 2: Replace header and add stage3_utils import**

Replace the opening docstring + import block with:

```python
"""
SWING3 Stage 3 optimization — DOW filter (PARALLEL).

Tests 8 day-of-week entry masks on Stage 2 passing combos.
Entry signals are zeroed on non-matching DOW bars; SL/TP active on all bars.

Usage:
    python run_swing3_stage3_parallel_v2.py
    python run_swing3_stage3_parallel_v2.py --workers 8
    python run_swing3_stage3_parallel_v2.py --skip-download
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage3_utils import run_stage3_parallel, DOW_MASKS, select_winner
```

- [ ] **Step 3: Update constants block**

Replace the `STRATEGY_ID / HOME_TF / RESULTS_BASE / TF_MAP / TF_FREQ_MAP / VENV_SITE_PACKAGES` block with:

```python
STRATEGY_ID  = "SWING3"
STRATEGY_KEY = "swing3_supertrend_adx"
HOME_TF      = "1h"
RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
V2_NOTE      = "v2/vectorbt"

TF_MAP = {
    "15m": "M15",
    "4h":  "H4",
    "12h": "H12",
}

# Vectorbt freq strings for Sharpe annualization — must match the actual off-TF data
TF_FREQ_MAP = {
    "15m": "15min",
    "4h":  "4h",
    "12h": "12h",
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"
```

- [ ] **Step 4: Delete functions not needed in Stage 3**

Delete the following functions entirely:
- `_build_sl_params_list`
- `_optimize_vbt`

Keep: `_supertrend_loop`, `_compute_supertrend`, `_compute_adx`, `_compute_ema`, `_make_signals`, `_extract_pf_stats`, `_run_vbt_portfolio`.

- [ ] **Step 5: Rename `_eval_single` to `_eval_single_dow` and add DOW masking**

Replace the existing `_eval_single` function with:

```python
def _eval_single_dow(data, direction, sl_type, best_params, dow_days, freq="1h"):
    """
    Evaluate best_params on data slice with DOW entry masking.
    dow_days: set of weekday ints (0=Mon..6=Sun), or None for no filter.
    Returns (oos_sharpe, num_trades) or (None, 0) on error.
    """
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)

    try:
        st_dir, _, atr = _compute_supertrend(h, l, c,
                                              best_params["st_period"],
                                              best_params["st_factor"])
        adx = _compute_adx(h, l, c)
        ema = _compute_ema(c, best_params["ema_filter"])
        le, lx, se, sx = _make_signals(st_dir, adx, ema, c,
                                        best_params["adx_threshold"], direction)

        # DOW masking — zero out entries on non-matching days
        if dow_days is not None:
            dow_bool = pd.Series(data.index).dt.dayofweek.isin(dow_days).values
            le = le & dow_bool
            se = se & dow_bool

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

        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr, freq=freq)
        row      = stats_df.iloc[0]
        sharpe   = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        n_trades = int(row["trades"])
        return sharpe, n_trades
    except Exception as e:
        print(f"    _eval_single_dow error: {e}", flush=True)
        return None, 0
```

- [ ] **Step 6: Replace `_worker_v2` entirely**

```python
def _worker_v2(task):
    """
    Stage 3 worker. One process per Stage 2 passing combo.
    Runs _eval_single_dow for each of the 8 DOW masks, then selects winner.
    """
    sym               = task["sym"]
    tf                = task["tf"]
    direction         = task["direction"]
    sl_type           = task["sl_type"]
    best_params       = task["best_params"]
    stage2_oos_sharpe = task["stage2_oos_sharpe"]

    import sys
    sys.path.insert(0, str(VENV_SITE_PACKAGES))
    sys.path.insert(0, str(BACKTESTING_MCP))
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame

    symbol_usdt = sym + "USDT"
    note        = (V2_NOTE + " ~9 months data") if sym in LIMITED_DATA else V2_NOTE
    log_prefix  = f"[{symbol_usdt} {tf} {direction} {sl_type}]"
    tf_enum     = getattr(TimeFrame, TF_MAP[tf])

    print(f"{log_prefix} loading data...", flush=True)
    try:
        data = engine.get_data(symbol_usdt, tf_enum,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        print(f"{log_prefix} DATA ERROR: {e}", flush=True)
        return {
            "symbol": symbol_usdt, "timeframe": tf,
            "direction": direction, "sl_type": sl_type,
            "note": f"DATA ERROR: {e}",
        }

    if data.empty or len(data) < 500:
        return {
            "symbol": symbol_usdt, "timeframe": tf,
            "direction": direction, "sl_type": sl_type,
            "note": "insufficient data",
        }

    test_data = data.iloc[int(len(data) * 0.7):]

    print(f"{log_prefix} running 8 DOW masks ({len(test_data)} OOS bars)...", flush=True)
    dow_results = {}
    for mask_name, dow_days in DOW_MASKS.items():
        sharpe, trades = _eval_single_dow(
            test_data, direction, sl_type, best_params,
            dow_days=dow_days, freq=TF_FREQ_MAP[tf],
        )
        dow_results[mask_name] = {"oos_sharpe": sharpe, "num_trades": trades}

    winner_mask, winner_sharpe, winner_trades, dow_improved = select_winner(dow_results)
    print(
        f"{log_prefix} winner={winner_mask} sharpe={winner_sharpe} improved={dow_improved}",
        flush=True,
    )

    return {
        "strategy":         STRATEGY_KEY,
        "symbol":           symbol_usdt,
        "timeframe":        tf,
        "direction":        direction,
        "sl_type":          sl_type,
        "stage":            3,
        "best_params":      best_params,
        "stage2_oos_sharpe": stage2_oos_sharpe,
        "dow_results":      dow_results,
        "winner_mask":      winner_mask,
        "winner_sharpe":    winner_sharpe,
        "winner_trades":    winner_trades,
        "dow_improved":     dow_improved,
        "note":             note,
    }
```

- [ ] **Step 7: Replace `main()`**

Delete old `main()` and replace with:

```python
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="SWING3 Stage 3 — DOW filter (15m, 4h, 12h off-TFs)")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    run_stage3_parallel(
        strategy_id    = STRATEGY_ID,
        results_base   = RESULTS_BASE,
        symbols        = SYMBOLS,
        worker_fn      = _worker_v2,
        backtesting_mcp= BACKTESTING_MCP,
        workers        = args.workers,
        skip_download  = args.skip_download,
    )


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
```

- [ ] **Step 8: Verify clean import**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "import run_swing3_stage3_parallel_v2; print('Import OK')"
```

Expected: `Import OK`

- [ ] **Step 9: Commit**

```powershell
git add optimization/wave3/run_swing3_stage3_parallel_v2.py
git commit -m "feat: SWING3 Stage 3 — DOW filter script (entry masking, 8 masks)"
```

---

## Task 3: Create remaining 1h home TF scripts (SWING5, EMA_REJ_V1, VR1, VP1)

Each follows the exact same transformation as Task 2. For each:
1. Copy from the corresponding Stage 2 script in `optimization/wave2/`
2. Apply all changes from Task 2 steps 2–7

**Strategy-specific values:**

| Script | STRATEGY_ID | STRATEGY_KEY | Stage 2 source |
|---|---|---|---|
| run_swing5_stage3_parallel_v2.py | "SWING5" | "swing5_keltner_breakout" | run_swing5_stage2_parallel_v2.py |
| run_ema_rej_v1_stage3_parallel_v2.py | "EMA_REJ_V1" | "ema_rejection_v1" | run_ema_rej_v1_stage2_parallel_v2.py |
| run_vr1_stage3_parallel_v2.py | "VR1" | "vr1_vwap_mean_reversion" | run_vr1_stage2_parallel_v2.py |
| run_vp1_stage3_parallel_v2.py | "VP1" | "vp1_volume_profile_breakout" | run_vp1_stage2_parallel_v2.py |

**TF_MAP and TF_FREQ_MAP are identical for all 1h home TF scripts:**
```python
TF_MAP     = {"15m": "M15", "4h": "H4", "12h": "H12"}
TF_FREQ_MAP = {"15m": "15min", "4h": "4h", "12h": "12h"}
```

**EMA_REJ_V1 special case — `_eval_single_dow` has extra parameters:**

EMA_REJ_V1's `_eval_single` (in Stage 2) takes `(data, direction, sl_type, best_params, atr_test, htf_bars, freq)`. The Stage 3 version adds `dow_days`:

```python
def _eval_single_dow(data, direction, sl_type, best_params, atr_test, htf_bars, dow_days, freq="1h"):
```

And in `_worker_v2`, compute `atr_test` and `htf_bars` before the DOW loop:

```python
    h_test = test_data.High.values
    l_test = test_data.Low.values
    c_test = test_data.Close.values
    atr_test = _compute_atr(h_test, l_test, c_test)
    htf_bars = HTF_BARS_MAP[tf]

    for mask_name, dow_days in DOW_MASKS.items():
        sharpe, trades = _eval_single_dow(
            test_data, direction, sl_type, best_params,
            atr_test, htf_bars=htf_bars,
            dow_days=dow_days, freq=TF_FREQ_MAP[tf],
        )
```

`HTF_BARS_MAP` is kept from Stage 2: `{"15m": 36, "4h": 2, "12h": 1}`.

- [ ] **Copy and patch SWING5**

```powershell
Copy-Item optimization/wave2/run_swing5_stage2_parallel_v2.py `
          optimization/wave3/run_swing5_stage3_parallel_v2.py
```

Apply Task 2 steps 2–7 with `STRATEGY_ID = "SWING5"`, `STRATEGY_KEY = "swing5_keltner_breakout"`.

SWING5 has `THRESHOLD_PARAMS` — leave unchanged (part of indicator logic).

```powershell
git add optimization/wave3/run_swing5_stage3_parallel_v2.py
git commit -m "feat: SWING5 Stage 3 — DOW filter script"
```

- [ ] **Copy and patch EMA_REJ_V1**

```powershell
Copy-Item optimization/wave2/run_ema_rej_v1_stage2_parallel_v2.py `
          optimization/wave3/run_ema_rej_v1_stage3_parallel_v2.py
```

Apply Task 2 steps 2–7 with `STRATEGY_ID = "EMA_REJ_V1"`, `STRATEGY_KEY = "ema_rejection_v1"`, plus the EMA_REJ_V1 special case above for `_eval_single_dow` and `_worker_v2`.

```powershell
git add optimization/wave3/run_ema_rej_v1_stage3_parallel_v2.py
git commit -m "feat: EMA_REJ_V1 Stage 3 — DOW filter script (HTF_BARS_MAP preserved)"
```

- [ ] **Copy and patch VR1**

```powershell
Copy-Item optimization/wave2/run_vr1_stage2_parallel_v2.py `
          optimization/wave3/run_vr1_stage3_parallel_v2.py
```

Apply Task 2 steps 2–7 with `STRATEGY_ID = "VR1"`, `STRATEGY_KEY = "vr1_vwap_mean_reversion"`.

```powershell
git add optimization/wave3/run_vr1_stage3_parallel_v2.py
git commit -m "feat: VR1 Stage 3 — DOW filter script"
```

- [ ] **Copy and patch VP1**

```powershell
Copy-Item optimization/wave2/run_vp1_stage2_parallel_v2.py `
          optimization/wave3/run_vp1_stage3_parallel_v2.py
```

Apply Task 2 steps 2–7 with `STRATEGY_ID = "VP1"`, `STRATEGY_KEY = "vp1_volume_profile_breakout"`.

VP1 has `_VA_Z` dict — leave unchanged.

```powershell
git add optimization/wave3/run_vp1_stage3_parallel_v2.py
git commit -m "feat: VP1 Stage 3 — DOW filter script"
```

- [ ] **Verify all 4 import cleanly**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "
import run_swing5_stage3_parallel_v2
import run_ema_rej_v1_stage3_parallel_v2
import run_vr1_stage3_parallel_v2
import run_vp1_stage3_parallel_v2
print('All 4 import OK')
"
```

Expected: `All 4 import OK`

---

## Task 4: Create `run_swing2_stage3_parallel_v2.py` (4h reference template)

**Files:**
- Source: `optimization/wave2/run_swing2_stage2_parallel_v2.py`
- Create: `optimization/wave3/run_swing2_stage3_parallel_v2.py`

The only difference from the 1h template (Task 2) is `HOME_TF = "4h"` and `TF_MAP` covers 15m/1h/12h instead of 15m/4h/12h.

- [ ] **Step 1: Copy Stage 2 script**

```powershell
Copy-Item optimization/wave2/run_swing2_stage2_parallel_v2.py `
          optimization/wave3/run_swing2_stage3_parallel_v2.py
```

- [ ] **Step 2–7: Apply same transformation as Task 2 with these values**

```python
STRATEGY_ID  = "SWING2"
STRATEGY_KEY = "swing2_bb_squeeze"
HOME_TF      = "4h"

TF_MAP = {
    "15m": "M15",
    "1h":  "H1",
    "12h": "H12",
}

TF_FREQ_MAP = {
    "15m": "15min",
    "1h":  "1h",
    "12h": "12h",
}
```

- [ ] **Step 3: Verify clean import**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "import run_swing2_stage3_parallel_v2; print('Import OK')"
```

- [ ] **Step 4: Commit**

```powershell
git add optimization/wave3/run_swing2_stage3_parallel_v2.py
git commit -m "feat: SWING2 Stage 3 — DOW filter script (15m, 1h, 12h)"
```

---

## Task 5: Create remaining 4h home TF scripts (SWING4, DC1, AGGR_PULLBACK, MO1)

Same transformation as Task 4. `HOME_TF = "4h"`, `TF_MAP = {"15m": "M15", "1h": "H1", "12h": "H12"}`, `TF_FREQ_MAP = {"15m": "15min", "1h": "1h", "12h": "12h"}` for all four.

| Script | STRATEGY_ID | STRATEGY_KEY | Source |
|---|---|---|---|
| run_swing4_stage3_parallel_v2.py | "SWING4" | "swing4_macd_divergence" | run_swing4_stage2_parallel_v2.py |
| run_dc1_stage3_parallel_v2.py | "DC1" | "dc1_donchian_channel" | run_dc1_stage2_parallel_v2.py |
| run_aggr_pullback_stage3_parallel_v2.py | "AGGR_PULLBACK" | "aggr_pullback" | run_aggr_pullback_stage2_parallel_v2.py |
| run_mo1_stage3_parallel_v2.py | "MO1" | "mo1_momentum_rotation" | run_mo1_stage2_parallel_v2.py |

**SWING4 note:** SWING4 uses `numba` (`@numba.njit` for `_detect_divergence`) — keep the `import numba` line.

- [ ] **Copy and patch each script (4 separate commits)**

```powershell
foreach ($s in @("swing4","dc1","aggr_pullback","mo1")) {
    Copy-Item "optimization/wave2/run_${s}_stage2_parallel_v2.py" `
              "optimization/wave3/run_${s}_stage3_parallel_v2.py"
}
```

Apply Task 2 steps 2–7 to each, using the strategy-specific values from the table above.

```powershell
git add optimization/wave3/run_swing4_stage3_parallel_v2.py
git commit -m "feat: SWING4 Stage 3 — DOW filter script"

git add optimization/wave3/run_dc1_stage3_parallel_v2.py
git commit -m "feat: DC1 Stage 3 — DOW filter script"

git add optimization/wave3/run_aggr_pullback_stage3_parallel_v2.py
git commit -m "feat: AGGR_PULLBACK Stage 3 — DOW filter script"

git add optimization/wave3/run_mo1_stage3_parallel_v2.py
git commit -m "feat: MO1 Stage 3 — DOW filter script"
```

- [ ] **Verify all 4 import cleanly**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "
import run_swing4_stage3_parallel_v2
import run_dc1_stage3_parallel_v2
import run_aggr_pullback_stage3_parallel_v2
import run_mo1_stage3_parallel_v2
print('All 4 import OK')
"
```

Expected: `All 4 import OK`

---

## Task 6: Create `generate_stage3_summary.py`

**Files:**
- Create: `optimization/wave3/generate_stage3_summary.py`

- [ ] **Step 1: Create the file**

Create `optimization/wave3/generate_stage3_summary.py`:

```python
#!/usr/bin/env python3
"""
Generate Stage 3 summary markdown for a completed DOW-filter run.

Usage:
    python generate_stage3_summary.py <STRATEGY_ID>
    python generate_stage3_summary.py ALL
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")

STRATEGY_META = {
    "SWING2":        {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING3":        {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING4":        {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING5":        {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "EMA_REJ_V1":    {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "DC1":           {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VR1":           {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "AGGR_PULLBACK": {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "MO1":           {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VP1":           {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
}

DOW_MASK_ORDER = ["ALL", "MON-FRI", "SAT-SUN", "MON", "TUE", "WED", "THU", "FRI"]


def load_results(strategy_id):
    stage3_dir = RESULTS_BASE / strategy_id / "stage3"
    results = []
    if not stage3_dir.exists():
        return results
    for fpath in stage3_dir.glob("*_dow.json"):
        try:
            results.append(json.loads(fpath.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
    return results


def generate_summary(strategy_id):
    meta    = STRATEGY_META[strategy_id]
    results = load_results(strategy_id)

    done     = len(results)
    improved = [r for r in results if r.get("dow_improved") is True]
    n_improved = len(improved)
    pct_improved = f"{100*n_improved/done:.1f}%" if done > 0 else "0%"

    # Winner mask distribution
    winner_counts = Counter(r.get("winner_mask", "ALL") for r in results)

    # Sort by winner_sharpe descending
    ranked = sorted(
        [r for r in results if r.get("winner_sharpe") is not None],
        key=lambda r: r.get("winner_sharpe") or 0,
        reverse=True,
    )

    lines = []
    lines.append(f"# {strategy_id} — Stage 3 Summary "
                 f"(home TF: {meta['home_tf'].upper()})")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Combos processed:** {done}")
    lines.append(f"**DOW improvement rate:** {n_improved} / {done} ({pct_improved}) "
                 f"— combos where a DOW mask beat ALL by ≥ 0.10 Sharpe with ≥ 20 trades")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Winner Mask Distribution")
    lines.append("")
    lines.append("| Mask | Times Won | % of Combos |")
    lines.append("|---|---|---|")
    for mask in DOW_MASK_ORDER:
        count = winner_counts.get(mask, 0)
        pct   = f"{100*count/done:.1f}%" if done > 0 else "0%"
        lines.append(f"| {mask} | {count} | {pct} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Top Combos (ranked by Winner Sharpe)")
    lines.append("")
    if ranked:
        lines.append("| Symbol | Off-TF | Direction | SL | Winner Mask | "
                     "Winner Sharpe | Stage2 Sharpe | OOS Trades | DOW Improved |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in ranked:
            params_str = json.dumps(r.get("best_params") or {})
            if len(params_str) > 60:
                params_str = params_str[:57] + "..."
            lines.append(
                f"| {r.get('symbol','?')} "
                f"| {r.get('timeframe','?')} "
                f"| {r.get('direction','?')} "
                f"| {r.get('sl_type','?')} "
                f"| {r.get('winner_mask','?')} "
                f"| {r.get('winner_sharpe','N/A')} "
                f"| {r.get('stage2_oos_sharpe','N/A')} "
                f"| {r.get('winner_trades','?')} "
                f"| {'✅' if r.get('dow_improved') else '➖'} |"
            )
    else:
        lines.append("_No Stage 3 results yet._")

    lines.append("")
    lines.append(f"**Stage 3 DOW improvement rate: {n_improved} / {done}**")
    lines.append("")

    out_dir = RESULTS_BASE / "stage3_summarized"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{strategy_id}_stage3_summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  DOW improved: {n_improved}/{done}  improved rate: {pct_improved}")
    return n_improved, done


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <STRATEGY_ID | ALL>")
        print(f"Strategies: {list(STRATEGY_META.keys())}")
        sys.exit(1)

    arg = sys.argv[1].upper()

    if arg == "ALL":
        targets = list(STRATEGY_META.keys())
    elif arg in STRATEGY_META:
        targets = [arg]
    else:
        print(f"Unknown strategy '{arg}'. Options: {list(STRATEGY_META.keys())} or ALL")
        sys.exit(1)

    total_improved = total_done = 0
    for sid in targets:
        print(f"\n-- {sid} --")
        i, d = generate_summary(sid)
        total_improved += i
        total_done     += d

    if len(targets) > 1:
        print(f"\n{'='*50}")
        pct = f"{100*total_improved/total_done:.1f}%" if total_done > 0 else "0%"
        print(f"ALL strategies Stage 3 — DOW improved: {total_improved}/{total_done} ({pct})")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with empty stage3 dirs**

```powershell
cd optimization/wave3
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" generate_stage3_summary.py SWING3
```

Expected output (no stage3 results yet):
```
-- SWING3 --
Written: ...results\stage3_summarized\SWING3_stage3_summary.md
  DOW improved: 0/0  improved rate: 0%
```

Then test ALL:
```powershell
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" generate_stage3_summary.py ALL
```

Expected: 10 "Written:" lines, no crashes.

- [ ] **Step 3: Commit**

```powershell
git add optimization/wave3/generate_stage3_summary.py
git commit -m "feat: generate_stage3_summary — DOW improvement rate, mask distribution, ranked combos"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ `optimization/wave3/` file structure (spec §5)
- ✅ `stage3_utils.py` exports `DOW_MASKS`, `MIN_TRADES`, `MIN_LIFT`, `load_stage2_passing`, `select_winner`, `run_stage3_parallel` (spec §6)
- ✅ 10 strategy scripts, same set as Stage 2 (spec §2)
- ✅ DOW masking applied only to entries (`le`/`se`), exits unchanged (spec §3)
- ✅ Winner rule: strictly > ALL + 0.10, ≥20 trades; defaults to ALL (spec §4)
- ✅ JSON output has `dow_results`, `winner_mask`, `winner_sharpe`, `winner_trades`, `dow_improved`, `stage2_oos_sharpe` (spec §8)
- ✅ `generate_stage3_summary.py` writes to `stage3_summarized/`, includes mask distribution + ranked combos (spec §9)
- ✅ EMA_REJ_V1 `HTF_BARS_MAP` preserved from Stage 2 (spec §7)

**Placeholder scan:** None found.

**Type consistency:** `select_winner` returns `(str, float|None, int, bool)` — consumed correctly in `_worker_v2` as `winner_mask, winner_sharpe, winner_trades, dow_improved = select_winner(dow_results)`. Task dict keys (`sym`, `tf`, `direction`, `sl_type`, `best_params`, `stage2_oos_sharpe`) match across `run_stage3_parallel`, `_worker_v2`.
