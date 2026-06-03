# Stage 4 Summary & Robustness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run ±10% parameter sensitivity analysis on 1,943 Stage 3 passing combos (winner_sharpe ≥ 0.5), write a SUMMARY.md per strategy, and append a Wave 1 results table to BACKTEST-ROADMAP.md.

**Architecture:** Approach A — `stage4_utils.py` owns Stage 3 loading, param nudging, parallel dispatch, and JSON I/O. Each of 10 per-strategy scripts copies indicator functions + `_eval_single_dow` from its Stage 3 counterpart and adds a sensitivity loop over param nudges. `generate_stage4_summary.py` reads stage4 JSONs and writes SUMMARY.md + updates BACKTEST-ROADMAP.md.

**Tech Stack:** Python 3.x, vectorbt, `ProcessPoolExecutor`, BacktestingMCP engine; `DOW_MASKS` imported from `stage3_utils` by sensitivity scripts.

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `optimization/wave4/stage4_utils.py` | Create | Stage 3 loading, `nudge_params`, executor, JSON I/O |
| `optimization/wave4/tests/__init__.py` | Create | Package marker |
| `optimization/wave4/tests/test_stage4_utils.py` | Create | Unit tests for utils |
| `optimization/wave4/run_swing3_stage4_sensitivity.py` | Create | SWING3 — 1h reference |
| `optimization/wave4/run_swing5_stage4_sensitivity.py` | Create | SWING5 — 1h |
| `optimization/wave4/run_ema_rej_v1_stage4_sensitivity.py` | Create | EMA_REJ_V1 — 1h |
| `optimization/wave4/run_vr1_stage4_sensitivity.py` | Create | VR1 — 1h |
| `optimization/wave4/run_vp1_stage4_sensitivity.py` | Create | VP1 — 1h |
| `optimization/wave4/run_swing2_stage4_sensitivity.py` | Create | SWING2 — 4h reference |
| `optimization/wave4/run_swing4_stage4_sensitivity.py` | Create | SWING4 — 4h |
| `optimization/wave4/run_dc1_stage4_sensitivity.py` | Create | DC1 — 4h |
| `optimization/wave4/run_aggr_pullback_stage4_sensitivity.py` | Create | AGGR_PULLBACK — 4h |
| `optimization/wave4/run_mo1_stage4_sensitivity.py` | Create | MO1 — 4h |
| `optimization/wave4/generate_stage4_summary.py` | Create | SUMMARY.md + BACKTEST-ROADMAP.md update |

---

## Task 1: Create `stage4_utils.py` with unit tests

**Files:**
- Create: `optimization/wave4/stage4_utils.py`
- Create: `optimization/wave4/tests/__init__.py`
- Create: `optimization/wave4/tests/test_stage4_utils.py`

- [ ] **Step 1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force "optimization/wave4/tests"
```

- [ ] **Step 2: Write failing tests**

Create `optimization/wave4/tests/test_stage4_utils.py`:

```python
# Run with: python -m pytest tests/test_stage4_utils.py -v
# Requires: BacktestingMCP venv which has pytest
import json
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from stage4_utils import nudge_params, load_stage3_passing, SENSITIVITY_FILTER


def _write_stage3_json(base, strategy_id, symbol, tf, direction, sl_type,
                       winner_sharpe, winner_mask="ALL", best_params=None):
    d = base / strategy_id / "stage3"
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": symbol, "timeframe": tf, "direction": direction,
        "sl_type": sl_type, "winner_sharpe": winner_sharpe,
        "winner_mask": winner_mask, "winner_trades": 30,
        "stage2_oos_sharpe": 0.6,
        "best_params": best_params or {"p": 1},
    }
    (d / f"{symbol}_{tf}_{direction}_{sl_type}_dow.json").write_text(json.dumps(payload))


# ── nudge_params ──────────────────────────────────────────────────────────────

def test_nudge_params_floats_up():
    result = nudge_params({"st_factor": 2.0}, 1.1)
    assert result["st_factor"] == pytest.approx(2.2, rel=1e-4)


def test_nudge_params_floats_down():
    result = nudge_params({"st_factor": 2.0}, 0.9)
    assert result["st_factor"] == pytest.approx(1.8, rel=1e-4)


def test_nudge_params_integers_up():
    result = nudge_params({"st_period": 10}, 1.1)
    assert result["st_period"] == 11
    assert isinstance(result["st_period"], int)


def test_nudge_params_integers_down():
    result = nudge_params({"st_period": 10}, 0.9)
    assert result["st_period"] == 9
    assert isinstance(result["st_period"], int)


