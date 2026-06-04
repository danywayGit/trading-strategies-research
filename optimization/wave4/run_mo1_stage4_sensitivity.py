#!/usr/bin/env python3
"""
MO1 Stage 4 — parameter sensitivity analysis (PARALLEL).

Nudges each numeric param in best_params ±10% and re-evaluates OOS Sharpe
with the Stage 3 winner DOW mask applied. Flags combos where any nudge
drops Sharpe by >20% (sensitive). Robust = no param is sensitive.

Usage:
    python run_mo1_stage4_sensitivity.py
    python run_mo1_stage4_sensitivity.py --workers 8
    python run_mo1_stage4_sensitivity.py --skip-download
"""
import sys
import os
import argparse
from pathlib import Path

BACKTESTING_MCP = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP")
sys.path.insert(0, str(BACKTESTING_MCP / "venv" / "Lib" / "site-packages"))
sys.path.insert(0, str(BACKTESTING_MCP))

from stage4_utils import run_sensitivity_parallel, nudge_params, SENSITIVITY_FILTER
sys.path.insert(0, str(Path(__file__).parent.parent / "wave3"))
from stage3_utils import DOW_MASKS

import numpy as np
import pandas as pd
from datetime import datetime

import vectorbt as vbt

STRATEGY_ID  = "MO1"
STRATEGY_KEY = "mo1_momentum_rotation"
RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
V2_NOTE      = "v2/vectorbt approx: per-asset RSI vs 50±threshold"

TF_MAP = {
    "15m": "M15",
    "1h":  "H1",
    "12h": "H12",
}

# Vectorbt freq strings for Sharpe annualization
TF_FREQ_MAP = {
    "15m": "15min",
    "1h":  "1h",
    "12h": "12h",
}

VENV_SITE_PACKAGES = BACKTESTING_MCP / "venv" / "Lib" / "site-packages"

LIMITED_DATA = {"ENA", "TAO"}


# ── Indicator helpers ─────────────────────────────────────────────────────────

def _compute_rsi(close, period):
    delta = pd.Series(close).diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_g = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_l = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    rs    = avg_g / avg_l.replace(0, np.nan)
    return (100.0 - 100.0 / (1.0 + rs)).fillna(50.0).values.astype(np.float64)


