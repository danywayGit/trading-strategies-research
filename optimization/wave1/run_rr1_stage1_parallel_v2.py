#!/usr/bin/env python3
"""
RR1 Stage 1 optimization — vectorbt v2 (PARALLEL).
TF: 4H  |  Strategy: rr1_range_mean_reversion  |  SL type: embedded ONLY

Signal: Ranging market (ADX < threshold) + price at BB extreme + RSI extreme
        + Stochastic cross from oversold/overbought zone.
  Long:  ADX < adx_threshold + close <= bb_lower + RSI < rsi_oversold
         + stoch_k crosses above stoch_d from below 20
  Short: Mirror.

TP approximation: BB band width (opposite extreme) as fraction of close.
SL: range_low (rolling min of low) or range_high minus ATR × sl_buffer_atr.

Note: Original strategy has partial TP at SMA20 (50% close) and ADX/time exits.
      vectorbt approximation uses full TP at BB opposite extreme + ATR stop.
      Acceptable for Stage 1 screening (PASS/FAIL based on OOS Sharpe > 0).

Grid: Only 'embedded' sl_type (strategy uses self.buy(sl=...) directly).
      sl_buffer_atr [6 values] swept as inner vectorbt columns.
      All other params create 324 indicator × 27 threshold = 8,748 outer iterations.
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

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\RR1\stage1")
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
SL_TYPES   = ["embedded"]   # RR1 only supports embedded

# Indicator shape params (outer loop, 324 unique indicator combos)
INDICATOR_PARAMS = {
    "adx_period":    [10, 14],
    "rsi_period":    [10, 14, 21],
    "bb_length":     [20, 30, 50],
    "bb_mult":       [1.5, 2.0, 2.5],
    "stoch_k":       [14, 18, 21],
    "stoch_d":       [3, 5],
}
# Filter thresholds (swept in outer loop, 27 combos per indicator set)
THRESHOLD_PARAMS = {
    "adx_threshold":  [15, 20, 25],
    "rsi_oversold":   [25, 30, 35],
    "rsi_overbought": [65, 70, 75],
}
# SL param swept as vectorbt columns
SL_PARAM_GRID = {
    "embedded": {"sl_buffer_atr": [0.2, 0.3, 0.5, 0.8, 1.0, 1.5]},
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
        "strategy":         "rr1_range_mean_reversion",
        "symbol":           symbol,
        "timeframe":        "4h",
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

def _compute_adx(high, low, close, period):
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
    adx = dx.ewm(alpha=alpha, adjust=False).mean().fillna(0.0)
    return adx.values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean().fillna(0).values.astype(np.float64)


def _compute_rsi(close, period):
    s = pd.Series(close)
    delta = s.diff()
    gain  = delta.clip(lower=0).ewm(alpha=1.0 / period, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(alpha=1.0 / period, adjust=False).mean()
    rs    = gain / loss.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).fillna(50).values.astype(np.float64)


def _compute_bb(close, bb_length, bb_mult):
    s    = pd.Series(close)
    sma  = s.rolling(bb_length, min_periods=bb_length).mean()
    std  = s.rolling(bb_length, min_periods=bb_length).std(ddof=1)
    upper = (sma + bb_mult * std).ffill().bfill().values
    lower = (sma - bb_mult * std).ffill().bfill().values
    return upper, lower, sma.ffill().bfill().values


def _compute_stoch(high, low, close, k_period, d_period):
    """Stochastic oscillator: %K and %D."""
    h, l, c = pd.Series(high), pd.Series(low), pd.Series(close)
    low_min  = l.rolling(k_period, min_periods=k_period).min()
    high_max = h.rolling(k_period, min_periods=k_period).max()
    k = 100 * (c - low_min) / (high_max - low_min).replace(0, np.nan)
    k = k.fillna(50)
    d = k.rolling(d_period, min_periods=1).mean()
    return k.values.astype(np.float64), d.values.astype(np.float64)


def _compute_range_levels(high, low, bb_length):
    """Range high/low: rolling max/min over bb_length bars (for stop placement)."""
    h = pd.Series(high).rolling(bb_length, min_periods=bb_length).max().ffill().bfill().values
    l = pd.Series(low).rolling(bb_length, min_periods=bb_length).min().ffill().bfill().values
    return h.astype(np.float64), l.astype(np.float64)


# ── Signals ───────────────────────────────────────────────────────────────────

def _make_signals(adx, rsi, bb_upper, bb_lower, stoch_k, stoch_d, close,
                  adx_threshold, rsi_oversold, rsi_overbought, direction):
    """
    RR1 range mean reversion signals.
    Stochastic crossover condition includes oversold/overbought zone filter.
    No signal exits — TP at opposite BB extreme (via tp_stop), SL via sl_buffer_atr.
    """
    n = len(close)
    le = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)

    ranging = adx < adx_threshold

    # Stochastic crosses
    stoch_x_up = np.zeros(n, dtype=bool)
    stoch_x_dn = np.zeros(n, dtype=bool)
    stoch_x_up[1:] = ((stoch_k[:-1] < stoch_d[:-1]) & (stoch_k[1:] >= stoch_d[1:]) &
                       (stoch_k[1:] < 20) & (stoch_d[1:] < 20))
    stoch_x_dn[1:] = ((stoch_k[:-1] > stoch_d[:-1]) & (stoch_k[1:] <= stoch_d[1:]) &
                       (stoch_k[1:] > 80) & (stoch_d[1:] > 80))

    if direction in ("long", "both"):
        le = ranging & (close <= bb_lower) & (rsi < rsi_oversold) & stoch_x_up
    if direction in ("short", "both"):
        se = ranging & (close >= bb_upper) & (rsi > rsi_overbought) & stoch_x_dn

    return le, np.zeros(n, dtype=bool), se, np.zeros(n, dtype=bool)


# ── vectorbt portfolio ────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    return [{"sl_buffer_atr": v} for v in SL_PARAM_GRID[sl_type]["sl_buffer_atr"]]


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
                       sl_params_list, atr, bb_upper, bb_lower,
                       range_high, range_low, close_arr):
    """
    RR1 embedded: SL at range_low/high - atr × sl_buffer_atr (6 columns).
    TP at opposite BB extreme (fraction of close).
    """
    n_combos = len(sl_params_list)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    # TP: distance to opposite BB extreme as fraction of close
    # (vectorbt applies positive tp_stop fraction in the favorable direction for each position)
    tp_long  = np.clip(np.where(close_arr > 0, (bb_upper - close_arr) / close_arr, 0.05), 1e-4, 2.0)
    tp_short = np.clip(np.where(close_arr > 0, (close_arr - bb_lower) / close_arr, 0.05), 1e-4, 2.0)
    tp_frac  = np.maximum(tp_long, tp_short)   # combined approximation
    tp_2d    = np.tile(tp_frac[:, None], (1, n_combos))

    # SL: distance from close to range_low/high ± ATR buffer
    sl_2d = np.column_stack([
        np.clip(
            np.where(close_arr > 0,
                     (close_arr - np.minimum(range_low - atr * p["sl_buffer_atr"], close_arr * 0.995)) / close_arr,
                     0.05),
            1e-4, 1.0,
        )
        for p in sl_params_list
    ])

    pf = vbt.Portfolio.from_signals(
        close=close_series,
        entries=le_2d, exits=lx_2d,
        short_entries=se_2d, short_exits=sx_2d,
        sl_stop=sl_2d, tp_stop=tp_2d,
        init_cash=1_000_000, fees=0.0005, freq="4h",
    )
    return _extract_pf_stats(pf, n_combos)


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    # Indicator caches
    adx_cache:   dict = {}
    rsi_cache:   dict = {}
    bb_cache:    dict = {}
    stoch_cache: dict = {}
    atr_cache:   dict = {}

    ip = INDICATOR_PARAMS
    tp = THRESHOLD_PARAMS
    for adx_period, rsi_period, bb_length, bb_mult, stoch_k_p, stoch_d_p in product(
        ip["adx_period"], ip["rsi_period"], ip["bb_length"],
        ip["bb_mult"],    ip["stoch_k"],    ip["stoch_d"],
    ):
        if adx_period not in adx_cache:
            adx_cache[adx_period] = _compute_adx(h, l, c, adx_period)
        adx_arr = adx_cache[adx_period]

        if rsi_period not in rsi_cache:
            rsi_cache[rsi_period] = _compute_rsi(c, rsi_period)
        rsi_arr = rsi_cache[rsi_period]

        bb_key = (bb_length, bb_mult)
        if bb_key not in bb_cache:
            bb_u, bb_lo, bb_sma = _compute_bb(c, bb_length, bb_mult)
            rh, rl = _compute_range_levels(h, l, bb_length)
            bb_cache[bb_key] = (bb_u, bb_lo, bb_sma, rh, rl)
        bb_upper, bb_lower, _, range_high, range_low = bb_cache[bb_key]

        sk_key = (stoch_k_p, stoch_d_p)
        if sk_key not in stoch_cache:
            stoch_cache[sk_key] = _compute_stoch(h, l, c, stoch_k_p, stoch_d_p)
        stoch_k_arr, stoch_d_arr = stoch_cache[sk_key]

        if "atr14" not in atr_cache:
            atr_cache["atr14"] = _compute_atr(h, l, c, 14)
        atr_arr = atr_cache["atr14"]

        for adx_threshold, rsi_oversold, rsi_overbought in product(
            tp["adx_threshold"], tp["rsi_oversold"], tp["rsi_overbought"]
        ):
            le, lx, se, sx = _make_signals(
                adx_arr, rsi_arr, bb_upper, bb_lower, stoch_k_arr, stoch_d_arr, c,
                adx_threshold, rsi_oversold, rsi_overbought, direction,
            )
            if le.sum() + se.sum() == 0:
                continue

            try:
                stats_df = _run_vbt_portfolio(
                    close_s, le, lx, se, sx,
                    sl_list, atr_arr, bb_upper, bb_lower,
                    range_high, range_low, c,
                )
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
                        "adx_period":     adx_period,
                        "adx_threshold":  adx_threshold,
                        "rsi_period":     rsi_period,
                        "rsi_oversold":   rsi_oversold,
                        "rsi_overbought": rsi_overbought,
                        "bb_length":      bb_length,
                        "bb_mult":        bb_mult,
                        "stoch_k":        stoch_k_p,
                        "stoch_d":        stoch_d_p,
                        "direction":      direction,
                        "sl_mode":        "embedded",
                        **sl_p,
                    },
                    sharpe, n_trades, wr, dd,
                )

    return best_result


def _eval_single(data, direction, sl_type, best_params):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    close_s  = pd.Series(c, index=data.index)
    try:
        adx_arr                      = _compute_adx(h, l, c, best_params["adx_period"])
        rsi_arr                      = _compute_rsi(c, best_params["rsi_period"])
        bb_upper, bb_lower, _, rh, rl = (*_compute_bb(c, best_params["bb_length"], best_params["bb_mult"]),
                                          *_compute_range_levels(h, l, best_params["bb_length"]))
        stoch_k_arr, stoch_d_arr     = _compute_stoch(h, l, c, best_params["stoch_k"], best_params["stoch_d"])
        atr_arr                      = _compute_atr(h, l, c, 14)
        le, lx, se, sx = _make_signals(
            adx_arr, rsi_arr, bb_upper, bb_lower, stoch_k_arr, stoch_d_arr, c,
            best_params["adx_threshold"], best_params["rsi_oversold"],
            best_params["rsi_overbought"], direction,
        )
        sl_list = [{"sl_buffer_atr": best_params["sl_buffer_atr"]}]
        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_list, atr_arr, bb_upper, bb_lower, rh, rl, c)
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
        data = engine.get_data(symbol_usdt, TimeFrame.H4,
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
    print(f"Pre-downloading {len(symbols)} symbols (4H)...")
    for sym in symbols:
        symbol_usdt = sym + "USDT"
        try:
            d = engine.get_data(symbol_usdt, TimeFrame.H4, start, end)
            print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
        except Exception as e:
            print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description="RR1 Stage 1 v2 parallel optimization")
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
                fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
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
    print(f"RR1 Stage 1 v2 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do.")
        return

    done = skipped
    passed = 0
    for sym in SYMBOLS:
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fpath = RESULTS_DIR / f"{sym}USDT_4h_{direction}_{sl_type}.json"
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
                    fname = f"{symbol_usdt}_4h_{direction}_{sl_type}.json"
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