def test_nudge_params_integer_minimum_one():
    result = nudge_params({"st_period": 1}, 0.9)
    assert result["st_period"] == 1   # max(1, round(0.9)) = 1


def test_nudge_params_skips_direction_key():
    result = nudge_params({"st_period": 10, "direction": "long"}, 1.1)
    assert result["direction"] == "long"   # unchanged
    assert result["st_period"] == 11


def test_nudge_params_skips_string_values():
    result = nudge_params({"mode": "fast", "period": 5}, 1.1)
    assert result["mode"] == "fast"        # unchanged
    assert result["period"] == 6


def test_nudge_params_skips_bool_values():
    # bool is a subclass of int in Python — must be excluded explicitly
    result = nudge_params({"use_filter": True, "period": 10}, 1.1)
    assert result["use_filter"] is True    # unchanged
    assert result["period"] == 11


def test_nudge_params_does_not_mutate_input():
    original = {"st_period": 10}
    nudge_params(original, 1.1)
    assert original["st_period"] == 10


# ── load_stage3_passing ────────────────────────────────────────────────────────

def test_load_stage3_passing_filters_by_sharpe():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage3_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr", winner_sharpe=0.8)
        _write_stage3_json(tmp, "SWING3", "ETHUSDT", "4h", "long", "embedded", winner_sharpe=0.3)
        result = load_stage3_passing("SWING3", tmp, sharpe_threshold=0.5)
        syms = [r["symbol"] for r in result]
        assert "BTCUSDT" in syms
        assert "ETHUSDT" not in syms


def test_load_stage3_passing_includes_all_required_keys():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage3_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr",
                           winner_sharpe=0.9, winner_mask="MON-FRI",
                           best_params={"st_period": 10})
        result = load_stage3_passing("SWING3", tmp)
        assert len(result) == 1
        r = result[0]
        for key in ("symbol","timeframe","direction","sl_type","best_params",
                    "winner_mask","winner_sharpe","winner_trades","stage2_oos_sharpe"):
            assert key in r, f"Missing key: {key}"


def test_load_stage3_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_stage3_passing("NONEXISTENT", Path(tmp))
        assert result == []


def test_load_stage3_passing_skips_none_winner_sharpe():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d = tmp / "SWING3" / "stage3"
        d.mkdir(parents=True)
        payload = {"symbol": "BTCUSDT", "timeframe": "4h", "direction": "both",
                   "sl_type": "atr", "winner_sharpe": None, "winner_mask": "ALL",
                   "winner_trades": 30, "stage2_oos_sharpe": 0.5, "best_params": {}}
        (d / "BTCUSDT_4h_both_atr_dow.json").write_text(json.dumps(payload))
        result = load_stage3_passing("SWING3", tmp)
        assert result == []


def test_sensitivity_filter_default():
    assert SENSITIVITY_FILTER == 0.5
```

- [ ] **Step 3: Run to confirm tests fail**

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -m pytest tests/test_stage4_utils.py -v
```

Expected: `ModuleNotFoundError: No module named 'stage4_utils'`

- [ ] **Step 4: Implement `stage4_utils.py`**

Create `optimization/wave4/stage4_utils.py`:

