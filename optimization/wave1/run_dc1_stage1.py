#!/usr/bin/env python3
"""
DC1 Stage 1 optimization across all available symbols.
Home TF: 4H. Runs 3 directions × 4 SL types = 12 combos per symbol.
"""
import json
import sys
import numpy as np
from pathlib import Path
from datetime import datetime

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP))


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

from src.core.backtesting_engine import engine
from src.strategies.templates import STRATEGY_REGISTRY
from config.settings import TimeFrame

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\DC1\stage1")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

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

# DC1 embedded SL = ATR trailing stop (Turtle-style trail_atr_mult)
GRIDS = {
    "embedded": {
        "sl_mode": ["embedded"],
        "donchian_length": [15, 20, 25, 55],
        "adx_threshold": [20, 25, 30],
        "adx_exit": [15, 20, 25],
        "atr_stop_mult": [1.5, 2.0, 3.0],
        "trail_atr_mult": [1.5, 2.0, 2.5],
        "rr_ratio": [2.0, 2.5, 3.0],
        "atr_period": [10, 14, 21],
        "vol_avg_period": [14, 20, 30],
        "vol_mult": [0.8, 1.0, 1.2],
    },
    "fixed_pct": {
        "sl_mode": ["fixed_pct"],
        "donchian_length": [15, 20, 25, 55],
        "adx_threshold": [20, 25, 30],
        "adx_exit": [15, 20, 25],
        "stop_loss_pct": [1.5, 2.0, 2.5, 3.0],
        "take_profit_pct": [3.0, 4.0, 6.0],
        "atr_period": [10, 14, 21],
        "vol_avg_period": [14, 20, 30],
        "vol_mult": [0.8, 1.0, 1.2],
    },
    "fixed_signal": {
        "sl_mode": ["fixed_signal"],
        "donchian_length": [15, 20, 25, 55],
        "adx_threshold": [20, 25, 30],
        "adx_exit": [15, 20, 25],
        "stop_loss_pct": [1.5, 2.0, 2.5, 3.0],
        "take_profit_pct": [3.0, 4.0, 6.0],
        "trail_atr_mult": [1.5, 2.0, 2.5],
        "atr_period": [10, 14, 21],
        "vol_avg_period": [14, 20, 30],
        "vol_mult": [0.8, 1.0, 1.2],
    },
    "atr": {
        "sl_mode": ["atr"],
        "donchian_length": [15, 20, 25, 55],
        "adx_threshold": [20, 25, 30],
        "adx_exit": [15, 20, 25],
        "atr_stop_mult": [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
        "rr_ratio": [2.0, 2.5, 3.0],
        "atr_period": [10, 14, 21],
        "vol_avg_period": [14, 20, 30],
        "vol_mult": [0.8, 1.0, 1.2],
    },
}

STRATEGY_CLASS = STRATEGY_REGISTRY["dc1_donchian_channel"]


def run_combo(symbol_usdt, direction, sl_type):
    sym_base = symbol_usdt.replace("USDT", "")
    note = "~9 months data only" if sym_base in LIMITED_DATA else ""

    grid = dict(GRIDS[sl_type])
    grid["direction"] = [direction]

    print(f"  Optimizing {symbol_usdt} dir={direction} sl={sl_type} ...", flush=True)

    try:
        opt_result = engine.run_optimization(
            strategy_class=STRATEGY_CLASS,
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
        print(f"    OPT ERROR: {e}", flush=True)
        return make_result(symbol_usdt, direction, sl_type, note=f"OPT ERROR: {e}")

    num_trades = int(best_stats["# Trades"])
    train_sharpe = float(best_stats["Sharpe Ratio"])
    win_rate = float(best_stats["Win Rate [%]"])
    max_dd = float(best_stats["Max. Drawdown [%]"])

    print(f"    num_trades={num_trades}, sharpe={train_sharpe:.4f}", flush=True)

    if num_trades < 30:
        return make_result(
            symbol_usdt, direction, sl_type,
            best_params=best_params,
            train_sharpe=train_sharpe,
            num_trades=num_trades,
            win_rate=win_rate,
            max_dd=max_dd,
            note=note or f"num_trades={num_trades} < 30",
        )

    print(f"    Running walk-forward...", flush=True)
    try:
        train_r, test_r, split_date = engine.run_walk_forward(
            strategy_class=STRATEGY_CLASS,
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
        print(f"    WF ERROR: {e}", flush=True)
        return make_result(
            symbol_usdt, direction, sl_type,
            best_params=best_params,
            train_sharpe=train_sharpe,
            num_trades=num_trades,
            win_rate=win_rate,
            max_dd=max_dd,
            note=note or f"WF ERROR: {e}",
        )

    print(f"    oos_sharpe={oos_sharpe:.4f}" if oos_sharpe else "    oos_sharpe=None", flush=True)
    verdict = "PASS" if (oos_sharpe is not None and oos_sharpe > 0) else "FAIL"

    return make_result(
        symbol_usdt, direction, sl_type,
        best_params=best_params,
        train_sharpe=train_sharpe,
        oos_sharpe=oos_sharpe,
        num_trades=num_trades,
        win_rate=win_rate,
        max_dd=max_dd,
        verdict=verdict,
        note=note,
    )


def make_result(symbol, direction, sl_type, best_params=None, train_sharpe=None,
                oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                verdict="FAIL", note=""):
    return {
        "strategy": "dc1_donchian_channel",
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


def main():
    all_results = []
    done = 0
    passed = 0

    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        print(f"\n{'='*60}", flush=True)
        print(f"Symbol: {symbol_usdt}", flush=True)
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
                fpath = RESULTS_DIR / fname
                if fpath.exists():
                    print(f"  SKIP: {fname}", flush=True)
                    with open(fpath) as f:
                        result = json.load(f)
                    all_results.append(result)
                    done += 1
                    if result.get("verdict") == "PASS":
                        passed += 1
                    continue

                result = run_combo(symbol_usdt, direction, sl_type)
                with open(fpath, "w") as f:
                    json.dump(result, f, indent=2, cls=NumpyEncoder)
                all_results.append(result)
                done += 1
                if result.get("verdict") == "PASS":
                    passed += 1
                print(f"    => {result['verdict']} | {fname}", flush=True)

    total = len(SYMBOLS) * len(DIRECTIONS) * len(SL_TYPES)
    print(f"\n{'='*60}", flush=True)
    print(f"DONE: {done}/{total} combos. Passed: {passed}", flush=True)


if __name__ == "__main__":
    main()
