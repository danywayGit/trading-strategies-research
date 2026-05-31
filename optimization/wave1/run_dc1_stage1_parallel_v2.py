#!/usr/bin/env python3
"""
DC1 Stage 1 optimization — vectorbt v2 (PARALLEL).
TF: 4H  |  Strategy: dc1_donchian_channel

Signal: close breaks Donchian Channel + ADX trend filter + volume filter.
  Long:  close > DC_upper + ADX > adx_threshold + volume > vol_sma × vol_mult
  Short: close < DC_lower + ADX > adx_threshold + volume > vol_sma × vol_mult
Exit (embedded): signal exit when ADX < adx_exit (trend fading).
Note: vectorbt approximates trailing stop with fixed ATR stop.

Indicator cache: DC by donchian_length (4), ADX/ATR by atr_period (3),
  vol_sma by vol_avg_period (3) = 36 unique indicator datasets.
Thresholds swept in outer loop: adx_threshold (3) × adx_exit (3) × vol_mult (3) = 27.
Total outer iterations: 36 × 27 = 972.
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

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\DC1\stage1")
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

# Indicator shape params
INDICATOR_PARAMS = {
    "donchian_length": [15, 20, 25, 55],
    "adx_threshold":   [20, 25, 30],
    "adx_exit":        [15, 20, 25],
    "atr_period":      [10, 14, 21],
    "vol_avg_period":  [14, 20, 30],
    "vol_mult":        [0.8, 1.0, 1.2],
}

# SL params swept as vectorbt columns
SL_PARAM_GRID = {
    # embedded: atr_stop_mult for SL, rr_ratio for TP (trail_atr_mult ignored/fixed)
    "embedded":     {"atr_stop_mult":   [1.5, 2.0, 3.0],
                     "rr_ratio":        [2.0, 2.5, 3.0]},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0]},
    "atr":          {"atr_stop_mult":   [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
                     "rr_ratio":        [2.0, 2.5, 3.0]},
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
        "strategy":         "dc1_donchian_channel",
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

    # ADX exit: ADX drops below adx_exit threshold (trend fading)
    adx_exit_signal = adx < adx_exit

    if direction in ("long", "both"):
        le = valid_dc & (close > dc_upper) & adx_strong & vol_confirm
        lx = adx_exit_signal
    if direction in ("short", "both"):
        se = valid_dc & (close < dc_lower) & adx_strong & vol_confirm
        sx = adx_exit_signal

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


def _run_vbt_portfolio(close_series, le, lx, se, sx, sl_type, sl_params_list, atr):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq="4h")

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

def _optimize_vbt(data, direction, sl_type):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    vol      = data.Volume.values
    close_s  = pd.Series(c, index=data.index)
    sl_list  = _build_sl_params_list(sl_type)

    best_sharpe = -np.inf
    best_result = None

    dc_cache:  dict = {}
    adx_cache: dict = {}
    vol_cache: dict = {}

    ip = INDICATOR_PARAMS
    for donchian_length, adx_threshold, adx_exit, atr_period, vol_avg_period, vol_mult in product(
        ip["donchian_length"], ip["adx_threshold"], ip["adx_exit"],
        ip["atr_period"],      ip["vol_avg_period"], ip["vol_mult"],
    ):
        if donchian_length not in dc_cache:
            dc_cache[donchian_length] = _compute_donchian(h, l, donchian_length)
        dc_upper, dc_lower = dc_cache[donchian_length]

        if atr_period not in adx_cache:
            adx_cache[atr_period] = _compute_adx_and_atr(h, l, c, atr_period)
        adx_arr, atr_arr = adx_cache[atr_period]

        if vol_avg_period not in vol_cache:
            vol_cache[vol_avg_period] = _compute_vol_sma(vol, vol_avg_period)
        vol_sma = vol_cache[vol_avg_period]

        le, lx, se, sx = _make_signals(
            c, dc_upper, dc_lower, adx_arr, vol, vol_sma,
            adx_threshold, adx_exit, vol_mult, direction,
        )
        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr_arr)
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
                    "donchian_length": donchian_length,
                    "adx_threshold":   adx_threshold,
                    "adx_exit":        adx_exit,
                    "atr_period":      atr_period,
                    "vol_avg_period":  vol_avg_period,
                    "vol_mult":        vol_mult,
                    "direction":       direction,
                    **sl_p,
                },
                sharpe, n_trades, wr, dd,
            )

    return best_result


def _eval_single(data, direction, sl_type, best_params):
    h, l, c = data.High.values, data.Low.values, data.Close.values
    vol      = data.Volume.values
    close_s  = pd.Series(c, index=data.index)
    try:
        dc_upper, dc_lower = _compute_donchian(h, l, best_params["donchian_length"])
        adx_arr, atr_arr   = _compute_adx_and_atr(h, l, c, best_params["atr_period"])
        vol_sma            = _compute_vol_sma(vol, best_params["vol_avg_period"])
        le, lx, se, sx = _make_signals(
            c, dc_upper, dc_lower, adx_arr, vol, vol_sma,
            best_params["adx_threshold"], best_params["adx_exit"],
            best_params["vol_mult"], direction,
        )
        if sl_type in ("embedded", "atr"):
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio": best_params["rr_ratio"]}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct": best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        else:
            raise ValueError(f"Unknown sl_type: {sl_type}")
        stats_df = _run_vbt_portfolio(close_s, le, lx, se, sx, sl_type, sl_list, atr_arr)
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
    parser = argparse.ArgumentParser(description="DC1 Stage 1 v2 parallel optimization")
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
    print(f"DC1 Stage 1 v2 — Parallel ({args.workers} workers)")
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
