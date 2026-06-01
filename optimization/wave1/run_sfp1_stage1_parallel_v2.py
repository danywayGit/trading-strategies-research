#!/usr/bin/env python3
"""
SFP1 Stage 1 optimization — vectorbt v2 (PARALLEL).
5m Swing Failure Pattern. Embedded SL only.
Approximations vs original:
  - No FVG entry execution (enter on SFP bar directly)
  - max_ltf_wait_bars not enforced (no FVG wait loop)
  - Swing point detection via rolling min/max (lookback_bars window)
    rather than full pivot detection with swing_lookback wings
  - Session filter applied as entry mask on bar timestamps
  - use_bias_filter: EMA50 > EMA200 for long, < for short
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

import vectorbt as vbt

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SFP1\stage1")
V2_NOTE     = "v2/vectorbt approx: direct SFP bar entry, no FVG execution"

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]
LIMITED_DATA = {"ENA", "TAO"}
DIRECTIONS   = ["both", "long", "short"]
SL_TYPES     = ["embedded"]   # SFP1 is embedded-only

INDICATOR_PARAMS = {
    "lookback_bars":     [24, 48, 72],
    "swing_lookback":    [3, 5, 7],      # used for pivot width; in approx kept for param space
    "max_ltf_wait_bars": [12, 24, 36],   # noted; not enforced in approx
    "use_bias_filter":   [True, False],
    "session_mode":      ["NY", "London", "Any"],
}

SL_PARAM_GRID = {
    "embedded": {
        "rr_ratio":      [1.5, 2.0, 2.5, 3.0],
        "sl_buffer_atr": [0.3, 0.5, 0.8],
    },
}

# Session windows: (start_hour, start_min, end_hour, end_min) UTC
_SESSION_WINDOWS = {
    "NY":     (14, 30, 20, 0),
    "London": (7,  0,  12, 0),
    "Any":    (0,  0,  24, 0),
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
        "strategy":         "sfp1_swing_failure_pattern",
        "symbol":           symbol,
        "timeframe":        "5m",
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


# ── Indicator helpers ─────────────────────────────────────────────────────────

def _compute_ema(close, period):
    return pd.Series(close).ewm(span=period, adjust=False).mean().values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, adjust=False).mean().values.astype(np.float64)


def _session_mask(index, session_mode):
    """Boolean mask: True for bars inside the session window."""
    if session_mode == "Any":
        return np.ones(len(index), dtype=bool)
    sh, sm, eh, em = _SESSION_WINDOWS[session_mode]
    bar_min = index.hour * 60 + index.minute
    start   = sh * 60 + sm
    end     = eh * 60 + em
    return (bar_min >= start) & (bar_min < end)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(high, low, close, atr, ema50, ema200, index,
                  lookback_bars, use_bias_filter, session_mode, direction):
    """
    Long SFP:  low sweeps below previous rolling min of lows,
               then closes back above that level.
    Short SFP: high sweeps above previous rolling max of highs,
               then closes back below.
    """
    n = len(close)

    # Rolling swing levels (shifted 1 bar so we don't use same-bar info)
    prev_swing_low  = pd.Series(low).rolling(lookback_bars, min_periods=1).min().shift(1).values
    prev_swing_high = pd.Series(high).rolling(lookback_bars, min_periods=1).max().shift(1).values
    prev_swing_low[0]  = low[0]
    prev_swing_high[0] = high[0]

    long_sfp  = (low  < prev_swing_low)  & (close > prev_swing_low)
    short_sfp = (high > prev_swing_high) & (close < prev_swing_high)

    # Bias filter
    uptrend   = ema50 > ema200
    downtrend = ema50 < ema200

    # Session mask
    sess = _session_mask(index, session_mode)

    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    bias_long  = uptrend   if use_bias_filter else np.ones(n, dtype=bool)
    bias_short = downtrend if use_bias_filter else np.ones(n, dtype=bool)

    if direction in ("long", "both"):
        le[1:] = (long_sfp  & sess & bias_long)[1:]

    if direction in ("short", "both"):
        se[1:] = (short_sfp & sess & bias_short)[1:]

    # SL anchor: distance from close to swept swing level
    sl_dist_long  = np.maximum(close - prev_swing_low,  0.0)
    sl_dist_short = np.maximum(prev_swing_high - close, 0.0)

    return le, lx, se, sx, sl_dist_long, sl_dist_short


# ── vectorbt helpers ─────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    g = SL_PARAM_GRID[sl_type]
    return [{"rr_ratio": rr, "sl_buffer_atr": buf}
            for rr, buf in product(g["rr_ratio"], g["sl_buffer_atr"])]


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
        if not lst: return [np.nan] * n_combos
        return (lst + [lst[-1]] * n_combos)[:n_combos]

    return pd.DataFrame({
        "sharpe":   _pad(sharpes),
        "trades":   trade_counts,
        "win_rate": win_rates,
        "max_dd":   _pad(max_dds),
    })


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_params_list, atr,
                       sl_dist_long, sl_dist_short, direction):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)
    safe_c    = np.where(close_arr > 0, close_arr, 1.0)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    # Per-direction swing distance
    if direction == "long":
        swing_dist = sl_dist_long
    elif direction == "short":
        swing_dist = sl_dist_short
    else:
        swing_dist = np.maximum(sl_dist_long, sl_dist_short)

    # SL = swing_dist + ATR × sl_buffer_atr; TP = SL × rr_ratio
    sl_2d = np.column_stack([
        np.clip((swing_dist + atr * p["sl_buffer_atr"]) / safe_c, 1e-6, 1.0)
        for p in sl_params_list
    ])
    tp_2d = np.column_stack([
        np.clip((swing_dist + atr * p["sl_buffer_atr"]) * p["rr_ratio"] / safe_c, 1e-6, 5.0)
        for p in sl_params_list
    ])

    pf = vbt.Portfolio.from_signals(
        close=close_series,
        entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
        short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
        sl_stop=sl_2d, tp_stop=tp_2d,
        init_cash=1_000_000, fees=0.0005, freq="5min",
    )

    return _extract_pf_stats(pf, n_combos)


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type):
    h = data.High.values; l = data.Low.values; c = data.Close.values
    idx     = data.index
    close_s = pd.Series(c, index=idx)
    sl_list = _build_sl_params_list(sl_type)

    atr   = _compute_atr(h, l, c)
    ema50 = _compute_ema(c, 50)
    ema200 = _compute_ema(c, 200)

    sess_cache:  dict = {}
    signal_cache: dict = {}

    best_sharpe = -np.inf
    best_result = None
    ip = INDICATOR_PARAMS

    for (lb, sw_lb, wait, bias, sess) in product(
        ip["lookback_bars"], ip["swing_lookback"],
        ip["max_ltf_wait_bars"], ip["use_bias_filter"], ip["session_mode"]
    ):
        # Actual signal only varies with (lb, bias, sess); sw_lb and wait are noted params
        sig_key = (lb, bias, sess)
        if sig_key not in signal_cache:
            signal_cache[sig_key] = _make_signals(
                h, l, c, atr, ema50, ema200, idx,
                lb, bias, sess, direction
            )
        le, lx, se, sx, sd_long, sd_short = signal_cache[sig_key]

        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(
                close_s, le, lx, se, sx, sl_list, atr,
                sl_dist_long=sd_long, sl_dist_short=sd_short, direction=direction,
            )
        except Exception:
            continue

        for row_idx, sl_p in enumerate(sl_list):
            if row_idx >= len(stats_df):
                continue
            row      = stats_df.iloc[row_idx]
            sharpe   = float(row["sharpe"])   if np.isfinite(row.get("sharpe",   np.nan)) else -np.inf
            n_trades = int(row["trades"])
            wr       = float(row["win_rate"]) if np.isfinite(row.get("win_rate", 0.0))    else 0.0
            dd       = float(row["max_dd"])   if np.isfinite(row.get("max_dd",   np.nan)) else 0.0

            if n_trades < 30:
                continue
            if sharpe > best_sharpe:
                best_sharpe = sharpe
                best_result = (
                    {
                        "lookback_bars":     lb,
                        "swing_lookback":    sw_lb,
                        "max_ltf_wait_bars": wait,
                        "use_bias_filter":   bias,
                        "session_mode":      sess,
                        "direction":         direction,
                        **sl_p,
                    },
                    sharpe, n_trades, wr, dd,
                )

    return best_result


def _eval_single(data, direction, sl_type, best_params):
    h = data.High.values; l = data.Low.values; c = data.Close.values
    idx     = data.index
    close_s = pd.Series(c, index=idx)
    try:
        atr    = _compute_atr(h, l, c)
        ema50  = _compute_ema(c, 50)
        ema200 = _compute_ema(c, 200)

        le, lx, se, sx, sd_long, sd_short = _make_signals(
            h, l, c, atr, ema50, ema200, idx,
            best_params["lookback_bars"],
            best_params["use_bias_filter"],
            best_params["session_mode"],
            direction,
        )

        sl_list = [{"rr_ratio":      best_params["rr_ratio"],
                    "sl_buffer_atr": best_params["sl_buffer_atr"]}]

        stats_df = _run_vbt_portfolio(
            close_s, le, lx, se, sx, sl_list, atr,
            sl_dist_long=sd_long, sl_dist_short=sd_short, direction=direction,
        )
        row = stats_df.iloc[0]
        sharpe   = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        n_trades = int(row["trades"])
        return sharpe, n_trades
    except Exception as e:
        print(f"    _eval_single error: {e}", flush=True)
        return None, 0


# ── Worker ────────────────────────────────────────────────────────────────────

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
        data = engine.get_data(symbol_usdt, TimeFrame.M5,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        return _make_result(symbol_usdt, direction, sl_type, note=f"DATA ERROR: {e}")

    if data.empty or len(data) < 5000:
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
    print(f"Pre-downloading {len(symbols)} symbols (5m) — this may take a while...")
    for sym in symbols:
        symbol_usdt = sym + "USDT"
        try:
            d = engine.get_data(symbol_usdt, TimeFrame.M5, start, end)
            print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
        except Exception as e:
            print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description="SFP1 Stage 1 v2 parallel optimization")
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
                fname = f"{symbol_usdt}_5m_{direction}_{sl_type}.json"
                fpath = RESULTS_DIR / fname
                if fpath.exists():
                    try:
                        d = json.loads(fpath.read_text())
                        if any(k in str(d.get("note", "")) for k in ("WORKER CRASH", "OPT ERROR", "DATA ERROR")):
                            all_tasks.append((sym, direction, sl_type))
                            continue
                    except Exception:
                        pass
                    skipped += 1
                else:
                    all_tasks.append((sym, direction, sl_type))

    total = len(SYMBOLS) * len(DIRECTIONS) * len(SL_TYPES)
    print(f"SFP1 Stage 1 v2 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do.")
        return

    done = skipped
    passed = 0
    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fpath = RESULTS_DIR / f"{symbol_usdt}_5m_{direction}_{sl_type}.json"
                if fpath.exists():
                    try:
                        if json.loads(fpath.read_text()).get("verdict") == "PASS":
                            passed += 1
                    except Exception:
                        pass

    remaining = list(all_tasks)
    while remaining:
        batch     = remaining[:]
        remaining = []
        try:
            with ProcessPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(_worker_v2, task): task for task in batch}
                for future in as_completed(futures):
                    task = futures[future]
                    sym, direction, sl_type = task
                    symbol_usdt = sym + "USDT"
                    fname = f"{symbol_usdt}_5m_{direction}_{sl_type}.json"
                    fpath = RESULTS_DIR / fname
                    try:
                        result = future.result()
                    except BrokenExecutor:
                        for t, fut in futures.items():
                            if not fut.done():
                                remaining.append(futures[fut])
                        break
                    except Exception as e:
                        result = _make_result(symbol_usdt, direction, sl_type,
                                              note=f"WORKER CRASH: {e}")
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
