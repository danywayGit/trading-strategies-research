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
import json, os, sys
from concurrent.futures import ProcessPoolExecutor, as_completed, BrokenExecutor
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional
import numpy as np

SENSITIVITY_FILTER = 0.5

TF_ENUM_NAME = {"15m": "M15", "1h": "H1", "4h": "H4", "12h": "H12"}
_START = datetime(2022, 1, 1)
_END   = datetime(2024, 12, 31)


class _NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):  return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray):  return obj.tolist()
        return super().default(obj)


def nudge_params(best_params: dict, factor: float) -> dict:
    """Copy of best_params with numeric values nudged by factor. Skips bools, strings, 'direction'."""
    result = {}
    for k, v in best_params.items():
        if k == "direction" or isinstance(v, bool) or isinstance(v, str):
            result[k] = v
        elif isinstance(v, int):
            result[k] = max(1, round(v * factor))
        elif isinstance(v, float):
            result[k] = max(1e-9, round(v * factor, 4))
        else:
            result[k] = v
    return result


def load_stage3_passing(strategy_id: str, results_base: Path,
                        sharpe_threshold: float = SENSITIVITY_FILTER) -> list:
    """Return list of dicts for Stage 3 results where winner_sharpe >= sharpe_threshold."""
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
        enum_name = TF_ENUM_NAME.get(tf)
        if enum_name is None:
            print(f"Warning: unknown timeframe {tf!r} in Stage 3 results, skipping", file=sys.stderr)
            continue
        tf_enum = getattr(TimeFrame, enum_name)
        print(f"Pre-downloading {len(syms)} symbols ({tf})...")
        for sym in syms:
            symbol_usdt = sym + "USDT"
            try:
                d = engine.get_data(symbol_usdt, tf_enum, _START, _END)
                print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
            except Exception as e:
                print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
        print()


def run_sensitivity_parallel(strategy_id: str, results_base: Path,
                             worker_fn: Callable, backtesting_mcp: Path,
                             workers: Optional[int] = None,
                             skip_download: bool = False) -> None:
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
        sym = combo["symbol"].replace("USDT", "")
        tf, direction, sl_type = combo["timeframe"], combo["direction"], combo["sl_type"]
        fname = f"{combo['symbol']}_{tf}_{direction}_{sl_type}_sensitivity.json"
        fpath = stage4_dir / fname
        if fpath.exists():
            try:
                note = str(json.loads(fpath.read_text(encoding="utf-8")).get("note", ""))
                if not any(e in note for e in ("WORKER CRASH", "SENSITIVITY ERROR", "DATA ERROR")):
                    done += 1; continue
            except Exception:
                pass
        all_tasks.append({"sym": sym, "tf": tf, "direction": direction, "sl_type": sl_type,
                           "best_params": combo["best_params"], "winner_mask": combo["winner_mask"],
                           "winner_sharpe": combo["winner_sharpe"], "winner_trades": combo["winner_trades"],
                           "stage2_oos_sharpe": combo["stage2_oos_sharpe"]})

    total = len(passing)
    print(f"Tasks: {len(all_tasks)} to run, {done} already done, {total} total\n")
    if not all_tasks:
        print("Nothing to do — all results already on disk."); return

    remaining = list(all_tasks)
    while remaining:
        try:
            with ProcessPoolExecutor(max_workers=workers) as executor:
                completed_tasks = []
                futures = {executor.submit(worker_fn, task): task for task in remaining}
                for future in as_completed(futures):
                    task = futures[future]
                    completed_tasks.append(task)
                    try:
                        result = future.result()
                    except Exception as e:
                        result = {"symbol": task["sym"]+"USDT", "timeframe": task["tf"],
                                  "direction": task["direction"], "sl_type": task["sl_type"],
                                  "best_params": task["best_params"], "winner_mask": task["winner_mask"],
                                  "winner_sharpe": task["winner_sharpe"], "winner_trades": task["winner_trades"],
                                  "stage2_oos_sharpe": task["stage2_oos_sharpe"],
                                  "sensitivity": {}, "robust": False, "note": f"WORKER CRASH: {e}"}
                    sym_usdt = result.get("symbol","?"); tf_r = result.get("timeframe","?")
                    direction = result.get("direction","?"); sl_type = result.get("sl_type","?")
                    fname = f"{sym_usdt}_{tf_r}_{direction}_{sl_type}_sensitivity.json"
                    (stage4_dir / fname).write_text(json.dumps(result, indent=2, cls=_NumpyEncoder), encoding="utf-8")
                    done += 1
                    print(f"[{done}/{total}] {sym_usdt} {tf_r} {direction} {sl_type} → robust={result.get('robust',False)}", flush=True)
                remaining = []
        except BrokenExecutor:
            cs = {(t["sym"],t["tf"],t["direction"],t["sl_type"]) for t in completed_tasks}
            remaining = [t for t in remaining if (t["sym"],t["tf"],t["direction"],t["sl_type"]) not in cs]
            print(f"Pool broken — restarting with {len(remaining)} remaining", flush=True)

    print(f"\n{strategy_id} Stage 4 complete")
