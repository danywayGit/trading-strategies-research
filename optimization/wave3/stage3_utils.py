#!/usr/bin/env python3
"""
Shared machinery for Stage 3 DOW filter scripts.

Exports:
    DOW_MASKS    — 8 entry masks keyed by name
    MIN_TRADES   — minimum OOS trades for a mask to be a candidate (20)
    MIN_LIFT     — minimum absolute Sharpe improvement over ALL (0.10)
    load_stage2_passing(strategy_id, results_base) -> list[dict]
    select_winner(dow_results) -> (mask, sharpe, trades, improved)
    run_stage3_parallel(strategy_id, results_base, worker_fn,
                        backtesting_mcp, workers, skip_download)
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed, BrokenExecutor
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Callable, Optional

import numpy as np

_DOW_NAMES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]  # index == weekday int

def _build_dow_masks() -> dict:
    """Return all 128 masks: 'ALL' (no filter) + every non-empty subset of Mon–Sun."""
    masks: dict = {"ALL": None}
    for size in range(1, 8):
        for combo in combinations(range(7), size):
            name = "+".join(_DOW_NAMES[d] for d in combo)
            masks[name] = set(combo)
    return masks

DOW_MASKS = _build_dow_masks()

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
    all_sharpe_raw = all_data.get("oos_sharpe")
    all_sharpe = all_sharpe_raw if all_sharpe_raw is not None else 0.0
    all_trades = all_data.get("num_trades", 0)

    candidates = {
        name: data for name, data in dow_results.items()
        if name != "ALL"
        and data.get("num_trades", 0) >= MIN_TRADES
        and data.get("oos_sharpe") is not None
    }

    if candidates:
        best        = max(candidates, key=lambda m: candidates[m]["oos_sharpe"])
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


def run_stage3_parallel(
    strategy_id: str,
    results_base: Path,
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
                            "symbol":        task["sym"] + "USDT",
                            "timeframe":     task["tf"],
                            "direction":     task["direction"],
                            "sl_type":       task["sl_type"],
                            "winner_mask":   None,
                            "winner_sharpe": None,
                            "winner_trades": None,
                            "dow_improved":  False,
                            "note":          f"WORKER CRASH: {e}",
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
