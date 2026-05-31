#!/usr/bin/env python3
"""
SWING5 Stage 1 optimization — vectorbt v2 (PARALLEL).
TF: 1H  |  Strategy: swing5_keltner_breakout

Signal: close breaks outside Keltner Channel + CCI filter.
SL: EMA midline (stop_dist = close - ema); TP = stop_dist * rr_ratio.

Indicator params cached in outer loop (27 unique combos):
  kc_length [15,20,25] × kc_mult [1.5,2.0,2.5] × cci_period [14,20,28]

CCI threshold params sweep signals (9 per indicator combo):
  cci_long_min [-100,-50,0] × cci_short_max [0,50,100]

SL params swept as vectorbt columns (inner dimension per vbt call).
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

import json
import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product
from concurrent.futures import ProcessPoolExecutor, as_completed, BrokenExecutor

import numba
import vectorbt as vbt

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING5\stage1")
V2_NOTE     = "v2/vectorbt"

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]
LIMITED_DATA = {"ENA", "TAO"}

DIRECTIONS = ["both", "long", "short"]
SL_TYPES   = ["embedded", "fixed_pct", "fixed_signal", "atr"]

# Indicator shape params (outer loop, 27 unique indicator combos)
INDICATOR_PARAMS = {
    "kc_length":  [15, 20, 25],
    "kc_mult":    [1.5, 2.0, 2.5],
    "cci_period": [14, 20, 28],
}
# CCI filter thresholds (sweep as nested loop inside indicator loop)
THRESHOLD_PARAMS = {
    "cci_long_min":  [-100, -50, 0],
    "cci_short_max": [0, 50, 100],
}
# SL-only params swept as vectorbt columns
SL_PARAM_GRID = {
    "embedded":     {"rr_ratio": [2.0, 3.0, 4.0]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "atr":          {"atr_stop_mult":   [1.0, 1.5, 2.0, 2.5, 3.0],
                     "rr_ratio":        [2.0, 3.0, 4.0]},
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):  return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray):  return obj.tolist()
        return super().default(obj)


def _make_result(symbol, direction, sl_type, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy":         "swing5_keltner_breakout",
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


# ── Indicators ────────────────────────────────────────────────────────────────

def _compute_kc(high, low, close, kc_length, kc_mult):
    """Keltner Channel: EMA ± kc_mult × ATR(kc_length). Returns (ema, upper, lower, atr)."""
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    ema = c.ewm(span=kc_length, adjust=False).mean()
    tr  = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(kc_length).mean()
    upper = (ema + kc_mult * atr).values
    lower = (ema - kc_mult * atr).values
    return ema.values, upper, lower, atr.values


def _compute_cci(high, low, close, period):
    """CCI = (typical_price - SMA(typical_price)) / (0.015 * mean_deviation)."""
    tp = (pd.Series(high) + pd.Series(low) + pd.Series(close)) / 3.0
    sma = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: np.mean(np.abs(x - x.mean())), raw=True)
    cci = (tp - sma) / (0.015 * mad.replace(0, np.nan))
    return cci.fillna(0).values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(ema, upper_kc, lower_kc, cci, close,
                  cci_long_min, cci_short_max, direction):
    """
    Long: close > KC_upper + CCI > cci_long_min
    Short: close < KC_lower + CCI < cci_short_max
    No signal exits — SL at EMA, TP via rr_ratio.
    """
    n  = len(close)
    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    valid_ema = ~np.isnan(ema)
    if direction in ("long", "both"):
        le = valid_ema & (close > upper_kc) & (cci > cci_long_min)
    if direction in ("short", "both"):
        se = valid_ema & (close < lower_kc) & (cci < cci_short_max)

    return le, lx, se, sx


# ── vectorbt portfolio ────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    g = SL_PARAM_GRID[sl_type]
    if sl_type == "embedded":
        return [{"rr_ratio": r} for r in g["rr_ratio"]]
    if sl_type in ("fixed_pct", "fixed_signal"):
        return [{"stop_loss_pct": sl, "take_profit_pct": tp}
                for sl, tp in product(g["stop_loss_pct"], g["take_profit_pct"])]
    if sl_type == "atr":
        return [{"atr_stop_mult": m, "rr_ratio": r}
                for m, r in product(g["atr_stop_mult"], g["rr_ratio"])]
    raise ValueError(f"Unknown sl_type: {sl_type}")


def _extract_pf_stats(pf, n_combos):
    def _to_list(x):
        if isinstance(x, pd.Series):
            return x.reset_index(drop=True).tolist()
        if hasattr(x, '__iter__') and not isinstance(x, (float, int, np.floating, np.integer)):
            return list(x)
        return [float(x)] * n_combos

    try:
        sharpes = _to_list(pf.sharpe_ratio())
    except Exception:
        sharpes = [np.nan] * n_combos
    try:
        max_dds = [v * 100.0 for v in _to_list(pf.max_drawdown())]
    except Exception:
        max_dds = [np.nan] * n_combos

    trade_counts = [0] * n_combos
    win_rates    = [0.0] * n_combos
    try:
        records = pf.trades.records
        if isinstance(records, pd.DataFrame) and len(records) > 0:
            col_s = records["col"] if "col" in records.columns else pd.Series([0] * len(records))
            pnl_s = records["pnl"] if "pnl" in records.columns else pd.Series([0.0] * len(records))
            for i in range(n_combos):
                mask = col_s == i
                trade_counts[i] = int(mask.sum())
                if trade_counts[i] > 0:
                    win_rates[i] = float((pnl_s[mask] > 0).mean() * 100.0)
    except Exception:
        pass

    def _pad(lst):
        if not lst:
            return [np.nan] * n_combos
        return (lst + [lst[-1]] * n_combos)[:n_combos]

    return pd.DataFrame({
        "sharpe":   _pad(sharpes),
        "trades":   trade_counts,
        "win_rate": win_rates,
        "max_dd":   _pad(max_dds),
    })


def _run_vbt_portfolio(close_series, le, lx, se, sx,
                       sl_type, sl_params_list, atr, ema):
    """One vbt call covering all SL combos as columns."""
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq="1h")

    if sl_type == "embedded":
        # SL at EMA midline (fraction of close); TP = SL × rr_ratio
        sl_frac = np.clip(
            np.where(close_arr > 0, np.abs(close_arr - ema) / close_arr, 0.02),
            1e-4, 1.0,
        )
        sl_2d = np.tile(sl_frac[:, None], (1, n_combos))
        tp_2d = np.column_stack([sl_frac * p["rr_ratio"] for p in sl_params_list])
        tp_2d = np.clip(tp_2d, 1e-4, 5.0)
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_2d, tp_stop=tp_2d,
        )
    elif sl_type == "fixed_pct":
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_arr, tp_stop=tp_arr,
        )
    elif sl_type == "fixed_signal":
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_arr, tp_stop=tp_arr,
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
            **common,
            entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_2d, tp_stop=tp_2d,
        )
    else:
        raise ValueError(f"Unknown sl_type: {sl_type}")

    return _extract_pf_stats(pf, n_combos)


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    kc_cache: dict = {}
    cci_cache: dict = {}

    ip = INDICATOR_PARAMS
    tp = THRESHOLD_PARAMS
    for kc_length, kc_mult, cci_period in product(
        ip["kc_length"], ip["kc_mult"], ip["cci_period"]
    ):
        kc_key = (kc_length, kc_mult)
        if kc_key not in kc_cache:
            kc_cache[kc_key] = _compute_kc(h, l, c, kc_length, kc_mult)
        ema_arr, upper_kc, lower_kc, atr_arr = kc_cache[kc_key]

        cci_key = (cci_period,)
        if cci_key not in cci_cache:
            cci_cache[cci_key] = _compute_cci(h, l, c, cci_period)
        cci_arr = cci_cache[cci_key]

        for cci_long_min, cci_short_max in product(
            tp["cci_long_min"], tp["cci_short_max"]
        ):
            le, lx, se, sx = _make_signals(
                ema_arr, upper_kc, lower_kc, cci_arr, c,
                cci_long_min, cci_short_max, direction,
            )
            if le.sum() + se.sum() == 0:
                continue

            try:
                stats_df = _run_vbt_portfolio(
                    close_s, le, lx, se, sx, sl_type, sl_list, atr_arr, ema_arr
                )
            except Exception as e:
                print(f"    vbt error ({kc_length},{kc_mult},{cci_period},"
                      f"{cci_long_min},{cci_short_max}): {e}", flush=True)
                continue

            for row_idx, sl_p in enumerate(sl_list):
                if row_idx >= len(stats_df):
                    continue
                row = stats_df.iloc[row_idx]
                sharpe   = float(row["sharpe"])   if np.isfinite(row.get("sharpe",   np.nan)) else -np.inf
                n_trades = int(row["trades"])
                wr       = float(row["win_rate"]) if np.isfinite(row.get("win_rate", 0.0))    else 0.0
                dd       = float(row["max_dd"])   if np.isfinite(row.get("max_dd",   np.nan)) else 0.0

                if n_trades < 30 or sharpe <= best_sharpe:
                    continue
                best_sharpe = sharpe
                best_result = (
                    {
                        "kc_length":     kc_length,
                        "kc_mult":       kc_mult,
                        "cci_period":    cci_period,
                        "cci_long_min":  cci_long_min,
                        "cci_short_max": cci_short_max,
                        "direction":     direction,
                        **sl_p,
                    },
                    sharpe, n_trades, wr, dd,
                )

    return best_result


def _eval_single(data, direction, sl_type, best_params):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    try:
        ema_arr, upper_kc, lower_kc, atr_arr = _compute_kc(
            h, l, c, best_params["kc_length"], best_params["kc_mult"]
        )
        cci_arr = _compute_cci(h, l, c, best_params["cci_period"])
        le, lx, se, sx = _make_signals(
            ema_arr, upper_kc, lower_kc, cci_arr, c,
            best_params["cci_long_min"], best_params["cci_short_max"], direction,
        )
        if sl_type == "embedded":
            sl_list = [{"rr_ratio": best_params["rr_ratio"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct": best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        elif sl_type == "atr":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio": best_params["rr_ratio"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")
        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr_arr, ema_arr)
        row = stats_df.iloc[0]
        sharpe = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        return sharpe, int(row["trades"])
    except Exception as e:
        print(f"    _eval_single error: {e}", flush=True)
        return None, 0


def _worker_v2(task):
    sym, direction, sl_type = task
    import sys
    sys.path.insert(0, str(VENV_SITE_PACKAGES))
    sys.path.insert(0, str(BACKTESTING_MCP))
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame

    symbol_usdt = sym + "USDT"
    note        = (V2_NOTE + " ~9 months data") if sym in LIMITED_DATA else V2_NOTE
    log_prefix  = f"[{symbol_usdt} {direction} {sl_type}]"

    print(f"{log_prefix} loading data...", flush=True)
    try:
        data = engine.get_data(symbol_usdt, TimeFrame.H1,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        return _make_result(symbol_usdt, direction, sl_type, note=f"DATA ERROR: {e}")

    if data.empty or len(data) < 500:
        return _make_result(symbol_usdt, direction, sl_type, note="insufficient data")

    split_idx  = int(len(data) * 0.7)
    train_data = data.iloc[:split_idx]
    test_data  = data.iloc[split_idx:]

    print(f"{log_prefix} optimizing ({len(train_data)} train bars)...", flush=True)
    try:
        opt = _optimize_vbt(train_data, direction, sl_type)
    except Exception as e:
        return _make_result(symbol_usdt, direction, sl_type, note=f"OPT ERROR: {e}")

    if opt is None:
        return _make_result(symbol_usdt, direction, sl_type,
                            note=note + " | 0 combos passed 30-trade filter")

    best_params, train_sharpe, num_trades, win_rate, max_dd = opt
    print(f"{log_prefix} best train: sharpe={train_sharpe:.4f} trades={num_trades}", flush=True)

    if num_trades < 30:
        return _make_result(symbol_usdt, direction, sl_type,
                            best_params=best_params, train_sharpe=train_sharpe,
                            num_trades=num_trades, win_rate=win_rate, max_dd=max_dd,
                            note=note + f" | num_trades={num_trades} < 30")

    oos_sharpe, _ = _eval_single(test_data, direction, sl_type, best_params)
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


def _predownload_all(symbols):
    from src.core.backtesting_engine import engine
    from config.settings import TimeFrame
    start, end = datetime(2022, 1, 1), datetime(2024, 12, 31)
    print(f"Pre-downloading {len(symbols)} symbols (1H)...")
    for sym in symbols:
        symbol_usdt = sym + "USDT"
        try:
            d = engine.get_data(symbol_usdt, TimeFrame.H1, start, end)
            print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
        except Exception as e:
            print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description="SWING5 Stage 1 v2 parallel optimization")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
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
                        if "WORKER CRASH" in note or "OPT ERROR" in note or "DATA ERROR" in note:
                            all_tasks.append((sym, direction, sl_type))
                            continue
                    except Exception:
                        pass
                    skipped += 1
                else:
                    all_tasks.append((sym, direction, sl_type))

    total = len(SYMBOLS) * len(DIRECTIONS) * len(SL_TYPES)
    print(f"SWING5 Stage 1 v2 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do.")
        return

    done = skipped
    passed = 0
    for sym in SYMBOLS:
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fpath = RESULTS_DIR / f"{sym}USDT_1h_{direction}_{sl_type}.json"
                if fpath.exists():
                    try:
                        if json.loads(fpath.read_text()).get("verdict") == "PASS":
                            passed += 1
                    except Exception:
                        pass

    remaining = list(all_tasks)
    while remaining:
        batch, remaining = remaining[:], []
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
                        print(f"WORKER CRASH [{symbol_usdt} {direction} {sl_type}]: {e}", flush=True)
                        result = _make_result(symbol_usdt, direction, sl_type, note=f"WORKER CRASH: {e}")
                    with open(fpath, "w") as f:
                        json.dump(result, f, indent=2, cls=NumpyEncoder)
                    done += 1
                    if result.get("verdict") == "PASS":
                        passed += 1
                    print(f"[{done}/{total}] {result['verdict']} | {fname}", flush=True)
        except BrokenExecutor:
            print("Pool broken, restarting...", flush=True)

    print(f"\n{'='*60}")
    print(f"DONE: {done}/{total} combos. Passed: {passed}")


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
