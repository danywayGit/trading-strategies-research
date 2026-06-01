#!/usr/bin/env python3
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

import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product

import numba
import vectorbt as vbt

STRATEGY_ID  = "SWING3"
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

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]
LIMITED_DATA = {"ENA", "TAO"}

# Indicator params that drive the 81-combo outer loop (same values as v1)
INDICATOR_PARAMS = {
    "st_period":     [7, 10, 14],
    "st_factor":     [2.0, 3.0, 4.0],
    "adx_threshold": [20, 25, 30],
    "ema_filter":    [50, 100, 200],
}

# SL-only params swept as vectorbt columns (inner dimension per vbt call)
SL_PARAM_GRID = {
    "embedded":     {"atr_stop_mult":   [1.5, 2.5, 3.5]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.5, 3.5],
                     "take_profit_pct": [3.0, 6.0, 9.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.5, 3.5],
                     "take_profit_pct": [3.0, 6.0, 9.0]},
    "atr":          {"atr_stop_mult":   [1.5, 2.5, 3.5],
                     "rr_ratio":        [1.5, 2.5, 3.5]},
}


# ── Shared helpers ────────────────────────────────────────────────────────────

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


# ── Indicator helpers ─────────────────────────────────────────────────────────

@numba.njit(cache=True)
def _supertrend_loop(close, upper_band, lower_band):
    """Iterative Supertrend state machine — compiled to native code by numba."""
    n = len(close)
    direction = np.empty(n, dtype=np.float64)
    st_level  = np.empty(n, dtype=np.float64)
    direction[:] = np.nan
    st_level[:] = np.nan

    start = 0
    for i in range(n):
        if not np.isnan(upper_band[i]) and not np.isnan(lower_band[i]):
            start = i
            break

    direction[start] = -1.0          # start bullish
    st_level[start]  = lower_band[start]

    for i in range(start + 1, n):
        ub = upper_band[i]
        lb = lower_band[i]
        c  = close[i]
        if np.isnan(ub) or np.isnan(lb):
            direction[i] = direction[i - 1]
            st_level[i]  = st_level[i - 1]
            continue
        prev_dir   = direction[i - 1]
        prev_level = st_level[i - 1]
        if prev_dir == -1.0:                  # currently bullish
            curr_lb = max(lb, prev_level)
            if c < curr_lb:
                direction[i] =  1.0           # flip bearish
                st_level[i]  = ub
            else:
                direction[i] = -1.0
                st_level[i]  = curr_lb
        else:                                  # currently bearish
            curr_ub = min(ub, prev_level)
            if c > curr_ub:
                direction[i] = -1.0           # flip bullish
                st_level[i]  = lb
            else:
                direction[i] =  1.0
                st_level[i]  = curr_ub

    return direction, st_level


def _compute_supertrend(high, low, close, period, factor):
    """
    Returns (direction, st_level, atr) as float64 numpy arrays.
    direction: -1 = bullish (price above ST), +1 = bearish (price below ST).
    Matches the convention used in SWING3 strategy class.
    ATR is simple rolling mean of True Range — same as backtesting.py SWING3.
    """
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    hl2 = (h + l) / 2.0
    tr  = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs(),
    ], axis=1).max(axis=1)
    atr   = tr.rolling(period).mean().values
    upper = (hl2 + factor * pd.Series(atr)).values
    lower = (hl2 - factor * pd.Series(atr)).values

    direction, st_level = _supertrend_loop(
        close.astype(np.float64),
        upper.astype(np.float64),
        lower.astype(np.float64),
    )
    return direction, st_level, atr


