#!/usr/bin/env python3
"""
SWING2 Stage 1 optimization — PARALLEL version.

Runs 40 symbols × 3 directions × 4 SL types = 480 combos.
Each combo is an independent process → real multi-core parallelism,
bypassing the GIL limitation that makes bt.optimize() effectively
single-threaded on Windows.

Usage:
    python run_swing2_stage1_parallel.py              # auto-detect workers
    python run_swing2_stage1_parallel.py --workers 8  # explicit worker count

How it works:
  - Each (symbol, direction, sl_type) combo is one task.
  - Tasks already on disk are skipped (same resume logic as serial version).
  - WORKERS processes run concurrently; each runs a full bt.optimize() call
    on a dedicated data slice → no shared state, no GIL contention.
  - Estimated speedup: ~WORKERS× over serial (e.g. 8 cores → 8× faster).
"""
import json
import sys
import os
import numpy as np
import argparse
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
# sys.path is set inside the worker (each process must do it itself)

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING2\stage1")

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO"
]
LIMITED_DATA = {"ENA", "TAO"}

DIRECTIONS = ["both", "long", "short"]
SL_TYPES = ["embedded", "fixed_pct", "fixed_signal", "atr"]

GRIDS = {
    "embedded": {
        "bb_length":     [15, 20, 25],
        "bb_mult":       [1.8, 2.0, 2.2],
        "squeeze_bars":  [3, 5, 8],
        "macd_fast":     [10, 12],
        "macd_slow":     [24, 26],
        "atr_stop_mult": [2.0, 2.5, 3.0],
        "rr_ratio":      [2.0, 2.5, 3.0],
    },
    "fixed_pct": {
        "bb_length":       [15, 20, 25],
        "bb_mult":         [1.8, 2.0, 2.2],
        "squeeze_bars":    [3, 5, 8],
        "macd_fast":       [10, 12],
        "macd_slow":       [24, 26],
        "sl_mode":         ["fixed_pct"],
        "stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
        "take_profit_pct": [3.0, 4.0, 6.0, 8.0],
    },
    "fixed_signal": {
        "bb_length":       [15, 20, 25],
        "bb_mult":         [1.8, 2.0, 2.2],
        "squeeze_bars":    [3, 5, 8],
        "macd_fast":       [10, 12],
        "macd_slow":       [24, 26],
        "sl_mode":         ["fixed_signal"],
        "stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
        "take_profit_pct": [3.0, 4.0, 6.0, 8.0],
    },
    "atr": {
        "bb_length":     [15, 20, 25],
        "bb_mult":       [1.8, 2.0, 2.2],
        "squeeze_bars":  [3, 5, 8],
        "macd_fast":     [10, 12],
        "macd_slow":     [24, 26],
        "sl_mode":       ["atr"],
        "atr_stop_mult": [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
        "rr_ratio":      [2.0, 2.5, 3.0],
    },
}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def _make_result(symbol, direction, sl_type, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy": "swing2_bb_squeeze",
        "symbol": symbol,
        "timeframe": "4h",
        "direction": direction,
        "sl_type": sl_type,
        "stage": 1,
        "test_window": "2022-01-01/2024-12-31",
        "best_params": best_params,
        "train_sharpe": round(train_sharpe, 4) if train_sharpe is not None else None,
        "oos_sharpe": round(oos_sharpe, 4) if oos_sharpe is not None else None,
        "num_trades": num_trades,
        "win_rate_pct": round(win_rate, 2) if win_rate is not None else None,
        "max_drawdown_pct": round(max_dd, 2) if max_dd is not None else None,
        "verdict": verdict,
        "note": note,
    }


VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"


def _worker(task):
    """
    Run one (symbol, direction, sl_type) combo in a subprocess.
    Each worker imports the engine fresh — no shared state.
    """
    sym, direction, sl_type = task

    # Each spawned process must set up sys.path independently —
    # it does NOT inherit the parent's venv activation.
    import sys
    sys.path.insert(0, str(VENV_SITE_PACKAGES))
    sys.path.insert(0, str(BACKTESTING_MCP))

    from src.core.backtesting_engine import engine
    from src.strategies.templates import STRATEGY_REGISTRY
    from config.settings import TimeFrame

    symbol_usdt = sym + "USDT"
    sym_base = sym
    note = "~9 months data only" if sym_base in LIMITED_DATA else ""

    grid = dict(GRIDS[sl_type])
    grid["direction"] = [direction]

    log_prefix = f"[{symbol_usdt} {direction} {sl_type}]"
    print(f"{log_prefix} Starting opt ({sum(len(v) for v in grid.values())} param values)...", flush=True)

    try:
        opt_result = engine.run_optimization(
            strategy_class=STRATEGY_REGISTRY["swing2_bb_squeeze"],
            symbol=symbol_usdt,
            timeframe=TimeFrame.H4,
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2024, 12, 31),
            param_grid=grid,
            objective="sharpe_ratio",
            top_n=1,
        )
        best_stats = opt_result[0]
        best_params = opt_result[1]
    except Exception as e:
        print(f"{log_prefix} OPT ERROR: {e}", flush=True)
        return _make_result(symbol_usdt, direction, sl_type, note=f"OPT ERROR: {e}")

    num_trades = int(best_stats["# Trades"])
    train_sharpe = float(best_stats["Sharpe Ratio"])
    win_rate = float(best_stats["Win Rate [%]"])
    max_dd = float(best_stats["Max. Drawdown [%]"])

    print(f"{log_prefix} opt done: trades={num_trades} sharpe={train_sharpe:.4f}", flush=True)

    if num_trades < 30:
        return _make_result(
            symbol_usdt, direction, sl_type,
            best_params=best_params, train_sharpe=train_sharpe,
            num_trades=num_trades, win_rate=win_rate, max_dd=max_dd,
            note=note or f"num_trades={num_trades} < 30",
        )

    print(f"{log_prefix} Walk-forward...", flush=True)
    try:
        train_r, test_r, split_date = engine.run_walk_forward(
            strategy_class=STRATEGY_REGISTRY["swing2_bb_squeeze"],
            symbol=symbol_usdt,
            timeframe=TimeFrame.H4,
            start_date=datetime(2022, 1, 1),
            end_date=datetime(2024, 12, 31),
            train_ratio=0.7,
            parameters=best_params,
        )
        wf_train_sharpe = train_r.stats.get("sharpe_ratio")
        oos_sharpe = test_r.stats.get("sharpe_ratio")
        if wf_train_sharpe is not None:
            train_sharpe = wf_train_sharpe
    except Exception as e:
        print(f"{log_prefix} WF ERROR: {e}", flush=True)
        return _make_result(
            symbol_usdt, direction, sl_type,
            best_params=best_params, train_sharpe=train_sharpe,
            num_trades=num_trades, win_rate=win_rate, max_dd=max_dd,
            note=note or f"WF ERROR: {e}",
        )

    verdict = "PASS" if (oos_sharpe is not None and oos_sharpe > 0) else "FAIL"
    oos_str = f"{oos_sharpe:.4f}" if oos_sharpe is not None else "None"
    print(f"{log_prefix} WF done: oos_sharpe={oos_str} => {verdict}", flush=True)

    return _make_result(
        symbol_usdt, direction, sl_type,
        best_params=best_params, train_sharpe=train_sharpe,
        oos_sharpe=oos_sharpe, num_trades=num_trades,
        win_rate=win_rate, max_dd=max_dd,
        verdict=verdict, note=note,
    )


