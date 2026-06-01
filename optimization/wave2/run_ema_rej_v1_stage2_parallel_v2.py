#!/usr/bin/env python3
"""
EMA_REJ_V1 Stage 2 optimization — off-TF expansion (PARALLEL).

Runs full param-grid re-optimization on the 3 off-timeframes (15m, 4h, 12h)
for all EMA_REJ_V1 Stage 1 combos with OOS Sharpe >= 0.5.

Usage:
    python run_ema_rej_v1_stage2_parallel_v2.py
    python run_ema_rej_v1_stage2_parallel_v2.py --workers 8
    python run_ema_rej_v1_stage2_parallel_v2.py --skip-download
"""
import sys
import os
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage2_utils import run_stage2_parallel

import argparse
import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product

import vectorbt as vbt

STRATEGY_ID  = "EMA_REJ_V1"
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
HTF_BARS = 9   # fixed: 9 × 1H ≈ 9H HTF approximation (not swept)

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]
LIMITED_DATA = {"ENA", "TAO"}

INDICATOR_PARAMS = {
    "ema200_length":      [150, 200, 250],
    "rejection_lookback": [5, 10, 15],
    "rsi_period":         [10, 14],
    "rsi_ema_period":     [7, 9, 14],
    "rsi_confirm_window": [2, 3, 5],
}

SL_PARAM_GRID = {
    "embedded":     {"atr_stop_mult":   [2.0, 3.0, 4.0],
                     "rr_ratio":        [1.5, 2.0, 2.5, 3.0]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 5.0, 6.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 5.0, 6.0]},
    "atr":          {"atr_stop_mult":   [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
                     "rr_ratio":        [1.5, 2.0, 2.5, 3.0]},
}


# ── Shared helpers ────────────────────────────────────────────────────────────

def _make_result(symbol, direction, sl_type, tf, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy":         "ema_rejection_v1",
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


# ── Indicators ────────────────────────────────────────────────────────────────

def _compute_ema(close, period):
    return pd.Series(close).ewm(span=period, adjust=False).mean().values.astype(np.float64)


def _compute_rsi(close, period):
    s = pd.Series(close)
    delta = s.diff()
    gain  = delta.clip(lower=0).ewm(alpha=1.0 / period, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(alpha=1.0 / period, adjust=False).mean()
    rs    = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50).values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean().fillna(0).values.astype(np.float64)


def _within_last_n(events, n):
    """True if any True in the last n bars (including current bar)."""
    return pd.Series(events.astype(float)).rolling(n, min_periods=1).max().fillna(0).values.astype(bool)


# ── Signals ───────────────────────────────────────────────────────────────────

def _make_signals(close, ema200, htf_ema, rsi, rsi_ema,
                  rejection_lookback, rsi_confirm_window, direction):
    """
    EMA rejection: price briefly crossed EMA200 then returned.
    Long:  HTF uptrend + was cross_below recently + now cross_above + RSI recently crossed up
    Short: HTF downtrend + was cross_above recently + now cross_below + RSI recently crossed down
    No signal exits — SL/TP only.
    """
    n = len(close)

    # Detect EMA200 crosses (bar-by-bar)
    cross_above = np.zeros(n, dtype=bool)
    cross_below = np.zeros(n, dtype=bool)
    cross_above[1:] = (close[:-1] < ema200[:-1]) & (close[1:] >= ema200[1:])
    cross_below[1:] = (close[:-1] > ema200[:-1]) & (close[1:] <= ema200[1:])

    # RSI EMA crosses
    rsi_x_up   = np.zeros(n, dtype=bool)
    rsi_x_dn   = np.zeros(n, dtype=bool)
    rsi_x_up[1:] = (rsi[:-1] < rsi_ema[:-1]) & (rsi[1:] >= rsi_ema[1:])
    rsi_x_dn[1:] = (rsi[:-1] > rsi_ema[:-1]) & (rsi[1:] <= rsi_ema[1:])

    # Rolling window: "did X happen within last N bars?"
    had_cross_above = _within_last_n(cross_above, rejection_lookback)
    had_cross_below = _within_last_n(cross_below, rejection_lookback)
    had_rsi_up      = _within_last_n(rsi_x_up,   rsi_confirm_window)
    had_rsi_dn      = _within_last_n(rsi_x_dn,   rsi_confirm_window)

    htf_uptrend   = close > htf_ema
    htf_downtrend = close < htf_ema

    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    if direction in ("long", "both"):
        # Price crossed below EMA200 recently, now crosses back above (failed breakdown)
        le = htf_uptrend & cross_above & had_cross_below & had_rsi_up
    if direction in ("short", "both"):
        # Price crossed above EMA200 recently, now crosses back below (failed recovery)
        se = htf_downtrend & cross_below & had_cross_above & had_rsi_dn

    return le, lx, se, sx


# ── vectorbt portfolio ────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    g = SL_PARAM_GRID[sl_type]
    if sl_type in ("embedded", "atr"):
        return [{"atr_stop_mult": m, "rr_ratio": r}
                for m, r in product(g["atr_stop_mult"], g["rr_ratio"])]
    if sl_type in ("fixed_pct", "fixed_signal"):
        return [{"stop_loss_pct": sl, "take_profit_pct": tp}
                for sl, tp in product(g["stop_loss_pct"], g["take_profit_pct"])]
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
                       sl_type, sl_params_list, atr, freq="1h"):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq=freq)

    if sl_type in ("embedded", "atr"):
        sl_2d = np.column_stack([
            np.clip(np.where(close_arr > 0, atr * p["atr_stop_mult"] / close_arr, 0.05), 1e-6, 1.0)
            for p in sl_params_list
        ])
        tp_2d = np.column_stack([
            np.clip(np.where(close_arr > 0, atr * p["atr_stop_mult"] * p["rr_ratio"] / close_arr, 0.1), 1e-6, 5.0)
            for p in sl_params_list
        ])
        exits_arg = lx_2d if sl_type == "embedded" else np.zeros_like(le_2d, dtype=bool)
        sx_arg    = sx_2d if sl_type == "embedded" else np.zeros_like(se_2d, dtype=bool)
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=exits_arg,
            short_entries=se_2d, short_exits=sx_arg,
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
    else:
        raise ValueError(f"Unknown sl_type: {sl_type}")

    return _extract_pf_stats(pf, n_combos)


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type, atr_precomp, freq="1h"):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    # Cache indicators by their shape-determining params
    ema200_cache: dict = {}
    rsi_cache: dict    = {}

    ip = INDICATOR_PARAMS
    for ema200_length, rejection_lookback, rsi_period, rsi_ema_period, rsi_confirm_window in product(
        ip["ema200_length"], ip["rejection_lookback"],
        ip["rsi_period"],    ip["rsi_ema_period"],
        ip["rsi_confirm_window"],
    ):
        if ema200_length not in ema200_cache:
            ema200_cache[ema200_length] = (
                _compute_ema(c, ema200_length),
                _compute_ema(c, max(2, int(ema200_length * HTF_BARS))),
            )
        ema200_arr, htf_ema_arr = ema200_cache[ema200_length]

        rsi_key = (rsi_period, rsi_ema_period)
        if rsi_key not in rsi_cache:
            rsi_v = _compute_rsi(c, rsi_period)
            rsi_cache[rsi_key] = (rsi_v, _compute_ema(rsi_v, rsi_ema_period))
        rsi_arr, rsi_ema_arr = rsi_cache[rsi_key]

        le, lx, se, sx = _make_signals(
            c, ema200_arr, htf_ema_arr, rsi_arr, rsi_ema_arr,
            rejection_lookback, rsi_confirm_window, direction,
        )
        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr_precomp, freq=freq)
        except Exception as e:
            print(f"    vbt error: {e}", flush=True)
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
                    "ema200_length":      ema200_length,
                    "rejection_lookback": rejection_lookback,
                    "rsi_period":         rsi_period,
                    "rsi_ema_period":     rsi_ema_period,
                    "rsi_confirm_window": rsi_confirm_window,
                    "htf_bars":           HTF_BARS,
                    "direction":          direction,
                    **sl_p,
                },
                sharpe, n_trades, wr, dd,
            )

    return best_result


