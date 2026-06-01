#!/usr/bin/env python3
"""
Shared machinery for Stage 2 off-TF expansion scripts.

Exports:
    SHARPE_FILTER   — minimum Stage 1 OOS Sharpe to advance (0.5)
    OFF_TF_MAP      — maps home TF string to list of 3 off-TF strings
    load_stage1_passing(strategy_id, results_base, sharpe_threshold) -> set
    run_stage2_parallel(strategy_id, home_tf, results_base, symbols,
                        worker_fn, backtesting_mcp, workers, skip_download,
                        sharpe_threshold)
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

    off_tfs    = OFF_TF_MAP[home_tf]
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