```python
#!/usr/bin/env python3
"""
Shared machinery for Stage 4 sensitivity analysis scripts.

Exports:
    SENSITIVITY_FILTER  — minimum Stage 3 winner_sharpe to analyse (0.5)
    nudge_params(best_params, factor) -> dict
    load_stage3_passing(strategy_id, results_base, sharpe_threshold) -> list[dict]
    run_sensitivity_parallel(strategy_id, results_base, worker_fn,
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

SENSITIVITY_FILTER = 0.5

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


def nudge_params(best_params: dict, factor: float) -> dict:
    """
    Return a copy of best_params with all numeric (non-bool, non-string) values
    nudged by factor. Skips the "direction" key and any bool/string values.
    Integers are rounded and clamped to minimum 1.
    """
    result = {}
    for k, v in best_params.items():
        if k == "direction" or isinstance(v, bool) or isinstance(v, str):
            result[k] = v
        elif isinstance(v, int):
            result[k] = max(1, round(v * factor))
        elif isinstance(v, float):
            result[k] = round(v * factor, 4)
        else:
            result[k] = v
    return result


def load_stage3_passing(
    strategy_id: str,
    results_base: Path,
    sharpe_threshold: float = SENSITIVITY_FILTER,
) -> list:
    """
    Return list of dicts for Stage 3 results where winner_sharpe >= sharpe_threshold.
    Reads *_dow.json files from results/{strategy_id}/stage3/.
    """
    stage3_dir = results_base / strategy_id / "stage3"
    passing = []
    if not stage3_dir.exists():
        return passing
    for fpath in stage3_dir.glob("*_dow.json"):
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
            continue
        ws = data.get("winner_sharpe")
        if ws is None or ws < sharpe_threshold:
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
            "winner_mask":       data.get("winner_mask", "ALL"),
            "winner_sharpe":     ws,
            "winner_trades":     data.get("winner_trades", 0),
            "stage2_oos_sharpe": data.get("stage2_oos_sharpe"),
        })
    return passing


def _predownload(strategy_id: str, results_base: Path, backtesting_mcp: Path) -> None:
    """Download unique TFs present in Stage 3 passing combos for this strategy."""
    passing = load_stage3_passing(strategy_id, results_base)
    if not passing:
        return
    tfs  = sorted({c["timeframe"] for c in passing})
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


def run_sensitivity_parallel(
    strategy_id: str,
    results_base: Path,
    worker_fn: Callable,
    backtesting_mcp: Path,
    workers: Optional[int] = None,
    skip_download: bool = False,
) -> None:
    if workers is None:
        workers = max(1, (os.cpu_count() or 4) - 2)

    stage4_dir = results_base / strategy_id / "stage4"
    stage4_dir.mkdir(parents=True, exist_ok=True)

    if not skip_download:
        _predownload(strategy_id, results_base, backtesting_mcp)

    passing = load_stage3_passing(strategy_id, results_base)
    print(f"\n{strategy_id} Stage 4 — {len(passing)} combos (winner_sharpe >= {SENSITIVITY_FILTER})")

    all_tasks, done = [], 0
    for combo in passing:
        sym       = combo["symbol"].replace("USDT", "")
        tf        = combo["timeframe"]
        direction = combo["direction"]
        sl_type   = combo["sl_type"]
        fname = f"{combo['symbol']}_{tf}_{direction}_{sl_type}_sensitivity.json"
        fpath = stage4_dir / fname
        if fpath.exists():
            try:
                note = str(json.loads(fpath.read_text(encoding="utf-8")).get("note", ""))
                if not any(e in note for e in ("WORKER CRASH", "SENSITIVITY ERROR", "DATA ERROR")):
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
            "winner_mask":       combo["winner_mask"],
            "winner_sharpe":     combo["winner_sharpe"],
            "winner_trades":     combo["winner_trades"],
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
                            "best_params":       task["best_params"],
                            "winner_mask":       task["winner_mask"],
                            "winner_sharpe":     task["winner_sharpe"],
                            "winner_trades":     task["winner_trades"],
                            "stage2_oos_sharpe": task["stage2_oos_sharpe"],
                            "sensitivity":       {},
                            "robust":            False,
                            "note":              f"WORKER CRASH: {e}",
                        }

                    sym_usdt  = result.get("symbol", "?")
                    tf_r      = result.get("timeframe", "?")
                    direction = result.get("direction", "?")
                    sl_type   = result.get("sl_type", "?")
                    robust    = result.get("robust", False)

                    fname = f"{sym_usdt}_{tf_r}_{direction}_{sl_type}_sensitivity.json"
                    (stage4_dir / fname).write_text(
                        json.dumps(result, indent=2, cls=_NumpyEncoder),
                        encoding="utf-8",
                    )
                    done += 1
                    print(
                        f"[{done}/{total}] {sym_usdt} {tf_r} {direction} {sl_type}"
                        f" → robust={robust}",
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

    print(f"\n{strategy_id} Stage 4 complete")
```

- [ ] **Step 5: Run tests — confirm all pass**

```powershell
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -m pytest tests/test_stage4_utils.py -v
```

Expected: `15 passed`

- [ ] **Step 6: Commit**

```powershell
git add optimization/wave4/stage4_utils.py optimization/wave4/tests/
git commit -m "feat: stage4_utils — Stage 3 loading, param nudging, sensitivity executor"
```

---

## Task 2: Create `run_swing3_stage4_sensitivity.py` (1h reference template)

**Files:**
- Source: `optimization/wave3/run_swing3_stage3_parallel_v2.py`
- Create: `optimization/wave4/run_swing3_stage4_sensitivity.py`

- [ ] **Step 1: Copy Stage 3 script**

```powershell
Copy-Item optimization/wave3/run_swing3_stage3_parallel_v2.py `
          optimization/wave4/run_swing3_stage4_sensitivity.py