def _compute_adx(high, low, close, period=14):
    """
    Wilder-smoothed ADX via pandas ewm (alpha=1/period).
    Close approximation — differs from exact Wilder init only in first ~100 bars.
    Returns float64 numpy array same length as input.
    """
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    up, down = h.diff(), -l.diff()
    pdm  = np.where((up > down) & (up > 0), up, 0.0)
    mdm  = np.where((down > up) & (down > 0), down, 0.0)
    tr   = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs(),
    ], axis=1).max(axis=1)
    alpha = 1.0 / period
    tr_s  = tr.ewm(alpha=alpha, adjust=False).mean() * period
    pdm_s = pd.Series(pdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    mdm_s = pd.Series(mdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    with np.errstate(divide='ignore', invalid='ignore'):
        pdi = 100.0 * pdm_s / tr_s
        mdi = 100.0 * mdm_s / tr_s
        dx  = 100.0 * (pdi - mdi).abs() / (pdi + mdi)
    dx  = dx.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    adx = dx.ewm(alpha=alpha, adjust=False).mean()
    return adx.fillna(0.0).values.astype(np.float64)


def _compute_ema(close, period):
    return pd.Series(close).ewm(span=period, adjust=False).mean().values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(st_dir, adx, ema, close, adx_threshold, direction):
    """
    Generate boolean entry/exit arrays for vectorbt.
    Returns (long_entries, long_exits, short_entries, short_exits) — 1D bool, length n.
    Index 0 is always False (no previous bar available for flip detection).

    Supertrend convention (matches SWING3 strategy):
      st_dir == -1  ->  bullish (price above Supertrend)
      st_dir == +1  ->  bearish (price below Supertrend)
    """
    n  = len(close)
    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    prev  = st_dir[:-1]
    curr  = st_dir[1:]
    valid = ~(np.isnan(prev) | np.isnan(curr))

    flip_bull = valid & (curr == -1.0) & (prev ==  1.0)   # bearish -> bullish
    flip_bear = valid & (curr ==  1.0) & (prev == -1.0)   # bullish -> bearish

    adx_ok    = adx[1:]   > adx_threshold
    above_ema = close[1:] > ema[1:]
    below_ema = close[1:] < ema[1:]

    if direction in ("long", "both"):
        le[1:] = flip_bull & adx_ok & above_ema
        lx[1:] = flip_bear

    if direction in ("short", "both"):
        se[1:] = flip_bear & adx_ok & below_ema
        sx[1:] = flip_bull

    return le, lx, se, sx


# ── vectorbt portfolio ────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    """Return list of dicts, one per SL combo for the given sl_type."""
    g = SL_PARAM_GRID[sl_type]
    if sl_type == "embedded":
        return [{"atr_stop_mult": m} for m in g["atr_stop_mult"]]
    if sl_type in ("fixed_pct", "fixed_signal"):
        return [
            {"stop_loss_pct": sl, "take_profit_pct": tp}
            for sl, tp in product(g["stop_loss_pct"], g["take_profit_pct"])
        ]
    if sl_type == "atr":
        return [
            {"atr_stop_mult": m, "rr_ratio": r}
            for m, r in product(g["atr_stop_mult"], g["rr_ratio"])
        ]
    raise ValueError(f"Unknown sl_type: {sl_type}")


def _extract_pf_stats(pf, n_combos):
    """
    Extract per-column [sharpe, trades, win_rate, max_dd] from a vectorbt Portfolio.
    Handles both single-column (returns scalar) and multi-column (returns Series) cases.
    """
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

    # Trade count and win rate from the trades records DataFrame (vectorbt 0.28.x)
    trade_counts = [0] * n_combos
    win_rates    = [0.0] * n_combos
    try:
        records = pf.trades.records          # pd.DataFrame in vectorbt 0.28.x
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


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_type, sl_params_list, atr, freq="1h"):
    """
    Single vbt.Portfolio.from_signals() call evaluating all SL combos as columns.

    close_series  : pd.Series with DatetimeIndex
    le/lx/se/sx   : 1D bool numpy arrays (long/short entries/exits)
    sl_type       : "embedded" | "fixed_pct" | "fixed_signal" | "atr"
    sl_params_list: list of dicts from _build_sl_params_list()
    atr           : 1D float64 ATR array (same length as close)

    Returns DataFrame (n_combos rows) with columns: sharpe, trades, win_rate, max_dd.
    """
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)

    # Tile signal arrays to (n_bars, n_combos) — one column per SL combo
    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(
        close=close_series,
        init_cash=1_000_000,
        fees=0.0005,
        freq=freq,
    )

    if sl_type == "embedded":
        # ATR-based hard stop expressed as a fraction of close at each bar.
        # vectorbt picks the value at the entry bar — close approximation of entry price.
        sl_2d = np.column_stack([
            np.clip(
                np.where(close_arr > 0, atr * p["atr_stop_mult"] / close_arr, 0.05),
                1e-6, 1.0,
            )
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_2d,
        )

    elif sl_type == "fixed_pct":
        # Fixed % SL/TP — signal exits suppressed (backtesting.py fixed_pct behaviour)
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d,
            exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d,
            short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_arr,
            tp_stop=tp_arr,
        )

    elif sl_type == "fixed_signal":
        # Fixed % SL/TP + Supertrend signal exits remain active
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_arr,
            tp_stop=tp_arr,
        )

    elif sl_type == "atr":
        # ATR-based SL with fixed RR target — no signal exits
        sl_2d = np.column_stack([
            np.clip(
                np.where(close_arr > 0, atr * p["atr_stop_mult"] / close_arr, 0.05),
                1e-6, 1.0,
            )
            for p in sl_params_list
        ])
        tp_2d = np.column_stack([
            np.clip(
                np.where(close_arr > 0, atr * p["atr_stop_mult"] * p["rr_ratio"] / close_arr, 0.1),
                1e-6, 5.0,
            )
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d,
            exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d,
            short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_2d,
            tp_stop=tp_2d,
        )

    else:
        raise ValueError(f"Unknown sl_type: {sl_type}")

    return _extract_pf_stats(pf, n_combos)


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type, freq="1h"):
    """
    Loop over 81 unique indicator-param combos. For each:
      1. Compute indicators ONCE (Supertrend, ADX, EMA, ATR)
      2. Call _run_vbt_portfolio() for all SL variants simultaneously
      3. Track best combo by Sharpe (subject to >= 30 trades)

    Returns (best_params, best_sharpe, best_trades, best_win_rate, best_max_dd)
    or None if no combo produces >= 30 trades.
    """
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    ip = INDICATOR_PARAMS

    # ADX period is fixed at 14 for all combos — compute once
    adx_precomp = _compute_adx(h, l, c)

    # EMA only varies with ema_filter (3 unique values) — cache by period
    ema_cache: dict = {}

    # Supertrend varies with (st_period, st_factor) — 9 unique pairs
    st_cache: dict = {}

    for st_period, st_factor, adx_threshold, ema_filter in product(
        ip["st_period"], ip["st_factor"], ip["adx_threshold"], ip["ema_filter"]
    ):
        st_key = (st_period, st_factor)
        if st_key not in st_cache:
            st_cache[st_key] = _compute_supertrend(h, l, c, st_period, st_factor)
        st_dir, _, atr = st_cache[st_key]

        adx = adx_precomp

        if ema_filter not in ema_cache:
            ema_cache[ema_filter] = _compute_ema(c, ema_filter)
        ema = ema_cache[ema_filter]

        le, lx, se, sx  = _make_signals(st_dir, adx, ema, c, adx_threshold, direction)

        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr, freq=freq)
        except Exception as e:
            print(f"    vbt error ({st_period},{st_factor},{adx_threshold},{ema_filter}): {e}",
                  flush=True)
            continue

        for row_idx, sl_p in enumerate(sl_list):
            if row_idx >= len(stats_df):
                continue
            row = stats_df.iloc[row_idx]
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
                        "st_period":     st_period,
                        "st_factor":     st_factor,
                        "adx_threshold": adx_threshold,
                        "ema_filter":    ema_filter,
                        "direction":     direction,
                        **sl_p,
                    },
                    sharpe, n_trades, wr, dd,
                )

    return best_result


def _eval_single(data, direction, sl_type, best_params, freq="1h"):
    """
    Evaluate one parameter set on a data slice (the OOS test window).
    Returns (oos_sharpe, oos_trades) or (None, 0) on error.
    """
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)

    try:
        st_dir, _, atr = _compute_supertrend(h, l, c,
                                              best_params["st_period"],
                                              best_params["st_factor"])
        adx = _compute_adx(h, l, c)
        ema = _compute_ema(c, best_params["ema_filter"])
        le, lx, se, sx = _make_signals(st_dir, adx, ema, c,
                                        best_params["adx_threshold"], direction)

        if sl_type == "embedded":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct":   best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        elif sl_type == "atr":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")

        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr, freq=freq)
        row = stats_df.iloc[0]
        sharpe   = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        n_trades = int(row["trades"])
        return sharpe, n_trades
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

    print(f"{log_prefix} optimizing ({len(train_data)} train bars)...", flush=True)
    try:
        opt = _optimize_vbt(train_data, direction, sl_type, freq=TF_FREQ_MAP[tf])
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

    oos_sharpe, _ = _eval_single(test_data, direction, sl_type, best_params, freq=TF_FREQ_MAP[tf])
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
    from multiprocessing import freeze_support
    freeze_support()
    main()
