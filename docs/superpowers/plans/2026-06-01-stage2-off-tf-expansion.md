# Stage 2 Off-TF Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 10 strategy-specific Stage 2 optimization scripts in `optimization/wave2/` that re-optimize on 3 off-timeframes using Stage 1 passing combos filtered by OOS Sharpe ≥ 0.5.

**Architecture:** Approach C — `stage2_utils.py` owns filtering, task dispatch, resume logic, and JSON writing. Each strategy script copies its Stage 1 indicator logic verbatim and provides a `_worker_v2(task)` function; it calls `run_stage2_parallel()` from utils for all orchestration.

**Tech Stack:** Python 3.x, vectorbt, numba, `ProcessPoolExecutor`, BacktestingMCP engine (`TimeFrame.M15 / H1 / H4 / H12` all confirmed present in `BacktestingMCP/config/settings.py`)

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `optimization/wave2/stage2_utils.py` | Create | Shared: Stage 1 filter, task building, executor, JSON I/O |
| `optimization/wave2/tests/test_stage2_utils.py` | Create | Unit tests for utils |
| `optimization/wave2/run_swing3_stage2_parallel_v2.py` | Create | SWING3 — 1h home TF reference script |
| `optimization/wave2/run_swing5_stage2_parallel_v2.py` | Create | SWING5 — 1h home TF |
| `optimization/wave2/run_ema_rej_v1_stage2_parallel_v2.py` | Create | EMA_REJ_V1 — 1h home TF |
| `optimization/wave2/run_vr1_stage2_parallel_v2.py` | Create | VR1 — 1h home TF |
| `optimization/wave2/run_vp1_stage2_parallel_v2.py` | Create | VP1 — 1h home TF |
| `optimization/wave2/run_swing2_stage2_parallel_v2.py` | Create | SWING2 — 4h home TF reference script |
| `optimization/wave2/run_swing4_stage2_parallel_v2.py` | Create | SWING4 — 4h home TF |
| `optimization/wave2/run_dc1_stage2_parallel_v2.py` | Create | DC1 — 4h home TF |
| `optimization/wave2/run_aggr_pullback_stage2_parallel_v2.py` | Create | AGGR_PULLBACK — 4h home TF |
| `optimization/wave2/run_mo1_stage2_parallel_v2.py` | Create | MO1 — 4h home TF |
| `optimization/wave2/generate_stage2_summary.py` | Create | Summary markdown generator |

---

## Task 1: Create `stage2_utils.py` with unit tests

**Files:**
- Create: `optimization/wave2/stage2_utils.py`
- Create: `optimization/wave2/tests/__init__.py`
- Create: `optimization/wave2/tests/test_stage2_utils.py`

- [ ] **Step 1: Create the directory structure**

```powershell
New-Item -ItemType Directory -Force "optimization/wave2/tests"
```

- [ ] **Step 2: Write the failing tests**

Create `optimization/wave2/tests/test_stage2_utils.py`:

```python
import json
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from stage2_utils import load_stage1_passing, OFF_TF_MAP, SHARPE_FILTER


def _write_stage1_json(base_dir, strategy_id, symbol, tf, direction, sl_type,
                       oos_sharpe, verdict="PASS"):
    d = base_dir / strategy_id / "stage1"
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": symbol, "timeframe": tf, "direction": direction,
        "sl_type": sl_type, "oos_sharpe": oos_sharpe, "verdict": verdict,
    }
    (d / f"{symbol}_{tf}_{direction}_{sl_type}.json").write_text(json.dumps(payload))


def test_load_stage1_passing_filters_below_threshold():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage1_json(tmp, "SWING3", "BTCUSDT", "1h", "both", "atr", 0.8)
        _write_stage1_json(tmp, "SWING3", "ETHUSDT", "1h", "long", "embedded", 0.3)
        _write_stage1_json(tmp, "SWING3", "SOLUSDT", "1h", "short", "fixed_pct", 0.6)

        result = load_stage1_passing("SWING3", tmp, sharpe_threshold=0.5)

        assert ("BTCUSDT", "both", "atr") in result
        assert ("SOLUSDT", "short", "fixed_pct") in result
        assert ("ETHUSDT", "long", "embedded") not in result


def test_load_stage1_passing_excludes_fail_verdict():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage1_json(tmp, "SWING3", "BTCUSDT", "1h", "both", "atr",
                           oos_sharpe=0.9, verdict="FAIL")
        result = load_stage1_passing("SWING3", tmp)
        assert len(result) == 0


def test_load_stage1_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_stage1_passing("NONEXISTENT", Path(tmp))
        assert result == set()


def test_load_stage1_passing_skips_corrupt_json():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d = tmp / "SWING3" / "stage1"
        d.mkdir(parents=True)
        (d / "BTCUSDT_1h_both_atr.json").write_text("{invalid json")
        result = load_stage1_passing("SWING3", tmp)
        assert result == set()


def test_off_tf_map_1h_home():
    assert set(OFF_TF_MAP["1h"]) == {"15m", "4h", "12h"}
    assert len(OFF_TF_MAP["1h"]) == 3


def test_off_tf_map_4h_home():
    assert set(OFF_TF_MAP["4h"]) == {"15m", "1h", "12h"}
    assert len(OFF_TF_MAP["4h"]) == 3


def test_sharpe_filter_default_is_half():
    assert SHARPE_FILTER == 0.5
```