```

- [ ] **Step 2: Replace header and imports**

Replace the opening docstring + import block with:

```python
"""
SWING3 Stage 4 — parameter sensitivity analysis (PARALLEL).

Nudges each numeric param in best_params ±10% and re-evaluates OOS Sharpe
with the Stage 3 winner DOW mask applied. Flags combos where any nudge
drops Sharpe by >20% (sensitive). Robust = no param is sensitive.

Usage:
    python run_swing3_stage4_sensitivity.py
    python run_swing3_stage4_sensitivity.py --workers 8
    python run_swing3_stage4_sensitivity.py --skip-download
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage4_utils import run_sensitivity_parallel, nudge_params, SENSITIVITY_FILTER

# DOW_MASKS needed to convert winner_mask string → day set for _eval_single_dow
import sys as _sys; _sys.path.insert(0, str(Path(__file__).parent.parent / "wave3"))
from stage3_utils import DOW_MASKS
```

- [ ] **Step 3: Update constants block**

Replace with:

```python
STRATEGY_ID  = "SWING3"
STRATEGY_KEY = "swing3_supertrend_adx"
RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
V2_NOTE      = "v2/vectorbt"

TF_MAP = {
    "15m": "M15",
    "4h":  "H4",
    "12h": "H12",
}

# Vectorbt freq strings for Sharpe annualization
TF_FREQ_MAP = {
    "15m": "15min",
    "4h":  "4h",
    "12h": "12h",
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"
```

- [ ] **Step 4: Delete functions not needed in Stage 4**

Delete entirely:
- `select_winner` import reference (use `nudge_params` instead)
- `DOW_MASKS` if re-declared (it's imported from stage3_utils above)
- `_build_sl_params_list` (not present in Stage 3 copy, but double-check)
- `_optimize_vbt` (not present in Stage 3 copy)

Keep unchanged:
- `_supertrend_loop`, `_compute_supertrend`, `_compute_adx`, `_compute_ema`, `_make_signals`, `_extract_pf_stats`, `_run_vbt_portfolio`, `_eval_single_dow`

- [ ] **Step 5: Replace `_worker_v2` entirely**

```python
def _worker_v2(task):
    """
    Stage 4 worker. One process per Stage 3 passing combo.
    Nudges each numeric param ±10% and measures Sharpe impact
    using the Stage 3 winner DOW mask.
    task = {"sym","tf","direction","sl_type","best_params",
            "winner_mask","winner_sharpe","winner_trades","stage2_oos_sharpe"}
    """
    sym               = task["sym"]
    tf                = task["tf"]
    direction         = task["direction"]
    sl_type           = task["sl_type"]
    best_params       = task["best_params"]
    winner_mask       = task["winner_mask"]
    winner_sharpe     = task["winner_sharpe"]
    winner_trades     = task["winner_trades"]
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
    dow_days    = DOW_MASKS[winner_mask]

    _error_result = lambda msg: {
        "strategy": STRATEGY_KEY, "symbol": symbol_usdt,
        "timeframe": tf, "direction": direction, "sl_type": sl_type,
        "stage": 4, "best_params": best_params,
        "winner_mask": winner_mask, "winner_sharpe": winner_sharpe,
        "winner_trades": winner_trades, "stage2_oos_sharpe": stage2_oos_sharpe,
        "sensitivity": {}, "robust": False, "note": msg,
    }

    print(f"{log_prefix} loading data...", flush=True)
    try:
        data = engine.get_data(symbol_usdt, tf_enum,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        print(f"{log_prefix} DATA ERROR: {e}", flush=True)
        return _error_result(f"DATA ERROR: {e}")

    if data.empty or len(data) < 500:
        return _error_result("insufficient data")

    test_data = data.iloc[int(len(data) * 0.7):]

    # Compute indicators once — nudges only affect SL/TP params passed to _eval_single_dow
    h_t, l_t, c_t = test_data.High.values, test_data.Low.values, test_data.Close.values
    close_s_t = pd.Series(c_t, index=test_data.index)
    try:
        st_dir_t, _, atr_t = _compute_supertrend(h_t, l_t, c_t,
                                                  best_params["st_period"],
                                                  best_params["st_factor"])
        adx_t = _compute_adx(h_t, l_t, c_t)
        ema_t = _compute_ema(c_t, best_params["ema_filter"])
        le_t, lx_t, se_t, sx_t = _make_signals(st_dir_t, adx_t, ema_t, c_t,
                                                 best_params["adx_threshold"], direction)
    except Exception as e:
        print(f"{log_prefix} INDICATOR ERROR: {e}", flush=True)
        return _error_result(f"INDICATOR ERROR: {e}")

    print(f"{log_prefix} running sensitivity ({len(test_data)} OOS bars)...", flush=True)
    sensitivity = {}
    for param_name, param_value in best_params.items():
        if (param_name == "direction"
                or isinstance(param_value, bool)
                or isinstance(param_value, str)
                or not isinstance(param_value, (int, float))):
            continue

        param_results = {}
        for label, factor in [("up", 1.1), ("down", 0.9)]:
            nudged = nudge_params(best_params, factor)
            sharpe, trades = _eval_single_dow(
                close_s_t, le_t, lx_t, se_t, sx_t, atr_t,
                sl_type, nudged, dow_days=dow_days, freq=TF_FREQ_MAP[tf],
            )
            param_results[label] = {"sharpe": sharpe, "trades": trades}

        # Sensitive if any valid nudge drops Sharpe >20% below winner
        sensitive = (
            winner_sharpe > 0 and any(
                v["sharpe"] is not None and v["sharpe"] < winner_sharpe * 0.8
                for v in param_results.values()
            )
        )
        param_results["sensitive"] = sensitive
        sensitivity[param_name] = param_results

    robust = bool(sensitivity) and not any(
        v["sensitive"] for v in sensitivity.values()
    )
    print(f"{log_prefix} robust={robust} params_tested={len(sensitivity)}", flush=True)

    return {
        "strategy":          STRATEGY_KEY,
        "symbol":            symbol_usdt,
        "timeframe":         tf,
        "direction":         direction,
        "sl_type":           sl_type,
        "stage":             4,
        "best_params":       best_params,
        "winner_mask":       winner_mask,
        "winner_sharpe":     winner_sharpe,
        "winner_trades":     winner_trades,
        "stage2_oos_sharpe": stage2_oos_sharpe,
        "sensitivity":       sensitivity,
        "robust":            robust,
        "note":              note,
    }
```

- [ ] **Step 6: Replace `main()`**

```python
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="SWING3 Stage 4 — parameter sensitivity (15m, 4h, 12h off-TFs)")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    run_sensitivity_parallel(
        strategy_id    = STRATEGY_ID,
        results_base   = RESULTS_BASE,
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

- [ ] **Step 7: Verify clean import**

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "import run_swing3_stage4_sensitivity; print('Import OK')"
```

Expected: `Import OK`

- [ ] **Step 8: Commit**

```powershell
git add optimization/wave4/run_swing3_stage4_sensitivity.py
git commit -m "feat: SWING3 Stage 4 — parameter sensitivity script"
```

---

## Task 3: Create remaining 1h home TF scripts (SWING5, EMA_REJ_V1, VR1, VP1)

Each follows the identical transformation as Task 2. For each script:
1. Copy from Stage 3 counterpart in `optimization/wave3/`
2. Apply all changes from Task 2 (steps 2–6)

**Strategy-specific values:**

| Script | STRATEGY_ID | STRATEGY_KEY | Stage 3 source |
|---|---|---|---|
| run_swing5_stage4_sensitivity.py | "SWING5" | "swing5_keltner_breakout" | run_swing5_stage3_parallel_v2.py |
| run_ema_rej_v1_stage4_sensitivity.py | "EMA_REJ_V1" | "ema_rejection_v1" | run_ema_rej_v1_stage3_parallel_v2.py |
| run_vr1_stage4_sensitivity.py | "VR1" | "vr1_vwap_mean_reversion" | run_vr1_stage3_parallel_v2.py |
| run_vp1_stage4_sensitivity.py | "VP1" | "vp1_volume_profile_breakout" | run_vp1_stage3_parallel_v2.py |

All use `TF_MAP = {"15m":"M15","4h":"H4","12h":"H12"}` and `TF_FREQ_MAP = {"15m":"15min","4h":"4h","12h":"12h"}`.

**EMA_REJ_V1 special case:** Its `_worker_v2` must compute `htf_bars = HTF_BARS_MAP[tf]` before indicators and pass it to `_eval_single_dow`. The sensitivity loop calls `_eval_single_dow(close_s_t, le_t, lx_t, se_t, sx_t, atr_t, sl_type, nudged, atr_t, htf_bars=htf_bars, dow_days=dow_days, freq=TF_FREQ_MAP[tf])`. `HTF_BARS_MAP = {"15m":36,"4h":2,"12h":1}` is kept from Stage 3.

**SWING5, VR1, VP1 embedded SL inline:** These strategies handle `embedded` SL inline in `_worker_v2` rather than through `_eval_single_dow` because they require extra precomputed arrays (ema_t for SWING5, vwap_t for VR1, poc_t for VP1). The sensitivity loop for `embedded` must also be handled inline — apply nudge to `best_params`, recompute the embedded SL arrays, run vbt. For `fixed_pct`, `fixed_signal`, `atr` sl_types, call `_eval_single_dow` as normal.

- [ ] **Copy and patch each script**

```powershell
foreach ($s in @("swing5","ema_rej_v1","vr1","vp1")) {
    Copy-Item "optimization/wave3/run_${s}_stage3_parallel_v2.py" `
              "optimization/wave4/run_${s}_stage4_sensitivity.py"
}
```

Apply Task 2 transformation to each. Commit each separately:

```powershell
git add optimization/wave4/run_swing5_stage4_sensitivity.py
git commit -m "feat: SWING5 Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_ema_rej_v1_stage4_sensitivity.py
git commit -m "feat: EMA_REJ_V1 Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_vr1_stage4_sensitivity.py
git commit -m "feat: VR1 Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_vp1_stage4_sensitivity.py
git commit -m "feat: VP1 Stage 4 — parameter sensitivity script"
```

- [ ] **Verify all 4 import cleanly**

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "
import run_swing5_stage4_sensitivity
import run_ema_rej_v1_stage4_sensitivity
import run_vr1_stage4_sensitivity
import run_vp1_stage4_sensitivity
print('All 4 import OK')
"
```

---

## Task 4: Create `run_swing2_stage4_sensitivity.py` (4h reference template)

**Files:**
- Source: `optimization/wave3/run_swing2_stage3_parallel_v2.py`
- Create: `optimization/wave4/run_swing2_stage4_sensitivity.py`

Apply the same transformation as Task 2 with:

```python
STRATEGY_ID  = "SWING2"
STRATEGY_KEY = "swing2_bb_squeeze"

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

- [ ] **Copy, patch, verify, commit**

```powershell
Copy-Item optimization/wave3/run_swing2_stage3_parallel_v2.py `
          optimization/wave4/run_swing2_stage4_sensitivity.py
```

Apply transformation. Verify:

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "import run_swing2_stage4_sensitivity; print('Import OK')"
```

```powershell
git add optimization/wave4/run_swing2_stage4_sensitivity.py
git commit -m "feat: SWING2 Stage 4 — parameter sensitivity script (15m, 1h, 12h)"
```

---

## Task 5: Create remaining 4h home TF scripts (SWING4, DC1, AGGR_PULLBACK, MO1)

Same transformation as Task 4. `TF_MAP = {"15m":"M15","1h":"H1","12h":"H12"}` for all four.

| Script | STRATEGY_ID | STRATEGY_KEY | Stage 3 source |
|---|---|---|---|
| run_swing4_stage4_sensitivity.py | "SWING4" | "swing4_macd_divergence" | run_swing4_stage3_parallel_v2.py |
| run_dc1_stage4_sensitivity.py | "DC1" | "dc1_donchian_channel" | run_dc1_stage3_parallel_v2.py |
| run_aggr_pullback_stage4_sensitivity.py | "AGGR_PULLBACK" | "aggr_pullback" | run_aggr_pullback_stage3_parallel_v2.py |
| run_mo1_stage4_sensitivity.py | "MO1" | "mo1_momentum_rotation" | run_mo1_stage3_parallel_v2.py |

SWING4 keeps `import numba` (used by `@numba.njit _detect_divergence`).

- [ ] **Copy, patch, commit each**

```powershell
foreach ($s in @("swing4","dc1","aggr_pullback","mo1")) {
    Copy-Item "optimization/wave3/run_${s}_stage3_parallel_v2.py" `
              "optimization/wave4/run_${s}_stage4_sensitivity.py"
}
```

```powershell
git add optimization/wave4/run_swing4_stage4_sensitivity.py
git commit -m "feat: SWING4 Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_dc1_stage4_sensitivity.py
git commit -m "feat: DC1 Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_aggr_pullback_stage4_sensitivity.py
git commit -m "feat: AGGR_PULLBACK Stage 4 — parameter sensitivity script"

git add optimization/wave4/run_mo1_stage4_sensitivity.py
git commit -m "feat: MO1 Stage 4 — parameter sensitivity script"
```

- [ ] **Verify all 4 import cleanly**

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" -c "
import run_swing4_stage4_sensitivity
import run_dc1_stage4_sensitivity
import run_aggr_pullback_stage4_sensitivity
import run_mo1_stage4_sensitivity
print('All 4 import OK')
"
```

---

## Task 6: Create `generate_stage4_summary.py`

**Files:**
- Create: `optimization/wave4/generate_stage4_summary.py`

- [ ] **Step 1: Create the file**

Create `optimization/wave4/generate_stage4_summary.py`:

```python
#!/usr/bin/env python3
"""
Generate Stage 4 SUMMARY.md per strategy and update BACKTEST-ROADMAP.md.

