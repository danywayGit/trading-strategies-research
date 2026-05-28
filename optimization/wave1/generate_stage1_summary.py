#!/usr/bin/env python3
"""
Generate Stage 1 summary markdown for a completed strategy run.
Usage: python generate_stage1_summary.py <STRATEGY_ID>
Example: python generate_stage1_summary.py SWING2
"""
import json
import sys
from pathlib import Path
from datetime import datetime

RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")

STRATEGY_META = {
    "SWING2":    {"key": "swing2_bb_squeeze",        "tf": "4h"},
    "SWING3":    {"key": "swing3_supertrend_adx",    "tf": "1h"},
    "SWING4":    {"key": "swing4_macd_divergence",   "tf": "4h"},
    "SWING5":    {"key": "swing5_keltner_breakout",  "tf": "1h"},
    "EMA_REJ_V1":{"key": "ema_rejection_v1",         "tf": "1h"},
    "DC1":       {"key": "dc1_donchian_channel",     "tf": "4h"},
    "RR1":       {"key": "rr1_range_mean_reversion", "tf": "4h"},
}

SYMBOLS_ORDER = [
    "BTC", "ETH", "SOL", "BNB", "ADA", "DOGE", "DOT", "LINK", "LTC", "BCH",
    "UNI", "AAVE", "ATOM", "FIL", "INJ", "AVAX", "NEAR", "TRX",
    "ALGO", "SAND", "MANA", "RUNE", "AXS", "DASH", "ETC", "CHZ", "SHIB",
    "ICP", "FLOW", "FET", "DYDX", "OP", "GMX", "APT", "ARB", "SUI", "SEI",
    "ENA", "TAO"
]

DIRECTIONS = ["both", "long", "short"]
SL_TYPES = ["embedded", "fixed", "atr_wide"]


def load_results(strategy_id, tf):
    stage1_dir = RESULTS_BASE / strategy_id / "stage1"
    results = {}
    for sym in SYMBOLS_ORDER:
        symbol_usdt = sym + "USDT"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                fname = f"{symbol_usdt}_{tf}_{direction}_{sl_type}.json"
                fpath = stage1_dir / fname
                if fpath.exists():
                    with open(fpath) as f:
                        results[(symbol_usdt, direction, sl_type)] = json.load(f)
    return results


def cell(results, symbol_usdt, direction, sl_type):
    r = results.get((symbol_usdt, direction, sl_type))
    if r is None:
        return "⬜"
    if r.get("verdict") == "PASS":
        return "✅"
    return "❌"


def generate_summary(strategy_id):
    meta = STRATEGY_META[strategy_id]
    tf = meta["tf"]
    results = load_results(strategy_id, tf)

    total = len(SYMBOLS_ORDER) * 3 * 3
    done = len(results)
    pass_list = [r for r in results.values() if r.get("verdict") == "PASS"]
    passed = len(pass_list)

    # Sort pass list by OOS sharpe descending
    pass_list.sort(key=lambda r: (r.get("oos_sharpe") or 0), reverse=True)

    lines = []
    lines.append(f"# {strategy_id} — Stage 1 Summary ({tf.upper()}, all 39 symbols)")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Pass filter:** num_trades ≥ 30 AND OOS Sharpe > 0")
    lines.append(f"**Total combos run:** {done} / {total} (39 symbols × 3 dir × 3 SL)")
    lines.append(f"**Pass rate:** {passed} / {done}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Pass/Fail Table")
    lines.append("")
    header = "| Symbol | both/emb | both/fixed | both/atr | long/emb | long/fixed | long/atr | short/emb | short/fixed | short/atr |"
    sep    = "|---|---|---|---|---|---|---|---|---|---|"
    lines.append(header)
    lines.append(sep)

    for sym in SYMBOLS_ORDER:
        symbol_usdt = sym + "USDT"
        row = f"| {symbol_usdt}"
        for direction in DIRECTIONS:
            for sl_type in SL_TYPES:
                row += f" | {cell(results, symbol_usdt, direction, sl_type)}"
        row += " |"
        lines.append(row)

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Passing Combos (proceed to Stage 2)")
    lines.append("")
    if pass_list:
        lines.append("| Symbol | Direction | SL Type | OOS Sharpe | Train Sharpe | Trades | Max DD% | Best Params |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in pass_list:
            params_str = json.dumps(r.get("best_params") or {})
            if len(params_str) > 80:
                params_str = params_str[:77] + "..."
            lines.append(
                f"| {r['symbol']} | {r['direction']} | {r['sl_type']} "
                f"| {r.get('oos_sharpe') or 'N/A'} | {r.get('train_sharpe') or 'N/A'} "
                f"| {r.get('num_trades', 0)} | {r.get('max_drawdown_pct') or 'N/A'} "
                f"| `{params_str}` |"
            )
    else:
        lines.append("_No combos passed Stage 1._")

    lines.append("")
    lines.append(f"**Stage 1 pass rate: {passed} / {done}**")
    lines.append("")

    out_path = RESULTS_BASE / strategy_id / "stage1" / f"{strategy_id}_stage1_summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"Pass rate: {passed}/{done}")
    return passed, done


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <STRATEGY_ID>")
        print(f"Options: {list(STRATEGY_META.keys())}")
        sys.exit(1)
    strategy_id = sys.argv[1].upper()
    if strategy_id not in STRATEGY_META:
        print(f"Unknown strategy: {strategy_id}. Options: {list(STRATEGY_META.keys())}")
        sys.exit(1)
    generate_summary(strategy_id)