- [ ] **Step 3: Run tests to confirm they fail**

```powershell
cd optimization/wave2
python -m pytest tests/test_stage2_utils.py -v
```

Expected: `ModuleNotFoundError: No module named 'stage2_utils'`

- [ ] **Step 4: Implement `stage2_utils.py`**

Create `optimization/wave2/stage2_utils.py`:

```python
#!/usr/bin/env python3
"""
Shared machinery for Stage 2 off-TF expansion scripts.

Exports:
    SHARPE_FILTER   — minimum Stage 1 OOS Sharpe to advance (0.5)
    OFF_TF_MAP      — maps home TF string to list of 3 off-TF strings
    load_stage1_passing(strategy_id, results_base, sharpe_threshold) -> set
    run_stage2_parallel(strategy_id, home_tf, results_base, symbols,
                        worker_fn, workers, skip_download, sharpe_threshold)
"""
import json
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import numpy as np

SHARPE_FILTER = 0.5

OFF_TF_MAP = {
    "1h": ["15m", "4h", "12h"],
    "4h": ["15m", "1h", "12h"],
}

# Maps TF string -> TimeFrame enum attribute name (used inside worker processes)
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


def load_stage1_passing(
    strategy_id: str,
    results_base: Path,
    sharpe_threshold: float = SHARPE_FILTER,
) -> set:
    """
    Return set of (symbol_usdt, direction, sl_type) tuples where Stage 1
    verdict == PASS and oos_sharpe >= sharpe_threshold.
    """
    stage1_dir = results_base / strategy_id / "stage1"
    passing = set()
    if not stage1_dir.exists():
        return passing
    for fpath in stage1_dir.glob("*.json"):
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("verdict") != "PASS":
            continue
        oos = data.get("oos_sharpe")
        if oos is None or oos < sharpe_threshold:
            continue
        sym       = data.get("symbol")
        direction = data.get("direction")
        sl_type   = data.get("sl_type")
        if sym and direction and sl_type:
            passing.add((sym, direction, sl_type))
    return passing


def _predownload(symbols: list, off_tfs: list, backtesting_mcp: Path) -> None:
    import sys
    sys.path.insert(0, str(backtesting_mcp / "venv" / "Lib" / "site-packages"))
    sys.path.insert(0, str(backtesting_mcp))
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame

    for tf in off_tfs:
        tf_enum = getattr(TimeFrame, TF_ENUM_NAME[tf])
        print(f"Pre-downloading {len(symbols)} symbols ({tf})...")
        for sym in symbols:
            symbol_usdt = sym + "USDT"
            try:
                d = engine.get_data(symbol_usdt, tf_enum, _START, _END)
                print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
            except Exception as e:
                print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
        print()


def run_stage2_parallel(
    strategy_id: str,
    home_tf: str,
    results_base: Path,
    symbols: list,
    worker_fn: Callable,
    backtesting_mcp: Path,
    workers: Optional[int] = None,
    skip_download: bool = False,
    sharpe_threshold: float = SHARPE_FILTER,
) -> None:
    if workers is None:
        workers = max(1, (os.cpu_count() or 4) - 2)

    off_tfs   = OFF_TF_MAP[home_tf]
    stage2_dir = results_base / strategy_id / "stage2"
    stage2_dir.mkdir(parents=True, exist_ok=True)

    if not skip_download:
        _predownload(symbols, off_tfs, backtesting_mcp)

    passing = load_stage1_passing(strategy_id, results_base, sharpe_threshold)
    print(f"\n{strategy_id} Stage 2 — {len(passing)} Stage 1 combos pass "
          f"Sharpe >= {sharpe_threshold} filter")

    all_tasks, skipped = [], 0
    for symbol_usdt, direction, sl_type in passing:
        sym = symbol_usdt.replace("USDT", "")
        for tf in off_tfs:
            fname = f"{symbol_usdt}_{tf}_{direction}_{sl_type}.json"
            fpath = stage2_dir / fname
            if fpath.exists():
                try:
                    note = str(json.loads(fpath.read_text()).get("note", ""))
                    if not any(e in note for e in
                               ("WORKER CRASH", "OPT ERROR", "DATA ERROR")):
                        skipped += 1
                        continue
                except Exception:
                    pass
            all_tasks.append((sym, tf, direction, sl_type))

    total = len(passing) * len(off_tfs)
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do — all results already on disk.")
        return

    done = skipped
    passed = 0
    for fpath in stage2_dir.glob("*.json"):
        try:
            if json.loads(fpath.read_text()).get("verdict") == "PASS":
                passed += 1
        except Exception:
            pass

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker_fn, task): task for task in all_tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
            except Exception as e:
                sym, tf, direction, sl_type = task
                result = {
                    "symbol": sym + "USDT", "timeframe": tf,
                    "direction": direction, "sl_type": sl_type,
                    "verdict": "FAIL", "note": f"WORKER CRASH: {e}",
                }

            sym_usdt  = result.get("symbol", "?")
            tf        = result.get("timeframe", "?")
            direction = result.get("direction", "?")
            sl_type   = result.get("sl_type", "?")
            verdict   = result.get("verdict", "FAIL")

            fname = f"{sym_usdt}_{tf}_{direction}_{sl_type}.json"
            (stage2_dir / fname).write_text(
                json.dumps(result, indent=2, cls=_NumpyEncoder),
                encoding="utf-8",
            )

            done += 1
            if verdict == "PASS":
                passed += 1
            oos     = result.get("oos_sharpe")
            oos_str = f"{oos:.4f}" if oos is not None else "None"
            print(
                f"[{done}/{total}] {sym_usdt} {tf} {direction} {sl_type}"
                f" → {verdict} (OOS={oos_str})",
                flush=True,
            )

    print(f"\n{strategy_id} Stage 2 complete — {passed}/{done} passed")
```

