#!/usr/bin/env python3
"""
DC1 Stage 3 optimization — DOW filter (PARALLEL).

Tests 8 day-of-week entry masks on Stage 2 passing combos.
Entry signals are zeroed on non-matching DOW bars; SL/TP and signal exits
active on all bars.

Usage:
    python run_dc1_stage3_parallel_v2.py
    python run_dc1_stage3_parallel_v2.py --workers 8
    python run_dc1_stage3_parallel_v2.py --skip-download
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

STRATEGY_ID  = "DC1"
STRATEGY_KEY = "dc1_donchian_channel"
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


# ── Indicators ────────────────────────────────────────────────────────────────

def _compute_donchian(high, low, donchian_length):
    """Upper = rolling max of high shifted by 1; lower = rolling min of low shifted by 1."""
    h, l = pd.Series(high), pd.Series(low)
    upper = h.rolling(donchian_length).max().shift(1).ffill().bfill().values
    lower = l.rolling(donchian_length).min().shift(1).ffill().bfill().values
    return upper, lower


def _compute_adx_and_atr(high, low, close, period):
    """Returns (adx, atr) arrays using Wilder ewm approximation."""
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    up, down = h.diff(), -l.diff()
    pdm  = np.where((up > down) & (up > 0), up, 0.0)
    mdm  = np.where((down > up) & (down > 0), down, 0.0)
    tr   = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    alpha = 1.0 / period
    tr_s  = tr.ewm(alpha=alpha, adjust=False).mean() * period
    pdm_s = pd.Series(pdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    mdm_s = pd.Series(mdm, index=h.index).ewm(alpha=alpha, adjust=False).mean() * period
    with np.errstate(divide='ignore', invalid='ignore'):
        pdi = 100.0 * pdm_s / tr_s
        mdi = 100.0 * mdm_s / tr_s
        dx  = 100.0 * (pdi - mdi).abs() / (pdi + mdi)
    dx  = dx.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    adx = dx.ewm(alpha=alpha, adjust=False).mean().fillna(0.0).values.astype(np.float64)
    atr = tr.ewm(alpha=alpha, adjust=False).mean().fillna(0.0).values.astype(np.float64)
    return adx, atr


def _compute_vol_sma(volume, period):
    return pd.Series(volume).rolling(period, min_periods=1).mean().fillna(0).values.astype(np.float64)


# ── Signals ───────────────────────────────────────────────────────────────────

def _make_signals(close, dc_upper, dc_lower, adx, vol, vol_sma,
                  adx_threshold, adx_exit, vol_mult, direction):
    """
    DC1 signals with ADX trend + volume filter.
    Signal exit when ADX drops below adx_exit (trend fading).
    """
    n = len(close)
    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    adx_strong  = adx > adx_threshold
    vol_confirm = vol > vol_sma * vol_mult
    valid_dc    = ~(np.isnan(dc_upper) | np.isnan(dc_lower))

    adx_exit_signal = adx < adx_exit

    if direction in ("long", "both"):
        le = valid_dc & (close > dc_upper) & adx_strong & vol_confirm
        lx = adx_exit_signal
    if direction in ("short", "both"):
        se = valid_dc & (close < dc_lower) & adx_strong & vol_confirm
        sx = adx_exit_signal

    return le, lx, se, sx


# ── vectorbt portfolio ────────────────────────────────────────────────────────

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


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_type, sl_params_list, atr, freq="1h"):
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
        if dow_days is not None:
            dow_bool = np.isin(close_s.index.dayofweek, list(dow_days))
            le = le_base & dow_bool
            se = se_base & dow_bool
        else:
            le = le_base
            se = se_base

        if sl_type in ("embedded", "atr"):
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct":   best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
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
    vol_t     = test_data.Volume.values
    close_s_t = pd.Series(c_t, index=test_data.index)
    try:
        dc_upper_t, dc_lower_t = _compute_donchian(h_t, l_t, best_params["donchian_length"])
        adx_t, atr_t = _compute_adx_and_atr(h_t, l_t, c_t, best_params["atr_period"])
        vol_sma_t    = _compute_vol_sma(vol_t, best_params["vol_avg_period"])
        le_t, lx_t, se_t, sx_t = _make_signals(
            c_t, dc_upper_t, dc_lower_t, adx_t, vol_t, vol_sma_t,
            best_params["adx_threshold"], best_params["adx_exit"],
            best_params["vol_mult"], direction,
        )
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
        description="DC1 Stage 3 — DOW filter (15m, 1h, 12h off-TFs)")
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
