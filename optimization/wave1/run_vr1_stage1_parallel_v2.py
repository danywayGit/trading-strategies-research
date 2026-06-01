#!/usr/bin/env python3
"""
VR1 Stage 1 optimization — vectorbt v2 (PARALLEL).
1H VWAP mean reversion with volume exhaustion + RSI filter.
243 outer combos (band_mult × vol_exhaust × rsi_floor × rsi_ceil × min_bw).
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

RESULTS_DIR = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\VR1\stage1")
V2_NOTE     = "v2/vectorbt"

SYMBOLS = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]
LIMITED_DATA = {"ENA", "TAO"}
DIRECTIONS   = ["both", "long", "short"]
SL_TYPES     = ["embedded", "fixed_pct", "fixed_signal", "atr"]

INDICATOR_PARAMS = {
    "band_mult":                   [1.5, 2.0, 2.5],
    "volume_exhaustion_threshold": [0.2, 0.3, 0.5],
    "rsi_oversold_floor":          [25, 30, 35],
    "rsi_overbought_ceil":         [65, 70, 75],
    "min_band_width_pct":          [0.3, 0.5, 0.8],
}

SL_PARAM_GRID = {
    "embedded":     {},
    "fixed_pct":    {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "fixed_signal": {"stop_loss_pct":   [1.5, 2.0, 2.5, 3.0],
                     "take_profit_pct": [3.0, 4.0, 6.0, 8.0]},
    "atr":          {"atr_stop_mult":   [1.0, 1.5, 2.0, 2.5, 3.0, 4.0],
                     "rr_ratio":        [1.5, 2.0, 2.5, 3.0]},
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
        "strategy":         "vr1_vwap_mean_reversion",
        "symbol":           symbol,
        "timeframe":        "1h",
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

def _compute_vwap_daily(high, low, close, volume, index):
    """Cumulative VWAP with daily reset at midnight UTC."""
    tp  = (high + low + close) / 3.0
    tp_s  = pd.Series(tp,     index=index)
    vol_s = pd.Series(volume, index=index)
    dates    = tp_s.index.normalize()
    cum_tpv  = (tp_s * vol_s).groupby(dates).cumsum()
    cum_vol  = vol_s.groupby(dates).cumsum()
    safe_vol = cum_vol.replace(0, np.nan)
    return (cum_tpv / safe_vol).fillna(method="ffill").values.astype(np.float64)


def _compute_vwap_std(close, vwap, period=50):
    diff = pd.Series(close - vwap)
    return diff.rolling(period, min_periods=1).std().fillna(0.001).values.astype(np.float64)


def _compute_rsi(close, period=14):
    delta = pd.Series(close).diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)
    avg_g = gain.ewm(alpha=1.0 / period, adjust=False).mean()
    avg_l = loss.ewm(alpha=1.0 / period, adjust=False).mean()
    rs    = avg_g / avg_l.replace(0, np.nan)
    return (100.0 - 100.0 / (1.0 + rs)).fillna(50.0).values.astype(np.float64)


def _compute_atr(high, low, close, period=14):
    h = pd.Series(high); l = pd.Series(low); c = pd.Series(close)
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1.0 / period, adjust=False).mean().values.astype(np.float64)


def _compute_vol_sma(volume, period=20):
    return pd.Series(volume).rolling(period, min_periods=1).mean().values.astype(np.float64)


# ── Signal generation ─────────────────────────────────────────────────────────

def _make_signals(close, vwap, std_dev, rsi, vol, vol_sma,
                  band_mult, vol_exhaust_thresh, rsi_oversold, rsi_overbought,
                  min_band_width_pct, direction):
    n = len(close)
    lower_band = vwap - band_mult * std_dev
    upper_band = vwap + band_mult * std_dev
    band_width = band_mult * std_dev

    prev_close = np.roll(close, 1);    prev_close[0]   = close[0]
    prev_lower = np.roll(lower_band, 1); prev_lower[0] = lower_band[0]
    prev_upper = np.roll(upper_band, 1); prev_upper[0] = upper_band[0]
    prev_vol   = np.roll(vol, 1);      prev_vol[0]     = vol[0]
    prev_vsma  = np.roll(vol_sma, 1);  prev_vsma[0]    = vol_sma[0]
    prev_rsi   = np.roll(rsi, 1);      prev_rsi[0]     = rsi[0]
    prev_bw    = np.roll(band_width, 1); prev_bw[0]    = band_width[0]
    prev_vwap  = np.roll(vwap, 1);     prev_vwap[0]    = vwap[0]

    # Band width filter: previous band must be wide enough
    safe_prev = np.where(prev_close > 0, prev_close, 1.0)
    wide_enough  = (prev_bw / safe_prev) > (min_band_width_pct / 100.0)

    # Volume exhaustion: volume at prev bar was below threshold × avg
    vol_exhaust = (prev_vsma > 0) & (prev_vol < prev_vsma * vol_exhaust_thresh)

    # Reversal: previous bar closed outside band, current closes back inside
    long_rev  = (prev_close < prev_lower) & (close > lower_band)
    short_rev = (prev_close > prev_upper) & (close < upper_band)

    rsi_long_ok  = prev_rsi > rsi_oversold
    rsi_short_ok = prev_rsi < rsi_overbought

    le = np.zeros(n, dtype=bool)
    lx = np.zeros(n, dtype=bool)
    se = np.zeros(n, dtype=bool)
    sx = np.zeros(n, dtype=bool)

    if direction in ("long", "both"):
        le[1:] = (long_rev  & vol_exhaust & rsi_long_ok  & wide_enough)[1:]
        lx[1:] = (close > prev_vwap)[1:]   # exit near VWAP

    if direction in ("short", "both"):
        se[1:] = (short_rev & vol_exhaust & rsi_short_ok & wide_enough)[1:]
        sx[1:] = (close < prev_vwap)[1:]

    return le, lx, se, sx


# ── vectorbt helpers ─────────────────────────────────────────────────────────

def _build_sl_params_list(sl_type):
    g = SL_PARAM_GRID[sl_type]
    if sl_type == "embedded":
        return [{}]
    if sl_type in ("fixed_pct", "fixed_signal"):
        return [{"stop_loss_pct": sl, "take_profit_pct": tp}
                for sl, tp in product(g["stop_loss_pct"], g["take_profit_pct"])]
    if sl_type == "atr":
        return [{"atr_stop_mult": m, "rr_ratio": r}
                for m, r in product(g["atr_stop_mult"], g["rr_ratio"])]
    raise ValueError(sl_type)


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
                       vwap=None, std_dev=None, band_mult=None):
    n_combos  = len(sl_params_list)
    close_arr = close_series.values.astype(np.float64)
    safe_c    = np.where(close_arr > 0, close_arr, 1.0)

    le_2d = np.tile(le[:, None], (1, n_combos))
    lx_2d = np.tile(lx[:, None], (1, n_combos))
    se_2d = np.tile(se[:, None], (1, n_combos))
    sx_2d = np.tile(sx[:, None], (1, n_combos))

    common = dict(close=close_series, init_cash=1_000_000, fees=0.0005, freq="1h")

    if sl_type == "embedded":
        bw     = band_mult * std_dev
        sl_col = np.clip(1.5 * bw / safe_c, 1e-6, 1.0)
        tp_col = np.clip(np.abs(close_arr - vwap) / safe_c, 1e-6, 1.0)
        tp_col = np.maximum(tp_col, sl_col * 1.1)
        pf = vbt.Portfolio.from_signals(
            **common,
            entries=le_2d, exits=lx_2d,
            short_entries=se_2d, short_exits=sx_2d,
            sl_stop=sl_col[:, None], tp_stop=tp_col[:, None],
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


# ── Optimization loop ─────────────────────────────────────────────────────────

def _optimize_vbt(data, direction, sl_type):
    h   = data.High.values
    l   = data.Low.values
    c   = data.Close.values
    v   = data.Volume.values
    idx = data.index
    close_s = pd.Series(c, index=idx)
    sl_list = _build_sl_params_list(sl_type)

    vwap    = _compute_vwap_daily(h, l, c, v, idx)
    std_dev = _compute_vwap_std(c, vwap)
    rsi     = _compute_rsi(c)
    vol_sma = _compute_vol_sma(v)
    atr     = _compute_atr(h, l, c)

    best_sharpe = -np.inf
    best_result = None
    ip = INDICATOR_PARAMS

    for (band_mult, vol_exhaust, rsi_oversold, rsi_overbought, min_bw_pct) in product(
        ip["band_mult"], ip["volume_exhaustion_threshold"],
        ip["rsi_oversold_floor"], ip["rsi_overbought_ceil"], ip["min_band_width_pct"]
    ):
        le, lx, se, sx = _make_signals(
            c, vwap, std_dev, rsi, v, vol_sma,
            band_mult, vol_exhaust, rsi_oversold, rsi_overbought, min_bw_pct, direction
        )
        if le.sum() + se.sum() == 0:
            continue

        try:
            stats_df = _run_vbt_portfolio(
                close_s, le, lx, se, sx, sl_type, sl_list, atr,
                vwap=vwap, std_dev=std_dev, band_mult=band_mult,
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
                        "band_mult":                   band_mult,
                        "volume_exhaustion_threshold": vol_exhaust,
                        "rsi_oversold_floor":          rsi_oversold,
                        "rsi_overbought_ceil":         rsi_overbought,
                        "min_band_width_pct":          min_bw_pct,
                        "direction":                   direction,
                        **sl_p,
                    },
                    sharpe, n_trades, wr, dd,
                )

    return best_result


def _eval_single(data, direction, sl_type, best_params):
    h = data.High.values; l = data.Low.values; c = data.Close.values
    v = data.Volume.values; idx = data.index
    close_s = pd.Series(c, index=idx)
    try:
        vwap    = _compute_vwap_daily(h, l, c, v, idx)
        std_dev = _compute_vwap_std(c, vwap)
        rsi     = _compute_rsi(c)
        vol_sma = _compute_vol_sma(v)
        atr     = _compute_atr(h, l, c)

        band_mult = best_params["band_mult"]
        le, lx, se, sx = _make_signals(
            c, vwap, std_dev, rsi, v, vol_sma,
            band_mult,
            best_params["volume_exhaustion_threshold"],
            best_params["rsi_oversold_floor"],
            best_params["rsi_overbought_ceil"],
            best_params["min_band_width_pct"],
            direction,
        )

        if sl_type == "embedded":
            sl_list = [{}]
        elif sl_type in ("fixed_pct", "fixed_signal"):
            sl_list = [{"stop_loss_pct":   best_params["stop_loss_pct"],
                        "take_profit_pct": best_params["take_profit_pct"]}]
        elif sl_type == "atr":
            sl_list = [{"atr_stop_mult": best_params["atr_stop_mult"],
                        "rr_ratio":      best_params["rr_ratio"]}]
        else:
            raise ValueError(sl_type)

        stats_df = _run_vbt_portfolio(
            close_s, le, lx, se, sx, sl_type, sl_list, atr,
            vwap=vwap, std_dev=std_dev, band_mult=band_mult,
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
        data = engine.get_data(symbol_usdt, TimeFrame.H1,
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
    print(f"Pre-downloading {len(symbols)} symbols (1H)...")
    for sym in symbols:
        symbol_usdt = sym + "USDT"
        try:
            d = engine.get_data(symbol_usdt, TimeFrame.H1, start, end)
            print(f"  {symbol_usdt}: {len(d)} bars", flush=True)
        except Exception as e:
            print(f"  {symbol_usdt}: ERROR — {e}", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description="VR1 Stage 1 v2 parallel optimization")
    parser.add_argument("--workers", type=int,
                        default=max(1, (os.cpu_count() or 4) - 2))
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
                fname = f"{symbol_usdt}_1h_{direction}_{sl_type}.json"
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
    print(f"VR1 Stage 1 v2 — Parallel ({args.workers} workers)")
    print(f"Tasks: {len(all_tasks)} to run, {skipped} already done, {total} total\n")

    if not all_tasks:
        print("Nothing to do — all results already on disk.")
        return

    done = skipped
    passed = 0
    for sym in SYMBOLS:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fpath = RESULTS_DIR / f"{symbol_usdt}_1h_{direction}_{sl_type}.json"
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
                    fname = f"{symbol_usdt}_1h_{direction}_{sl_type}.json"
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