- [ ] **Step 5: Run tests to confirm they pass**

```powershell
python -m pytest tests/test_stage2_utils.py -v
```

Expected:
```
tests/test_stage2_utils.py::test_load_stage1_passing_filters_below_threshold PASSED
tests/test_stage2_utils.py::test_load_stage1_passing_excludes_fail_verdict PASSED
tests/test_stage2_utils.py::test_load_stage1_passing_empty_for_missing_dir PASSED
tests/test_stage2_utils.py::test_load_stage1_passing_skips_corrupt_json PASSED
tests/test_stage2_utils.py::test_off_tf_map_1h_home PASSED
tests/test_stage2_utils.py::test_off_tf_map_4h_home PASSED
tests/test_stage2_utils.py::test_sharpe_filter_default_is_half PASSED
7 passed
```

- [ ] **Step 6: Commit**

```powershell
git add optimization/wave2/stage2_utils.py optimization/wave2/tests/
git commit -m "feat: stage2_utils — shared filter, executor, JSON I/O for Stage 2 scripts"
```

---

## Task 2: Create `run_swing3_stage2_parallel_v2.py` (1h reference template)

**Files:**
- Source: `optimization/wave1/run_swing3_stage1_parallel_v2.py`
- Create: `optimization/wave2/run_swing3_stage2_parallel_v2.py`

- [ ] **Step 1: Copy the Stage 1 script as starting point**

```powershell
Copy-Item optimization/wave1/run_swing3_stage1_parallel_v2.py `
          optimization/wave2/run_swing3_stage2_parallel_v2.py
```

- [ ] **Step 2: Replace the header block (top of file, before imports)**

Replace:
```python
"""
SWING3 Stage 1 optimization — vectorbt v2 (PARALLEL).
...
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))
```

With:
```python
"""
SWING3 Stage 2 optimization — off-TF expansion (PARALLEL).

Runs full param-grid re-optimization on the 3 off-timeframes (15m, 4h, 12h)
for all SWING3 Stage 1 combos with OOS Sharpe >= 0.5.

