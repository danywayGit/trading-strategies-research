#!/usr/bin/env python3
"""
SWING2 Stage 2 optimization — off-TF expansion (PARALLEL).

Runs full param-grid re-optimization on the 3 off-timeframes (15m, 1h, 12h)
for all SWING2 Stage 1 combos with OOS Sharpe >= 0.5.

Usage:
    python run_swing2_stage2_parallel_v2.py
    python run_swing2_stage2_parallel_v2.py --workers 8
    python run_swing2_stage2_parallel_v2.py --skip-download
"""
import sys
import os
import argparse
from pathlib import Path

# Must happen before any third-party imports so the venv is on sys.path
# regardless of which Python interpreter the user invokes the script with.
BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage2_utils import run_stage2_parallel

import numpy as np
import pandas as pd
from datetime import datetime
from itertools import product

import vectorbt as vbt

STRATEGY_ID  = "SWING2"
HOME_TF      = "4h"
RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
V2_NOTE      = "v2/vectorbt"

TF_MAP = {
    "15m": "M15",
    "1h":  "H1",
    "12h": "H12",
}

# Vectorbt freq strings for Sharpe annualization — must match the actual off-TF data
TF_FREQ_MAP = {
    "15m": "15min",
    "1h":  "1h",
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

# Indicator params that drive the 36-combo outer loop
INDICATOR_PARAMS = {
    "bb_length":   [15, 20, 25],
    "bb_mult":     [1.8, 2.0, 2.2],
    "macd_fast":   [10, 12],
    "macd_slow":   [24, 26],
}

# SL-only params swept as vectorbt columns (inner dimension per vbt call)
SL_PARAM_GRID = {
    "embedded":     {"atr_stop_mult": [2.0, 2.5, 3.0],
                     "rr_ratio":      [2.0, 2.5, 3.0]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "atr":          {"atr_stop_mult": [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
                     "rr_ratio":      [2.0, 2.5, 3.0]},
}


# ── Shared helpers ────────────────────────────────────────────────────────────

def _make_result(symbol, direction, sl_type, tf, best_params=None, train_sharpe=None,
                 oos_sharpe=None, num_trades=0, win_rate=None, max_dd=None,
                 verdict="FAIL", note=""):
    return {
        "strategy":         "swing2_bb_squeeze",
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

def _compute_bb(close, bb_length, bb_mult):
    """
    Bollinger Bands: rolling mean +/- bb_mult * rolling std over bb_length bars.
    Returns (bb_upper, bb_lower, bb_mid) as float64 numpy arrays.
    """
    s     = pd.Series(close)
    mid   = s.rolling(bb_length).mean()
    std   = s.rolling(bb_length).std(ddof=1)
    upper = (mid + bb_mult * std).values.astype(np.float64)
    lower = (mid - bb_mult * std).values.astype(np.float64)
    mid   = mid.values.astype(np.float64)
    return upper, lower, mid


def _compute_macd(close, fast, slow):
    """
    MACD: EWM fast/slow EMAs; macd_signal_line = EWM of (fast_ema - slow_ema).
    Signal period fixed at 9.
    Returns (macd_line, macd_signal_line) as float64 numpy arrays.
    """
    s            = pd.Series(close)
    ema_fast     = s.ewm(span=fast, adjust=False).mean()
    ema_slow     = s.ewm(span=slow, adjust=False).mean()
    macd_line    = ema_fast - ema_slow
    macd_sig_line = macd_line.ewm(span=9, adjust=False).mean()
    return macd_line.values.astype(np.float64), macd_sig_line.values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    """
    ATR: rolling mean of True Range over `period` bars.
    Returns float64 numpy array same length as input.
    """
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat([
        h - l,
        (h - c.shift()).abs(),
        (l - c.shift()).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean().values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(close, bb_upper, bb_lower, macd_line, macd_signal_line, direction):
    """
    Generate boolean entry/exit arrays for vectorbt.
    Returns (long_entries, long_exits, short_entries, short_exits) — 1D bool, length n.

    Long  entry: close > bb_upper AND macd_line > macd_signal_line
    Short entry: close < bb_lower AND macd_line < macd_signal_line
    No signal-based exits — SL/TP only.
    """
    n  = len(close)
    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    # Use current bar values (entry on bar close)
    bull_cond = (close > bb_upper) & (macd_line > macd_signal_line)
    bear_cond = (close < bb_lower) & (macd_line < macd_signal_line)

    if direction in ("long", "both"):
        le[:] = bull_cond

    if direction in ("short", "both"):
        se[:] = bear_cond

    return le, lx, se, sx


# ── vectorbt portfolio ────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    """Return list of dicts, one per SL combo for the given sl_type."""
    g = SL_PARAM_GRID[sl_type]
    if sl_type == "embedded":
        return [
            {"atr_stop_mult": m, "rr_ratio": r}
            for m, r in product(g["atr_stop_mult"], g["rr_ratio"])
        ]
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
        # ATR-based SL + RR-based TP — no signal exits.
        # SL fraction = atr * atr_stop_mult / close
        # TP fraction = atr * atr_stop_mult * rr_ratio / close
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

    elif sl_type in ("fixed_pct", "fixed_signal"):
        # Fixed % SL/TP — SWING2 has no signal-based exits (SL/TP only)
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
    Loop over 36 unique indicator-param combos (bb_length x bb_mult x macd_fast x macd_slow).
    For each:
      1. Compute indicators ONCE (BB, MACD); ATR computed once before the loop.
      2. Call _run_vbt_portfolio() for all SL variants simultaneously.
      3. Track best combo by Sharpe (subject to >= 30 trades).

    Caching strategy:
      - ATR: computed once (period=14, fixed)
      - BB: cached by (bb_length, bb_mult) — 9 unique pairs
      - MACD: cached by (macd_fast, macd_slow) — 4 unique pairs

    Returns (best_params, best_sharpe, best_trades, best_win_rate, best_max_dd)
    or None if no combo produces >= 30 trades.
    """
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    ip = INDICATOR_PARAMS

    # ATR period is fixed at 14 for all combos — compute once
    atr = _compute_atr(h, l, c, period=14)

    # Cache BB by (bb_length, bb_mult) — 9 unique pairs
    bb_cache: dict = {}

    # Cache MACD by (macd_fast, macd_slow) — 4 unique pairs
    macd_cache: dict = {}

    for bb_length, bb_mult, macd_fast, macd_slow in product(
        ip["bb_length"], ip["bb_mult"], ip["macd_fast"], ip["macd_slow"]
    ):
        bb_key = (bb_length, bb_mult)
        if bb_key not in bb_cache:
            bb_cache[bb_key] = _compute_bb(c, bb_length, bb_mult)
        bb_upper, bb_lower, _ = bb_cache[bb_key]

        macd_key = (macd_fast, macd_slow)
        if macd_key not in macd_cache:
            macd_cache[macd_key] = _compute_macd(c, macd_fast, macd_slow)
        macd_line, macd_signal_line = macd_cache[macd_key]

        le, lx, se, sx = _make_signals(c, bb_upper, bb_lower, macd_line, macd_signal_line, direction)

        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr, freq=freq)
        except Exception as e:
            print(f"    vbt error ({bb_length},{bb_mult},{macd_fast},{macd_slow}): {e}",
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
                        "bb_length":    bb_length,
                        "bb_mult":      bb_mult,
                        "macd_fast":    macd_fast,
                        "macd_slow":    macd_slow,
                        "squeeze_bars": 5,
                        "direction":    direction,
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
        atr = _compute_atr(h, l, c, period=14)
        bb_upper, bb_lower, _ = _compute_bb(c, best_params["bb_length"], best_params["bb_mult"])
        macd_line, macd_signal_line = _compute_macd(c, best_params["macd_fast"], best_params["macd_slow"])
        le, lx, se, sx = _make_signals(c, bb_upper, bb_lower, macd_line, macd_signal_line, direction)

        if sl_type == "embedded":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
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

    oos_sharpe, oos_trades = _eval_single(test_data, direction, sl_type, best_params, freq=TF_FREQ_MAP[tf])
    verdict = "PASS" if (oos_sharpe is not None and oos_sharpe > 0) else "FAIL"
    oos_str = f"{oos_sharpe:.4f}" if oos_sharpe is not None else "None"
    print(f"{log_prefix} OOS sharpe={oos_str} => {verdict}", flush=True)

    return _make_result(
        symbol_usdt, direction, sl_type, tf,
        best_params=best_params, train_sharpe=train_sharpe,
        oos_sharpe=oos_sharpe, num_trades=oos_trades,
        win_rate=win_rate, max_dd=max_dd,
        verdict=verdict, note=note,
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SWING2 Stage 2 — off-TF expansion (15m, 1h, 12h)")
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