def _eval_single(data, direction, sl_type, best_params, atr, freq="1h"):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    try:
        ema200_arr  = _compute_ema(c, best_params["ema200_length"])
        htf_ema_arr = _compute_ema(c, max(2, int(best_params["ema200_length"] * HTF_BARS)))
        rsi_arr     = _compute_rsi(c, best_params["rsi_period"])
        rsi_ema_arr = _compute_ema(rsi_arr, best_params["rsi_ema_period"])
        le, lx, se, sx = _make_signals(
            c, ema200_arr, htf_ema_arr, rsi_arr, rsi_ema_arr,
            best_params["rejection_lookback"], best_params["rsi_confirm_window"], direction,
        )
        if sl_type in ("embedded", "atr"):
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio": best_params["rr_ratio"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct": best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")
        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr, freq=freq)
        row = stats_df.iloc[0]
        sharpe = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        return sharpe, int(row["trades"])
    except Exception as e:
        print(f"    _eval_single error: {e}", flush=True)
        return None, 0


# ── Worker ────────────────────────────────────────────────────────────────────

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

    # ATR fixed at period=14, computed once per data slice
    atr_train = _compute_atr(train_data.High.values, train_data.Low.values, train_data.Close.values)
    atr_test  = _compute_atr(test_data.High.values,  test_data.Low.values,  test_data.Close.values)

    print(f"{log_prefix} optimizing ({len(train_data)} train bars)...", flush=True)
    try:
        opt = _optimize_vbt(train_data, direction, sl_type, atr_train, freq=TF_FREQ_MAP[tf])
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

    oos_sharpe, _ = _eval_single(test_data, direction, sl_type, best_params, atr_test, freq=TF_FREQ_MAP[tf])
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


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="EMA_REJ_V1 Stage 2 — off-TF expansion (15m, 4h, 12h)")
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
    from multiprocessing import freeze_support
    freeze_support()
    main()