Usage:
    python run_swing3_stage2_parallel_v2.py
    python run_swing3_stage2_parallel_v2.py --workers 8
    python run_swing3_stage2_parallel_v2.py --skip-download
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage2_utils import run_stage2_parallel
```

- [ ] **Step 3: Update constants block (after imports, before NumpyEncoder)**

Replace:
```python
RESULTS_DIR            = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage1")
V2_NOTE                = "v2/vectorbt"
```

With:
```python
STRATEGY_ID  = "SWING3"
HOME_TF      = "1h"
RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
V2_NOTE      = "v2/vectorbt"

TF_MAP = {
    "15m": "M15",
    "4h":  "H4",
    "12h": "H12",
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"
```

- [ ] **Step 4: Delete the `NumpyEncoder` class**

Remove the entire `NumpyEncoder` class — it is now defined in `stage2_utils.py` and used there for JSON writing. The strategy script no longer needs it.

- [ ] **Step 5: Update `_make_result` to accept `tf` and use `stage=2`**

Replace the `_make_result` function signature and `"timeframe"` / `"stage"` fields:

```python
def _make_result(symbol, direction, sl_type, tf, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy":         "swing3_supertrend_adx",
        "symbol":           symbol,
        "timeframe":        tf,
        "direction":        direction,
        "sl_type":          sl_type,
        "stage":            2,
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

- [ ] **Step 6: Update `_worker_v2` to accept `(sym, tf, direction, sl_type)`**

Replace the `_worker_v2` function:

```python
def _worker_v2(task):
    """
    Stage 2 worker. One process per (symbol, tf, direction, sl_type).
    tf is one of the 3 off-timeframes; data is loaded fresh for that TF.
    """
    sym, tf, direction, sl_type = task
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
        return _make_result(symbol_usdt, direction, sl_type, tf,
                            note=f"DATA ERROR: {e}")

    if data.empty or len(data) < 500:
        return _make_result(symbol_usdt, direction, sl_type, tf,
                            note="insufficient data")

    split_idx  = int(len(data) * 0.7)
    train_data = data.iloc[:split_idx]
    test_data  = data.iloc[split_idx:]

    print(f"{log_prefix} optimizing ({len(train_data)} train bars)...", flush=True)
    try:
        opt = _optimize_vbt(train_data, direction, sl_type)
    except Exception as e:
        print(f"{log_prefix} OPT ERROR: {e}", flush=True)
        return _make_result(symbol_usdt, direction, sl_type, tf,
                            note=f"OPT ERROR: {e}")

    if opt is None:
        return _make_result(symbol_usdt, direction, sl_type, tf,
                            note=note + " | 0 combos passed 30-trade filter")

    best_params, train_sharpe, num_trades, win_rate, max_dd = opt
    print(f"{log_prefix} best train: sharpe={train_sharpe:.4f} trades={num_trades}",
          flush=True)

    if num_trades < 30:
        return _make_result(symbol_usdt, direction, sl_type, tf,
                            best_params=best_params, train_sharpe=train_sharpe,
                            num_trades=num_trades, win_rate=win_rate, max_dd=max_dd,
                            note=note + f" | num_trades={num_trades} < 30")

    oos_sharpe, _ = _eval_single(test_data, direction, sl_type, best_params)
    verdict = "PASS" if (oos_sharpe is not None and oos_sharpe > 0) else "FAIL"
    oos_str = f"{oos_sharpe:.4f}" if oos_sharpe is not None else "None"
    print(f"{log_prefix} OOS sharpe={oos_str} => {verdict}", flush=True)

    return _make_result(
        symbol_usdt, direction, sl_type, tf,
        best_params=best_params, train_sharpe=train_sharpe,
        oos_sharpe=oos_sharpe, num_trades=num_trades,
        win_rate=win_rate, max_dd=max_dd,
        verdict=verdict, note=note,
    )
```

- [ ] **Step 7: Replace the `_predownload_all` function and `main()`**

Delete the entire `_predownload_all` function (pre-download is now handled by `stage2_utils`).

Replace `main()` with:

```python
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="SWING3 Stage 2 — off-TF expansion (15m, 4h, 12h)")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    run_stage2_parallel(
        strategy_id    = STRATEGY_ID,
        home_tf        = HOME_TF,
        results_base   = RESULTS_BASE,
        symbols        = SYMBOLS,
        worker_fn      = _worker_v2,
        backtesting_mcp= BACKTESTING_MCP,
        workers        = args.workers,
        skip_download  = args.skip_download,
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 8: Smoke test — single symbol, one off-TF**

```powershell
cd optimization/wave2
# Temporarily patch SYMBOLS in the script to just ["BTC"] and run
python -c "
import sys; sys.argv = ['x', '--skip-download']
import run_swing3_stage2_parallel_v2 as m
m.SYMBOLS = ['BTC']
# Manually create a fake Stage 1 result so the filter passes
from pathlib import Path; import json
p = Path(r'C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage1\BTCUSDT_1h_both_atr.json')
if p.exists() and json.loads(p.read_text()).get('oos_sharpe', 0) >= 0.5:
    print('BTC stage1 passes filter — proceeding')
m.main()
"
```

Verify a file appears at `results/SWING3/stage2/BTCUSDT_*_both_atr.json`.

- [ ] **Step 9: Commit**

```powershell
git add optimization/wave2/run_swing3_stage2_parallel_v2.py
git commit -m "feat: SWING3 Stage 2 — off-TF expansion script (15m, 4h, 12h)"
```

---

## Task 3: Create remaining 1h home TF scripts (SWING5, EMA_REJ_V1, VR1, VP1)

Each script follows the exact same transformation as Task 2. For each one:
1. Copy from Stage 1 counterpart
2. Apply the 7 changes listed below (all identical to Task 2 except the strategy-specific constants)

**Changes that are IDENTICAL across all scripts** (apply exactly as in Task 2):
- Add `from stage2_utils import run_stage2_parallel` after sys.path setup
- Add `STRATEGY_ID`, `HOME_TF = "1h"`, `RESULTS_BASE`, `TF_MAP` constants
- Delete `NumpyEncoder` class
- Update `_make_result` to accept `tf`, set `"stage": 2`, `"timeframe": tf`
- Update `_worker_v2` signature to `(sym, tf, direction, sl_type)`, use `TF_MAP[tf]`
- Delete `_predownload_all`
- Replace `main()` with the `run_stage2_parallel(...)` call

**Strategy-specific constants that differ:**

### SWING5

- [ ] **Copy and patch SWING5**

```powershell
Copy-Item optimization/wave1/run_swing5_stage1_parallel_v2.py `
          optimization/wave2/run_swing5_stage2_parallel_v2.py
```

Apply the common changes above, then set these constants:
```python
STRATEGY_ID = "SWING5"
HOME_TF     = "1h"
TF_MAP      = {"15m": "M15", "4h": "H4", "12h": "H12"}
```

Update `_make_result` field:
```python
"strategy": "swing5_keltner_breakout",
```

SWING5 has an extra `THRESHOLD_PARAMS` dict — leave it unchanged (it's part of the indicator logic copied verbatim from Stage 1).

- [ ] **Commit SWING5**

```powershell
git add optimization/wave2/run_swing5_stage2_parallel_v2.py
git commit -m "feat: SWING5 Stage 2 — off-TF expansion script"
```

### EMA_REJ_V1

- [ ] **Copy and patch EMA_REJ_V1**

```powershell
Copy-Item optimization/wave1/run_ema_rej_v1_stage1_parallel_v2.py `
          optimization/wave2/run_ema_rej_v1_stage2_parallel_v2.py
```

Apply the common changes, then set:
```python
STRATEGY_ID = "EMA_REJ_V1"
HOME_TF     = "1h"
TF_MAP      = {"15m": "M15", "4h": "H4", "12h": "H12"}
```

Update `_make_result` field:
```python
"strategy": "ema_rejection_v1",
```

`HTF_BARS = 9` is part of indicator logic — leave it unchanged.

- [ ] **Commit EMA_REJ_V1**

```powershell
git add optimization/wave2/run_ema_rej_v1_stage2_parallel_v2.py
git commit -m "feat: EMA_REJ_V1 Stage 2 — off-TF expansion script"
```

### VR1

- [ ] **Copy and patch VR1**

```powershell
Copy-Item optimization/wave1/run_vr1_stage1_parallel_v2.py `
          optimization/wave2/run_vr1_stage2_parallel_v2.py
```

Apply the common changes, then set:
```python
STRATEGY_ID = "VR1"
HOME_TF     = "1h"
TF_MAP      = {"15m": "M15", "4h": "H4", "12h": "H12"}
```

Update `_make_result` field:
```python
"strategy": "vr1_vwap_mean_reversion",
```

- [ ] **Commit VR1**

```powershell
git add optimization/wave2/run_vr1_stage2_parallel_v2.py
git commit -m "feat: VR1 Stage 2 — off-TF expansion script"
```

### VP1

- [ ] **Copy and patch VP1**

```powershell
Copy-Item optimization/wave1/run_vp1_stage1_parallel_v2.py `
          optimization/wave2/run_vp1_stage2_parallel_v2.py
```

Apply the common changes, then set:
```python
STRATEGY_ID = "VP1"
HOME_TF     = "1h"
TF_MAP      = {"15m": "M15", "4h": "H4", "12h": "H12"}
```

Update `_make_result` field:
```python
"strategy": "vp1_volume_profile_breakout",
```

`_VA_Z` dict is part of indicator logic — leave it unchanged.

- [ ] **Commit VP1**

```powershell
git add optimization/wave2/run_vp1_stage2_parallel_v2.py
git commit -m "feat: VP1 Stage 2 — off-TF expansion script"
```

---

## Task 4: Create `run_swing2_stage2_parallel_v2.py` (4h reference template)

**Files:**
- Source: `optimization/wave1/run_swing2_stage1_parallel_v2.py`
- Create: `optimization/wave2/run_swing2_stage2_parallel_v2.py`

This is the reference template for 4h home TF scripts. The only difference from the 1h template (Task 2) is `HOME_TF = "4h"` and `TF_MAP` covers the 1h TF instead of 4h.

- [ ] **Step 1: Copy Stage 1 script**

```powershell
Copy-Item optimization/wave1/run_swing2_stage1_parallel_v2.py `
          optimization/wave2/run_swing2_stage2_parallel_v2.py
```

- [ ] **Step 2: Apply common changes (identical to Task 2 steps 2–7)**

Apply all 7 transformations from Task 2, with these strategy-specific values:

```python
STRATEGY_ID = "SWING2"
HOME_TF     = "4h"
TF_MAP      = {"15m": "M15", "1h": "H1", "12h": "H12"}
```

Update `_make_result` field:
```python
"strategy": "swing2_bb_squeeze",
```

Update docstring off-TF list to `(15m, 1h, 12h)`.

- [ ] **Step 3: Smoke test**

```powershell
python -c "
import sys; sys.argv = ['x', '--skip-download']
import run_swing2_stage2_parallel_v2 as m
m.SYMBOLS = ['BTC']
m.main()
"
```

Verify a file appears at `results/SWING2/stage2/BTCUSDT_*_both_*.json`.

- [ ] **Step 4: Commit**

```powershell
git add optimization/wave2/run_swing2_stage2_parallel_v2.py
git commit -m "feat: SWING2 Stage 2 — off-TF expansion script (15m, 1h, 12h)"
```

---

## Task 5: Create remaining 4h home TF scripts (SWING4, DC1, AGGR_PULLBACK, MO1)

Same transformation as Task 4. `HOME_TF = "4h"` and `TF_MAP = {"15m": "M15", "1h": "H1", "12h": "H12"}` for all four.

### SWING4

- [ ] **Copy and patch SWING4**

```powershell
Copy-Item optimization/wave1/run_swing4_stage1_parallel_v2.py `
          optimization/wave2/run_swing4_stage2_parallel_v2.py
```

```python
STRATEGY_ID = "SWING4"
HOME_TF     = "4h"
TF_MAP      = {"15m": "M15", "1h": "H1", "12h": "H12"}
```

```python
"strategy": "swing4_macd_divergence",
```

- [ ] **Commit SWING4**

```powershell
git add optimization/wave2/run_swing4_stage2_parallel_v2.py
git commit -m "feat: SWING4 Stage 2 — off-TF expansion script"
```

### DC1

- [ ] **Copy and patch DC1**

```powershell
Copy-Item optimization/wave1/run_dc1_stage1_parallel_v2.py `
          optimization/wave2/run_dc1_stage2_parallel_v2.py
```

```python
STRATEGY_ID = "DC1"
HOME_TF     = "4h"
TF_MAP      = {"15m": "M15", "1h": "H1", "12h": "H12"}
```

```python
"strategy": "dc1_donchian_channel",
```

- [ ] **Commit DC1**

```powershell
git add optimization/wave2/run_dc1_stage2_parallel_v2.py
git commit -m "feat: DC1 Stage 2 — off-TF expansion script"
```

### AGGR_PULLBACK

- [ ] **Copy and patch AGGR_PULLBACK**

```powershell
Copy-Item optimization/wave1/run_aggr_pullback_stage1_parallel_v2.py `
          optimization/wave2/run_aggr_pullback_stage2_parallel_v2.py
```

```python
STRATEGY_ID = "AGGR_PULLBACK"
HOME_TF     = "4h"
TF_MAP      = {"15m": "M15", "1h": "H1", "12h": "H12"}
```

```python
"strategy": "aggr_pullback",
```

- [ ] **Commit AGGR_PULLBACK**

```powershell
git add optimization/wave2/run_aggr_pullback_stage2_parallel_v2.py
git commit -m "feat: AGGR_PULLBACK Stage 2 — off-TF expansion script"
```

### MO1

- [ ] **Copy and patch MO1**

```powershell
Copy-Item optimization/wave1/run_mo1_stage1_parallel_v2.py `
          optimization/wave2/run_mo1_stage2_parallel_v2.py
```

```python
STRATEGY_ID = "MO1"
HOME_TF     = "4h"
TF_MAP      = {"15m": "M15", "1h": "H1", "12h": "H12"}
```

```python
"strategy": "mo1_momentum_rotation",
```

- [ ] **Commit MO1**

```powershell
git add optimization/wave2/run_mo1_stage2_parallel_v2.py
git commit -m "feat: MO1 Stage 2 — off-TF expansion script"
```

---

## Task 6: Create `generate_stage2_summary.py`

**Files:**
- Source: `optimization/wave1/generate_stage1_summary.py`
- Create: `optimization/wave2/generate_stage2_summary.py`

- [ ] **Step 1: Copy Stage 1 summary generator**

```powershell
Copy-Item optimization/wave1/generate_stage1_summary.py `
          optimization/wave2/generate_stage2_summary.py
```

- [ ] **Step 2: Update the STRATEGY_META — remove RR1 and SFP1, update stage**

Replace the `STRATEGY_META` dict — remove `RR1` and `SFP1` entries (no Stage 2 for them):

```python
STRATEGY_META = {
    "SWING2":        {"key": "swing2_bb_squeeze",           "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING3":        {"key": "swing3_supertrend_adx",       "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING4":        {"key": "swing4_macd_divergence",      "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING5":        {"key": "swing5_keltner_breakout",     "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "EMA_REJ_V1":    {"key": "ema_rejection_v1",            "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "DC1":           {"key": "dc1_donchian_channel",        "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VR1":           {"key": "vr1_vwap_mean_reversion",     "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "AGGR_PULLBACK": {"key": "aggr_pullback",               "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "MO1":           {"key": "mo1_momentum_rotation",       "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VP1":           {"key": "vp1_volume_profile_breakout", "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
}
```

- [ ] **Step 3: Update `load_results` to read from `stage2/` and loop over off-TFs**

Replace the `load_results` function:

```python
def load_results(strategy_id, off_tfs, sl_types):
    stage2_dir = RESULTS_BASE / strategy_id / "stage2"
    results = {}
    if not stage2_dir.exists():
        return results
    for sym in SYMBOLS_ORDER:
        symbol_usdt = sym + "USDT"
        for tf in off_tfs:
            for direction in DIRECTIONS:
                for sl_type in sl_types:
                    fname = f"{symbol_usdt}_{tf}_{direction}_{sl_type}.json"
                    fpath = stage2_dir / fname
                    if fpath.exists():
                        try:
                            with open(fpath, encoding="utf-8") as f:
                                results[(symbol_usdt, tf, direction, sl_type)] = json.load(f)
                        except Exception:
                            pass
    return results
```

- [ ] **Step 4: Update `_cell` to use the new 4-tuple key**

```python
def _cell(results, symbol_usdt, tf, direction, sl_type):
    r = results.get((symbol_usdt, tf, direction, sl_type))
    if r is None:
        return "⬜"
    if r.get("verdict") == "PASS":
        return "✅"
    return "❌"
```

- [ ] **Step 5: Update `generate_summary` — one table per off-TF**

Replace `generate_summary`:

```python
def generate_summary(strategy_id):
    meta     = STRATEGY_META[strategy_id]
    off_tfs  = meta["off_tfs"]
    sl_types = meta["sl_types"]
    results  = load_results(strategy_id, off_tfs, sl_types)

    n_sym  = len(SYMBOLS_ORDER)
    n_dir  = len(DIRECTIONS)
    n_sl   = len(sl_types)
    n_tf   = len(off_tfs)
    total  = n_sym * n_dir * n_sl * n_tf
    done   = len(results)
    pass_list = [r for r in results.values() if r.get("verdict") == "PASS"]
    passed    = len(pass_list)
    pass_list.sort(key=lambda r: (r.get("oos_sharpe") or 0), reverse=True)

    lines = []
    lines.append(f"# {strategy_id} — Stage 2 Summary "
                 f"(home TF: {meta['home_tf'].upper()}, {n_sym} symbols)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Off-TFs tested:** {', '.join(off_tfs)}")
    lines.append(f"**Pass filter:** num_trades ≥ 30 AND OOS Sharpe > 0")
    lines.append(f"**Total combos:** {done} / {total}  "
                 f"({n_sym} symbols × {n_dir} dir × {n_sl} SL × {n_tf} TFs)")
    lines.append(f"**Pass rate:** {passed} / {done}")
    lines.append("")
    lines.append("---")

    col_labels = [
        f"{d}/{_SL_SHORT.get(s, s)}"
        for d in DIRECTIONS
        for s in sl_types
    ]
    n_data_cols = len(col_labels)
    header = "| Symbol | " + " | ".join(col_labels) + " |"
    sep    = "|---" * (n_data_cols + 1) + "|"

    for tf in off_tfs:
        lines.append("")
        lines.append(f"## Pass/Fail Table — {tf.upper()}")
        lines.append("")
        lines.append(header)
        lines.append(sep)
        for sym in SYMBOLS_ORDER:
            symbol_usdt = sym + "USDT"
            row = f"| {symbol_usdt}"
            for direction in DIRECTIONS:
                for sl_type in sl_types:
                    row += f" | {_cell(results, symbol_usdt, tf, direction, sl_type)}"
            row += " |"
            lines.append(row)

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Passing Combos (proceed to Stage 3)")
    lines.append("")
    if pass_list:
        lines.append("| Symbol | TF | Direction | SL Type | OOS Sharpe | "
                     "Train Sharpe | Trades | Max DD% | Best Params |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in pass_list:
            params_str = json.dumps(r.get("best_params") or {})
            if len(params_str) > 80:
                params_str = params_str[:77] + "..."
            oos   = r.get("oos_sharpe")
            train = r.get("train_sharpe")
            dd    = r.get("max_drawdown_pct")
            lines.append(
                f"| {r['symbol']} | {r.get('timeframe','?')} "
                f"| {r['direction']} | {r['sl_type']} "
                f"| {oos if oos is not None else 'N/A'} "
                f"| {train if train is not None else 'N/A'} "
                f"| {r.get('num_trades', 0)} "
                f"| {dd if dd is not None else 'N/A'} "
                f"| `{params_str}` |"
            )
    else:
        lines.append("_No combos passed Stage 2._")

    lines.append("")
    lines.append(f"**Stage 2 pass rate: {passed} / {done}**")
    lines.append("")

    out_dir = RESULTS_BASE / "stage2_summarized"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{strategy_id}_stage2_summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  Pass rate: {passed}/{done}  (total expected: {total})")
    return passed, done
```

- [ ] **Step 6: Update `main()` — print header referencing Stage 2**

In `main()`, update the ALL-strategy print line:
```python
print(f"ALL strategies Stage 2 - total pass rate: {total_passed}/{total_done}")
```

- [ ] **Step 7: Test the generator against existing Stage 1 data (sanity check)**

At this point no Stage 2 results exist yet. Verify the generator handles empty dirs gracefully:

```powershell
cd optimization/wave2
python generate_stage2_summary.py SWING3
```

Expected output:
```
-- SWING3 --
Written: ...results\stage2_summarized\SWING3_stage2_summary.md
  Pass rate: 0/0  (total expected: 579)
```

- [ ] **Step 8: Commit**

```powershell
git add optimization/wave2/generate_stage2_summary.py
git commit -m "feat: generate_stage2_summary — Stage 2 summary generator with per-TF tables"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ `optimization/wave2/` structure (spec §5)
- ✅ `stage2_utils.py` exports `OFF_TF_MAP`, `load_stage1_passing`, `run_stage2_parallel` (spec §6)
- ✅ 10 strategy scripts, RR1 and SFP1 excluded (spec §2)
- ✅ `TF_MAP` with M15/H1/H4/H12 confirmed present in BacktestingMCP
- ✅ Stage 1 Sharpe ≥ 0.5 filter applied in `run_stage2_parallel` (spec §4)
- ✅ Output JSON has `"stage": 2` and variable `"timeframe"` (spec §8)
- ✅ Pass filter `num_trades ≥ 30 AND OOS Sharpe > 0` (spec §8)
- ✅ `generate_stage2_summary.py` writes to `results/stage2_summarized/` (spec §9)

**Placeholder scan:** None found.

**Type consistency:** `load_stage1_passing` returns `set` of `(symbol_usdt, direction, sl_type)` — consumed correctly in `run_stage2_parallel` which iterates over it and strips `USDT` suffix for the worker task tuple `(sym, tf, direction, sl_type)`. `_worker_v2` unpacks the same 4-tuple.