Usage:
    python generate_stage4_summary.py <STRATEGY_ID>
    python generate_stage4_summary.py ALL
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

RESULTS_BASE   = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
ROADMAP_PATH   = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\BACKTEST-ROADMAP.md")
ROADMAP_MARKER = "## Wave 1 — Optimization Results"

STRATEGY_META = {
    "SWING2":        {"home_tf": "4h"},
    "SWING3":        {"home_tf": "1h"},
    "SWING4":        {"home_tf": "4h"},
    "SWING5":        {"home_tf": "1h"},
    "EMA_REJ_V1":    {"home_tf": "1h"},
    "DC1":           {"home_tf": "4h"},
    "VR1":           {"home_tf": "1h"},
    "AGGR_PULLBACK": {"home_tf": "4h"},
    "MO1":           {"home_tf": "4h"},
    "VP1":           {"home_tf": "1h"},
}


def _load_summary_line(summary_md_path: Path, pattern: str) -> str:
    """Extract a value from a stage summary md file matching a line pattern."""
    if not summary_md_path.exists():
        return "?"
    for line in summary_md_path.read_text(encoding="utf-8").splitlines():
        if pattern in line:
            # Extract the last number-like token
            parts = line.split()
            for part in reversed(parts):
                p = part.rstrip(".")
                if "/" in p:
                    return p
                try:
                    float(p.strip("()*%"))
                    return p
                except ValueError:
                    continue
    return "?"


