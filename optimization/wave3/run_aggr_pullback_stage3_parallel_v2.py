#!/usr/bin/env python3
"""
AGGR_PULLBACK Stage 3 optimization — DOW filter (PARALLEL).

Tests 8 day-of-week entry masks on Stage 2 passing combos.
Entry signals are zeroed on non-matching DOW bars; SL/TP active on all bars.

Usage:
    python run_aggr_pullback_stage3_parallel_v2.py
    python run_aggr_pullback_stage3_parallel_v2.py --workers 8
    python run_aggr_pullback_stage3_parallel_v2.py --skip-download
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

STRATEGY_ID  = "AGGR_PULLBACK"
STRATEGY_KEY = "aggr_pullback"
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


# ── Indicator helpers ─────────────────────────────────────────────────────────

def _compute_ema(close, period):
    return pd.Series(close).ewm(span=period, adjust=False).mean().values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, adjust=False).mean().values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(open_, high, low, close, atr, ema_short, ema200,
                  pullback_tolerance, swing_lookback, massive_candle_mult, direction):
    """Returns (le, lx, se, sx, swing_dist_long, swing_dist_short)."""
    n = len(close)

    prev_o = np.roll(open_, 1);  prev_o[0] = open_[0]
    prev_c = np.roll(close, 1);  prev_c[0] = close[0]
    prev_cl_c = np.roll(close, 1); prev_cl_c[0] = close[0]

    curr_green = close > open_
    prev_red   = prev_c < prev_o
    curr_red   = close < open_
    prev_green = prev_c > prev_o

    bullish_engulf = curr_green & prev_red & (close > prev_o) & (open_ <= prev_c)
    bearish_engulf = curr_red & prev_green & (close < prev_o) & (open_ >= prev_c)

    below_ema = (close < ema_short).astype(float)
    above_ema = (close > ema_short).astype(float)
    below_3 = pd.Series(below_ema).rolling(3, min_periods=1).sum().values
    above_3 = pd.Series(above_ema).rolling(3, min_periods=1).sum().values
    pb_ok_long  = below_3 <= pullback_tolerance
    pb_ok_short = above_3 <= pullback_tolerance

    roll_min_low  = pd.Series(low).rolling(swing_lookback, min_periods=1).min().values
    roll_max_high = pd.Series(high).rolling(swing_lookback, min_periods=1).max().values
    prev_min_low  = np.roll(roll_min_low,  1); prev_min_low[0]  = roll_min_low[0]
    prev_max_high = np.roll(roll_max_high, 1); prev_max_high[0] = roll_max_high[0]
    prev_low  = np.roll(low,  1); prev_low[0]  = low[0]
    prev_high = np.roll(high, 1); prev_high[0] = high[0]

    is_swing_low  = (low  <= roll_min_low)  | (prev_low  <= prev_min_low)
    is_swing_high = (high >= roll_max_high) | (prev_high >= prev_max_high)

    tr_bar = np.maximum(high - low,
                        np.maximum(np.abs(high - prev_cl_c), np.abs(low - prev_cl_c)))
    not_massive = tr_bar < atr * massive_candle_mult

    uptrend   = (close > ema_short) & (close > ema200)
    downtrend = (close < ema_short) & (close < ema200)

    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    if direction in ("long", "both"):
        le[1:] = (bullish_engulf & pb_ok_long  & is_swing_low  & not_massive & uptrend)[1:]

    if direction in ("short", "both"):
        se[1:] = (bearish_engulf & pb_ok_short & is_swing_high & not_massive & downtrend)[1:]

    swing_dist_long  = np.maximum(close - roll_min_low,  0.0)
    swing_dist_short = np.maximum(roll_max_high - close, 0.0)

    return le, lx, se, sx, swing_dist_long, swing_dist_short


# ── vectorbt helpers ─────────────────────────────────────────────────────────

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


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_type, sl_params_list, atr,
                       swing_dist_long=None, swing_dist_short=None, direction=None,
                       freq="1h"):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)
    safe_c    = np.where(close_arr > 0, close_arr, 1.0)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq=freq)

    if sl_type == "embedded":
        if direction == "long":
            swing_dist = swing_dist_long
        elif direction == "short":
            swing_dist = swing_dist_short
        else:
            swing_dist = np.maximum(swing_dist_long, swing_dist_short)

        sl_2d = np.column_stack([
            np.clip((swing_dist + atr * p["stop_mult"]) / safe_c, 1e-6, 1.0)
            for p in sl_params_list
        ])
        tp_2d = np.column_stack([
            np.clip((swing_dist + atr * p["stop_mult"]) * p["rr_ratio"] / safe_c, 1e-6, 5.0)
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_2d, tp_stop=tp_2d,
        )

    elif sl_type in ("fixed_pct", "fixed_signal"):
        sl_arr = np.array([p["stop_loss_pct"]   / 100.0 for p in sl_params_list])
        tp_arr = np.array([p["take_profit_pct"] / 100.0 for p in sl_params_list])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_arr, tp_stop=tp_arr,
        )

    elif sl_type == "atr":
        sl_2d = np.column_stack([
            np.clip(atr * p["atr_stop_mult"] / safe_c, 1e-6, 1.0)
            for p in sl_params_list
        ])
        tp_2d = np.column_stack([
            np.clip(atr * p["atr_stop_mult"] * p["rr_ratio"] / safe_c, 1e-6, 5.0)
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=np.zeros_like(le_2d, dtype=bool),
            short_entries=se_2d, short_exits=np.zeros_like(se_2d, dtype=bool),
            sl_stop=sl_2d, tp_stop=tp_2d,
        )

    else:
        raise ValueError(sl_type)

    return _extract_pf_stats(pf, n_combos)


# ── DOW evaluation ────────────────────────────────────────────────────────────

def _eval_single_dow(close_s, le_base, lx, se_base, sx, atr,
                     sl_type, best_params, dow_days, freq="1h",
                     swing_dist_long=None, swing_dist_short=None, direction=None):
    """
    Evaluate pre-computed signals with DOW entry masking.
    le_base/se_base: unmasked entry signals from _make_signals.
    dow_days: set of weekday ints, or None for no filter (ALL mask).
    swing_dist_long/short passed through to _run_vbt_portfolio for embedded SL.
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

        if sl_type == "embedded":
            sl_list = [{"stop_mult": best_params["stop_mult"],
                        "rr_ratio":  best_params["rr_ratio"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct":   best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        elif sl_type == "atr":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")

        stats_df = _run_vbt_portfolio(
            close_s, le, lx, se, sx, sl_type, sl_list, atr,
            swing_dist_long=swing_dist_long, swing_dist_short=swing_dist_short,
            direction=direction, freq=freq,
        )
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
    Runs _eval_single_dow for each DOW mask in DOW_MASKS (all non-empty subsets of Mon–Sun + ALL), then selects winner.
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

    print(f"{log_prefix} running {len(DOW_MASKS)} DOW masks ({len(test_data)} OOS bars)...", flush=True)

    # Compute indicators once — DOW masking only affects entry signals
    o_t = test_data.Open.values
    h_t, l_t, c_t = test_data.High.values, test_data.Low.values, test_data.Close.values
    close_s_t = pd.Series(c_t, index=test_data.index)
    try:
        atr_t  = _compute_atr(h_t, l_t, c_t)
        ema200_t = _compute_ema(c_t, 200)
        ema_s_t  = _compute_ema(c_t, best_params["ema_length"])
        le_t, lx_t, se_t, sx_t, sd_long_t, sd_short_t = _make_signals(
            o_t, h_t, l_t, c_t, atr_t, ema_s_t, ema200_t,
            best_params["pullback_tolerance"],
            best_params["swing_lookback"],
            best_params["massive_candle_mult"],
            direction,
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
            swing_dist_long=sd_long_t, swing_dist_short=sd_short_t,
            direction=direction,
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
        description="AGGR_PULLBACK Stage 3 — DOW filter (15m, 1h, 12h off-TFs)")
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
