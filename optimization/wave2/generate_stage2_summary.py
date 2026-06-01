#!/usr/bin/env python3
"""
Generate Stage 2 summary markdown for a completed parallel-v2 strategy run.

Usage:
    python generate_stage2_summary.py <STRATEGY_ID>
    python generate_stage2_summary.py ALL          # generate for every strategy

Examples:
    python generate_stage2_summary.py SWING3
    python generate_stage2_summary.py AGGR_PULLBACK
    python generate_stage2_summary.py ALL
"""
import json
import sys
from pathlib import Path
from datetime import datetime

RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")

# Per-strategy metadata.
# sl_types must match the filenames written by the corresponding v2 script.
# RR1 and SFP1 are not included in Stage 2.
STRATEGY_META = {
    "SWING2":        {"key": "swing2_bb_squeeze",           "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING3":        {"key": "swing3_supertrend_adx",       "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING4":        {"key": "swing4_macd_divergence",      "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING5":        {"key": "swing5_keltner_breakout",     "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "EMA_REJ_V1":    {"key": "ema_rejection_v1",            "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "DC1":           {"key": "dc1_donchian_channel",        "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VR1":           {"key": "vr1_vwap_mean_reversion",     "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "AGGR_PULLBACK": {"key": "aggr_pullback",               "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "MO1":           {"key": "mo1_momentum_rotation",       "home_tf": "4h",
                      "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VP1":           {"key": "vp1_volume_profile_breakout", "home_tf": "1h",
                      "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
}

SYMBOLS_ORDER = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO",
]

DIRECTIONS = ["both", "long", "short"]

# Short labels for table columns
_SL_SHORT = {
    "embedded":    "emb",
    "fixed_pct":   "fpct",
    "fixed_signal":"fsig",
    "atr":         "atr",
}


def load_results(strategy_id, off_tfs, sl_types):
    stage2_dir = RESULTS_BASE / strategy_id / "stage2"
    results = {}
    if not stage2_dir.exists():
        return results
    for sym in SYMBOLS_ORDER:
        symbol_usdt = sym + "USDT"
        for tf in off_tfs:
            for direction in DIRECTIONS:
                for sl_type in sl_types:
                    fname = f"{symbol_usdt}_{tf}_{direction}_{sl_type}.json"
                    fpath = stage2_dir / fname
                    if fpath.exists():
                        try:
                            with open(fpath, encoding="utf-8") as f:
                                results[(symbol_usdt, tf, direction, sl_type)] = json.load(f)
                        except Exception:
                            pass
    return results


def _cell(results, symbol_usdt, tf, direction, sl_type):
    r = results.get((symbol_usdt, tf, direction, sl_type))
    if r is None:
        return "⬜"
    if r.get("verdict") == "PASS":
        return "✅"
    return "❌"


def generate_summary(strategy_id):
    meta     = STRATEGY_META[strategy_id]
    off_tfs  = meta["off_tfs"]
    sl_types = meta["sl_types"]
    results  = load_results(strategy_id, off_tfs, sl_types)

    n_sym  = len(SYMBOLS_ORDER)
    n_dir  = len(DIRECTIONS)
    n_sl   = len(sl_types)
    n_tf   = len(off_tfs)
    total  = n_sym * n_dir * n_sl * n_tf
    done   = len(results)
    pass_list = [r for r in results.values() if r.get("verdict") == "PASS"]
    passed    = len(pass_list)
    pass_list.sort(key=lambda r: (r.get("oos_sharpe") or 0), reverse=True)

    lines = []
    lines.append(f"# {strategy_id} — Stage 2 Summary "
                 f"(home TF: {meta['home_tf'].upper()}, {n_sym} symbols)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Off-TFs tested:** {', '.join(off_tfs)}")
    lines.append(f"**Pass filter:** num_trades ≥ 30 AND OOS Sharpe > 0")
    lines.append(f"**Total combos:** {done} / {total}  "
                 f"({n_sym} symbols × {n_dir} dir × {n_sl} SL × {n_tf} TFs)")
    lines.append(f"**Pass rate:** {passed} / {done}")
    lines.append("")
    lines.append("---")
    lines.append("")

    col_labels = [
        f"{d}/{_SL_SHORT.get(s, s)}"
        for d in DIRECTIONS
        for s in sl_types
    ]
    n_data_cols = len(col_labels)
    header = "| Symbol | " + " | ".join(col_labels) + " |"
    sep    = "|---" * (n_data_cols + 1) + "|"

    for tf in off_tfs:
        lines.append(f"## Pass/Fail Table — {tf.upper()}")
        lines.append("")
        lines.append(header)
        lines.append(sep)
        for sym in SYMBOLS_ORDER:
            symbol_usdt = sym + "USDT"
            row = f"| {symbol_usdt}"
            for direction in DIRECTIONS:
                for sl_type in sl_types:
                    row += f" | {_cell(results, symbol_usdt, tf, direction, sl_type)}"
            row += " |"
            lines.append(row)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Passing Combos (proceed to Stage 3)")
    lines.append("")
    if pass_list:
        lines.append("| Symbol | TF | Direction | SL Type | OOS Sharpe | "
                     "Train Sharpe | Trades | Max DD% | Best Params |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in pass_list:
            params_str = json.dumps(r.get("best_params") or {})
            if len(params_str) > 80:
                params_str = params_str[:77] + "..."
            oos   = r.get("oos_sharpe")
            train = r.get("train_sharpe")
            dd    = r.get("max_drawdown_pct")
            lines.append(
                f"| {r['symbol']} | {r.get('timeframe', '?')} "
                f"| {r['direction']} | {r['sl_type']} "
                f"| {oos if oos is not None else 'N/A'} "
                f"| {train if train is not None else 'N/A'} "
                f"| {r.get('num_trades', 0)} "
                f"| {dd if dd is not None else 'N/A'} "
                f"| `{params_str}` |"
            )
    else:
        lines.append("_No combos passed Stage 2._")

    lines.append("")
    lines.append(f"**Stage 2 pass rate: {passed} / {done}**")
    lines.append("")

    out_dir = RESULTS_BASE / "stage2_summarized"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{strategy_id}_stage2_summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  Pass rate: {passed}/{done}  (total expected: {total})")
    return passed, done


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <STRATEGY_ID | ALL>")
        print(f"Strategies: {list(STRATEGY_META.keys())}")
        sys.exit(1)

    arg = sys.argv[1].upper()

    if arg == "ALL":
        targets = list(STRATEGY_META.keys())
    elif arg in STRATEGY_META:
        targets = [arg]
    else:
        print(f"Unknown strategy '{arg}'. Options: {list(STRATEGY_META.keys())} or ALL")
        sys.exit(1)

    total_passed = total_done = 0
    for sid in targets:
        print(f"\n-- {sid} --")
        p, d = generate_summary(sid)
        total_passed += p
        total_done   += d

    if len(targets) > 1:
        print(f"\n{'='*50}")
        print(f"ALL strategies Stage 2 — total pass rate: {total_passed}/{total_done}")


if __name__ == "__main__":
    main()
