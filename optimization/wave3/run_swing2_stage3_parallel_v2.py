#!/usr/bin/env python3
"""
SWING2 Stage 3 optimization — DOW filter (PARALLEL).

Tests 8 day-of-week entry masks on Stage 2 passing combos.
Entry signals are zeroed on non-matching DOW bars; SL/TP active on all bars.

Usage:
    python run_swing2_stage3_parallel_v2.py
    python run_swing2_stage3_parallel_v2.py --workers 8
    python run_swing2_stage3_parallel_v2.py --skip-download
"""
import sys
import os
import argparse
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage3_utils import run_stage3_parallel, DOW_MASKS, select_winner

import numpy as np
import pandas as pd
from datetime import datetime

import vectorbt as vbt

STRATEGY_ID  = "SWING2"
STRATEGY_KEY = "swing2_bb_squeeze"
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

LIMITED_DATA = {"ENA", "TAO"}


# ── Shared helpers ────────────────────────────────────────────────────────────

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
    s             = pd.Series(close)
    ema_fast      = s.ewm(span=fast, adjust=False).mean()
    ema_slow      = s.ewm(span=slow, adjust=False).mean()
    macd_line     = ema_fast - ema_slow
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
    sl_params_list: list of dicts (one per SL combo)
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


# ── DOW evaluation ────────────────────────────────────────────────────────────

def _eval_single_dow(close_s, le_base, lx, se_base, sx, atr,
                     sl_type, best_params, dow_days, freq="1h"):
    """
    Evaluate pre-computed signals with DOW entry masking.
    le_base/se_base: unmasked entry signals from _make_signals.
    dow_days: set of weekday ints, or None for no filter (ALL mask).
    Returns (oos_sharpe, num_trades) or (None, 0) on error.
    """
    try:
        # Apply DOW masking to entry signals only
        if dow_days is not None:
            dow_bool = close_s.index.dayofweek.isin(dow_days).values
            le = le_base & dow_bool
            se = se_base & dow_bool
        else:
            le = le_base
            se = se_base

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
        row      = stats_df.iloc[0]
        sharpe   = float(row["sharpe"]) if np.isfinite(row.get("sharpe", np.nan)) else None
        n_trades = int(row["trades"])
        return sharpe, n_trades
    except Exception as e:
        print(f"    _eval_single_dow error: {e}", flush=True)
        return None, 0


# ── Worker ────────────────────────────────────────────────────────────────────

def _worker_v2(task):
    """
    Stage 3 worker. One process per Stage 2 passing combo.
    Runs _eval_single_dow for each of the 8 DOW masks, then selects winner.
    task = {"sym", "tf", "direction", "sl_type", "best_params", "stage2_oos_sharpe"}
    """
    sym               = task["sym"]
    tf                = task["tf"]
    direction         = task["direction"]
    sl_type           = task["sl_type"]
    best_params       = task["best_params"]
    stage2_oos_sharpe = task["stage2_oos_sharpe"]

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
        return {
            "strategy":          STRATEGY_KEY,
            "symbol":            symbol_usdt,
            "timeframe":         tf,
            "direction":         direction,
            "sl_type":           sl_type,
            "stage":             3,
            "best_params":       best_params,
            "stage2_oos_sharpe": stage2_oos_sharpe,
            "dow_results":       {},
            "winner_mask":       None,
            "winner_sharpe":     None,
            "winner_trades":     None,
            "dow_improved":      False,
            "note":              f"DATA ERROR: {e}",
        }

    if data.empty or len(data) < 500:
        return {
            "strategy":          STRATEGY_KEY,
            "symbol":            symbol_usdt,
            "timeframe":         tf,
            "direction":         direction,
            "sl_type":           sl_type,
            "stage":             3,
            "best_params":       best_params,
            "stage2_oos_sharpe": stage2_oos_sharpe,
            "dow_results":       {},
            "winner_mask":       None,
            "winner_sharpe":     None,
            "winner_trades":     None,
            "dow_improved":      False,
            "note":              "insufficient data",
        }

    test_data = data.iloc[int(len(data) * 0.7):]

    print(f"{log_prefix} running 8 DOW masks ({len(test_data)} OOS bars)...", flush=True)

    # Compute indicators once — DOW masking only affects entry signals
    h_t, l_t, c_t = test_data.High.values, test_data.Low.values, test_data.Close.values
    close_s_t = pd.Series(c_t, index=test_data.index)
    try:
        atr_t = _compute_atr(h_t, l_t, c_t, period=14)
        bb_upper_t, bb_lower_t, _ = _compute_bb(c_t, best_params["bb_length"], best_params["bb_mult"])
        macd_line_t, macd_sig_t   = _compute_macd(c_t, best_params["macd_fast"], best_params["macd_slow"])
        le_t, lx_t, se_t, sx_t = _make_signals(c_t, bb_upper_t, bb_lower_t,
                                                 macd_line_t, macd_sig_t, direction)
    except Exception as e:
        print(f"{log_prefix} INDICATOR ERROR: {e}", flush=True)
        return {
            "strategy":          STRATEGY_KEY,
            "symbol":            symbol_usdt,
            "timeframe":         tf,
            "direction":         direction,
            "sl_type":           sl_type,
            "stage":             3,
            "best_params":       best_params,
            "stage2_oos_sharpe": stage2_oos_sharpe,
            "dow_results":       {},
            "winner_mask":       None,
            "winner_sharpe":     None,
            "winner_trades":     None,
            "dow_improved":      False,
            "note":              f"INDICATOR ERROR: {e}",
        }

    dow_results = {}
    for mask_name, dow_days in DOW_MASKS.items():
        sharpe, trades = _eval_single_dow(
            close_s_t, le_t, lx_t, se_t, sx_t, atr_t,
            sl_type, best_params,
            dow_days=dow_days, freq=TF_FREQ_MAP[tf],
        )
        dow_results[mask_name] = {"oos_sharpe": sharpe, "num_trades": trades}

    winner_mask, winner_sharpe, winner_trades, dow_improved = select_winner(dow_results)
    print(
        f"{log_prefix} winner={winner_mask} sharpe={winner_sharpe} improved={dow_improved}",
        flush=True,
    )

    return {
        "strategy":          STRATEGY_KEY,
        "symbol":            symbol_usdt,
        "timeframe":         tf,
        "direction":         direction,
        "sl_type":           sl_type,
        "stage":             3,
        "best_params":       best_params,
        "stage2_oos_sharpe": stage2_oos_sharpe,
        "dow_results":       dow_results,
        "winner_mask":       winner_mask,
        "winner_sharpe":     winner_sharpe,
        "winner_trades":     winner_trades,
        "dow_improved":      dow_improved,
        "note":              note,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SWING2 Stage 3 — DOW filter (15m, 1h, 12h off-TFs)")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    run_stage3_parallel(
        strategy_id    = STRATEGY_ID,
        results_base   = RESULTS_BASE,
        worker_fn      = _worker_v2,
        backtesting_mcp= BACKTESTING_MCP,
        workers        = args.workers,
        skip_download  = args.skip_download,
    )


if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