def load_sensitivity_results(strategy_id: str) -> list:
    stage4_dir = RESULTS_BASE / strategy_id / "stage4"
    results = []
    if not stage4_dir.exists():
        return results
    for fpath in stage4_dir.glob("*_sensitivity.json"):
        try:
            results.append(json.loads(fpath.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
    return results


def generate_summary(strategy_id: str) -> tuple:
    """Write SUMMARY.md for strategy. Returns (n_robust, n_total)."""
    meta    = STRATEGY_META[strategy_id]
    results = load_sensitivity_results(strategy_id)

    n_total  = len(results)
    n_robust = sum(1 for r in results if r.get("robust") is True)
    pct      = f"{100*n_robust/n_total:.1f}%" if n_total > 0 else "0%"

    ranked = sorted(
        [r for r in results if r.get("winner_sharpe") is not None],
        key=lambda r: r.get("winner_sharpe") or 0,
        reverse=True,
    )

    lines = []
    lines.append(f"# {strategy_id} — Summary (home TF: {meta['home_tf'].upper()})")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Combos analysed:** {n_total}")
    lines.append(f"**Robust:** {n_robust} / {n_total} ({pct})")
    lines.append(f"  _(Robust = no param nudge ±10% drops OOS Sharpe by >20%)_")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Top Combos")
    lines.append("")

    if ranked:
        lines.append("| Symbol | Off-TF | Direction | SL | Winner Mask | "
                     "Winner Sharpe | Stage2 Sharpe | Trades | Robust |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in ranked:
            robust_icon = "✅" if r.get("robust") else "❌"
            lines.append(
                f"| {r.get('symbol','?')} "
                f"| {r.get('timeframe','?')} "
                f"| {r.get('direction','?')} "
                f"| {r.get('sl_type','?')} "
                f"| {r.get('winner_mask','?')} "
                f"| {r.get('winner_sharpe','N/A')} "
                f"| {r.get('stage2_oos_sharpe','N/A')} "
                f"| {r.get('winner_trades','?')} "
                f"| {robust_icon} |"
            )
    else:
        lines.append("_No Stage 4 results yet._")

    lines.append("")
    lines.append(f"**Robust rate: {n_robust} / {n_total}**")
    lines.append("")

    out_path = RESULTS_BASE / strategy_id / "SUMMARY.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  Robust: {n_robust}/{n_total} ({pct})")
    return n_robust, n_total


def _best_combo_str(strategy_id: str) -> str:
    stage4_dir = RESULTS_BASE / strategy_id / "stage4"
    if not stage4_dir.exists():
        return "—"
    best = None
    for fpath in stage4_dir.glob("*_sensitivity.json"):
        try:
            r = json.loads(fpath.read_text(encoding="utf-8"))
            ws = r.get("winner_sharpe")
            if ws and (best is None or ws > best.get("winner_sharpe", 0)):
                best = r
        except Exception:
            continue
    if not best:
        return "—"
    return (f"{best.get('symbol','?')} {best.get('timeframe','?')} "
            f"{best.get('direction','?')} {best.get('sl_type','?')} "
            f"{best.get('winner_mask','?')} Ŝ={best.get('winner_sharpe',0):.3f}")


def update_roadmap(strategy_stats: dict) -> None:
    """Append Wave 1 results section to BACKTEST-ROADMAP.md (idempotent)."""
    content = ROADMAP_PATH.read_text(encoding="utf-8")
    if ROADMAP_MARKER in content:
        print(f"BACKTEST-ROADMAP.md: '{ROADMAP_MARKER}' section already exists — skipping.")
        return

    s1_base  = RESULTS_BASE / "stage1_summarized"
    s2_base  = RESULTS_BASE / "stage2_summarized"
    s3_base  = RESULTS_BASE / "stage3_summarized"

    rows = []
    for sid, (n_robust, n_total) in strategy_stats.items():
        home_tf = STRATEGY_META[sid]["home_tf"]
        s1_pass = _load_summary_line(s1_base / f"{sid}_stage1_summary.md", "Pass rate:")
        s2_pass = _load_summary_line(s2_base / f"{sid}_stage2_summary.md", "Stage 2 pass rate:")
        s3_impr = _load_summary_line(s3_base / f"{sid}_stage3_summary.md", "Stage 3 DOW improvement rate:")
        best    = _best_combo_str(sid)
        rows.append(
            f"| {sid} | {home_tf} | {s1_pass} | {s2_pass} | {s3_impr} "
            f"| {n_robust}/{n_total} | {best} |"
        )

    section = [
        "",
        "---",
        "",
        ROADMAP_MARKER + " (Stages 1–4)",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}  ",
        "**Strategies:** 10 · **Symbols:** 39 · **Test window:** 2022-01-01 → 2024-12-31",
        "",
        "| Strategy | Home TF | S1 Pass | S2 Pass | S3 DOW Improved | S4 Robust | Best Combo |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
    ]

    updated = content.rstrip() + "\n" + "\n".join(section) + "\n"
    ROADMAP_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated: {ROADMAP_PATH}")


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

    strategy_stats = {}
    for sid in targets:
        print(f"\n-- {sid} --")
        n_robust, n_total = generate_summary(sid)
        strategy_stats[sid] = (n_robust, n_total)

    if len(targets) > 1:
        total_r = sum(v[0] for v in strategy_stats.values())
        total_t = sum(v[1] for v in strategy_stats.values())
        pct = f"{100*total_r/total_t:.1f}%" if total_t > 0 else "0%"
        print(f"\n{'='*50}")
        print(f"ALL strategies Stage 4 — robust: {total_r}/{total_t} ({pct})")
        update_roadmap(strategy_stats)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test with empty stage4 dirs**

```powershell
cd optimization/wave4
& "C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\venv\Scripts\python.exe" generate_stage4_summary.py SWING3
```

Expected:
```
-- SWING3 --
Written: ...results\SWING3\SUMMARY.md
  Robust: 0/0 (0%)
```

- [ ] **Step 3: Commit**

```powershell
git add optimization/wave4/generate_stage4_summary.py
git commit -m "feat: generate_stage4_summary — SUMMARY.md per strategy + BACKTEST-ROADMAP.md update"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ `stage4_utils.py`: `SENSITIVITY_FILTER=0.5`, `nudge_params`, `load_stage3_passing`, `run_sensitivity_parallel` (spec §5)
- ✅ `nudge_params`: skips bool/string/"direction", integer min=1, float rounded to 4dp (spec §3)
- ✅ `load_stage3_passing` reads `*_dow.json` (not `*_sensitivity.json`) from `stage3/` (spec §2)
- ✅ 10 sensitivity scripts in `wave4/` (spec §4)
- ✅ `_worker_v2` computes indicators once, loops over params, nudges ±10%, flags `sensitive` if `sharpe < winner_sharpe * 0.8` (spec §6)
- ✅ `None` sharpe treated as non-sensitive (spec §3 addendum)
- ✅ `robust = True` only if `len(sensitivity) > 0 and no param sensitive` (spec §3)
- ✅ Sensitivity JSON has `sensitivity`, `robust`, `winner_mask`, `winner_sharpe`, `stage=4` (spec §7)
- ✅ Output path `stage4/*_sensitivity.json` (spec §4)
- ✅ `generate_stage4_summary.py` writes `results/{STRATEGY}/SUMMARY.md` with ranked combos (spec §8)
- ✅ BACKTEST-ROADMAP.md update is idempotent (spec §8)
- ✅ DOW_MASKS imported from `stage3_utils` (not redefined)

**Placeholder scan:** None found.

**Type consistency:** `task` dict keys in `run_sensitivity_parallel` (`sym`, `tf`, `direction`, `sl_type`, `best_params`, `winner_mask`, `winner_sharpe`, `winner_trades`, `stage2_oos_sharpe`) match exactly what `_worker_v2` unpacks in Task 2.