def main():
    parser = argparse.ArgumentParser(description="SWING2 Stage 1 parallel optimization")
    parser.add_argument(
        "--workers", type=int,
        default=max(1, (os.cpu_count() or 4) // 2),
        help="Number of parallel worker processes (default: half of CPU count)"
    )
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Build task list — skip already-done combos, but re-run crash results
    all_tasks = []
    skipped = 0
    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
                fpath = RESULTS_DIR / fname
                if fpath.exists():
                    try:
                        data = json.loads(fpath.read_text())
                        if "WORKER CRASH" in str(data.get("note", "")):
                            # Re-run crashed results
                            all_tasks.append((sym, direction, sl_type))
                            continue
                    except Exception:
                        pass
                    skipped += 1
                else:
                    all_tasks.append((sym, direction, sl_type))

    total = len(SYMBOLS) * len(DIRECTIONS) * len(SL_TYPES)
    print(f"SWING2 Stage 1 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total")
    print()

    if not all_tasks:
        print("Nothing to do — all results already on disk.")
        return

    done = skipped
    passed = 0

    # Count already-passed results
    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
                fpath = RESULTS_DIR / fname
                if fpath.exists():
                    try:
                        with open(fpath) as f:
                            r = json.load(f)
                        if r.get("verdict") == "PASS":
                            passed += 1
                    except Exception:
                        pass

    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(_worker, task): task for task in all_tasks}

        for future in as_completed(futures):
            task = futures[future]
            sym, direction, sl_type = task
            symbol_usdt = sym + "USDT"
            fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
            fpath = RESULTS_DIR / fname

            try:
                result = future.result()
            except Exception as e:
                print(f"WORKER CRASH [{symbol_usdt} {direction} {sl_type}]: {e}", flush=True)
                result = _make_result(symbol_usdt, direction, sl_type, note=f"WORKER CRASH: {e}")

            with open(fpath, "w") as f:
                json.dump(result, f, indent=2, cls=NumpyEncoder)

            done += 1
            if result.get("verdict") == "PASS":
                passed += 1
            print(f"[{done}/{total}] {result['verdict']} | {fname}", flush=True)

    print(f"\n{'='*60}")
    print(f"DONE: {done}/{total} combos. Passed: {passed}")


if __name__ == "__main__":
    # Required on Windows for ProcessPoolExecutor
    from multiprocessing import freeze_support
    freeze_support()
    main()