def _compute_adx(high, low, close, period=14):
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    up   = h.diff(); down = -l.diff()
    pdm  = np.where((up > down) & (up > 0), up, 0.0)
    mdm  = np.where((down > up) & (down > 0), down, 0.0)
    tr   = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    a    = 1.0 / period
    tr_s  = tr.ewm(alpha=a, adjust=False).mean() * period
    pdm_s = pd.Series(pdm, index=h.index).ewm(alpha=a, adjust=False).mean() * period
    mdm_s = pd.Series(mdm, index=h.index).ewm(alpha=a, adjust=False).mean() * period
    with np.errstate(divide="ignore", invalid="ignore"):
        pdi = 100.0 * pdm_s / tr_s
        mdi = 100.0 * mdm_s / tr_s
        dx  = 100.0 * (pdi - mdi).abs() / (pdi + mdi)
    dx  = dx.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    adx = dx.ewm(alpha=a, adjust=False).mean()
    return adx.fillna(0.0).values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, adjust=False).mean().values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(close, rsi, adx, momentum_threshold, adx_trend_confirm,
                  adx_exit_fade, direction):
    """
    Long entry:  RSI crosses above 50+threshold AND ADX > adx_trend_confirm.
    Short entry: RSI crosses below 50-threshold AND ADX > adx_trend_confirm.
    Exit: ADX drops below adx_exit_fade.
    """
    n = len(close)

    long_cond  = (rsi > 50.0 + momentum_threshold) & (adx > adx_trend_confirm)
    short_cond = (rsi < 50.0 - momentum_threshold) & (adx > adx_trend_confirm)

    prev_long  = np.roll(long_cond.astype(np.uint8),  1); prev_long[0]  = 0
    prev_short = np.roll(short_cond.astype(np.uint8), 1); prev_short[0] = 0

    fade_exit = adx < adx_exit_fade

    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    if direction in ("long", "both"):
        le[1:] = (long_cond & ~prev_long.astype(bool))[1:]
        lx[1:] = fade_exit[1:]

    if direction in ("short", "both"):
        se[1:] = (short_cond & ~prev_short.astype(bool))[1:]
        sx[1:] = fade_exit[1:]

    return le, lx, se, sx


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


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_type, sl_params_list, atr, freq="1h"):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)
    safe_c    = np.where(close_arr > 0, close_arr, 1.0)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq=freq)

    if sl_type == "embedded":
        sl_2d = np.column_stack([
            np.clip(atr * p["atr_stop_mult"] / safe_c, 1e-6, 1.0)
            for p in sl_params_list
        ])
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_2d,
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
    Stage 4 worker. One process per Stage 3 passing combo.
    Nudges each numeric param ±10% and measures Sharpe impact
    using the Stage 3 winner DOW mask.
    task = {"sym","tf","direction","sl_type","best_params",
            "winner_mask","winner_sharpe","winner_trades","stage2_oos_sharpe"}
    """
    sym               = task["sym"]
    tf                = task["tf"]
    direction         = task["direction"]
    sl_type           = task["sl_type"]
    best_params       = task["best_params"]
    winner_mask       = task["winner_mask"]
    winner_sharpe     = task["winner_sharpe"]
    winner_trades     = task["winner_trades"]
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
    dow_days    = DOW_MASKS[winner_mask]

    def _error(msg):
        return {"strategy": STRATEGY_KEY, "symbol": symbol_usdt, "timeframe": tf,
                "direction": direction, "sl_type": sl_type, "stage": 4,
                "best_params": best_params, "winner_mask": winner_mask,
                "winner_sharpe": winner_sharpe, "winner_trades": winner_trades,
                "stage2_oos_sharpe": stage2_oos_sharpe,
                "sensitivity": {}, "robust": False, "note": msg}

    print(f"{log_prefix} loading data...", flush=True)
    try:
        data = engine.get_data(symbol_usdt, tf_enum,
                               datetime(2022, 1, 1), datetime(2024, 12, 31))
    except Exception as e:
        print(f"{log_prefix} DATA ERROR: {e}", flush=True)
        return _error(f"DATA ERROR: {e}")

    if data.empty or len(data) < 500:
        return _error("insufficient data")

    test_data = data.iloc[int(len(data) * 0.7):]

    h_t, l_t, c_t = test_data.High.values, test_data.Low.values, test_data.Close.values
    close_s_t = pd.Series(c_t, index=test_data.index)
    try:
        adx_t = _compute_adx(h_t, l_t, c_t)
        atr_t = _compute_atr(h_t, l_t, c_t)
        rsi_t = _compute_rsi(c_t, best_params["rsi_period"])
        le_t, lx_t, se_t, sx_t = _make_signals(
            c_t, rsi_t, adx_t,
            best_params["momentum_threshold"],
            best_params["adx_trend_confirm"],
            best_params["adx_exit_fade"],
            direction,
        )
    except Exception as e:
        print(f"{log_prefix} INDICATOR ERROR: {e}", flush=True)
        return _error(f"INDICATOR ERROR: {e}")

    print(f"{log_prefix} running sensitivity ({len(test_data)} OOS bars)...", flush=True)
    sensitivity = {}
    for param_name, param_value in best_params.items():
        if (param_name == "direction"
                or isinstance(param_value, bool)
                or isinstance(param_value, str)
                or not isinstance(param_value, (int, float))):
            continue
        param_results = {}
        for label, factor in [("up", 1.1), ("down", 0.9)]:
            nudged_val = nudge_params({param_name: param_value}, factor)[param_name]
            nudged = {**best_params, param_name: nudged_val}
            sharpe, trades = _eval_single_dow(
                close_s_t, le_t, lx_t, se_t, sx_t, atr_t,
                sl_type, nudged, dow_days=dow_days, freq=TF_FREQ_MAP[tf],
            )
            param_results[label] = {"sharpe": sharpe, "trades": trades}
        sensitive = (
            winner_sharpe > 0 and any(
                v["sharpe"] is not None and v["sharpe"] < winner_sharpe * 0.8
                for v in param_results.values()
            )
        )
        param_results["sensitive"] = sensitive
        sensitivity[param_name] = param_results

    robust = bool(sensitivity) and not any(v["sensitive"] for v in sensitivity.values())
    print(f"{log_prefix} robust={robust} params_tested={len(sensitivity)}", flush=True)

    return {
        "strategy":          STRATEGY_KEY,
        "symbol":            symbol_usdt,
        "timeframe":         tf,
        "direction":         direction,
        "sl_type":           sl_type,
        "stage":             4,
        "best_params":       best_params,
        "winner_mask":       winner_mask,
        "winner_sharpe":     winner_sharpe,
        "winner_trades":     winner_trades,
        "stage2_oos_sharpe": stage2_oos_sharpe,
        "sensitivity":       sensitivity,
        "robust":            robust,
        "note":              note,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="MO1 Stage 4 — parameter sensitivity (15m, 1h, 12h off-TFs)")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
    parser.add_argument("--skip-download", action="store_true")
    args = parser.parse_args()

    run_sensitivity_parallel(
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
