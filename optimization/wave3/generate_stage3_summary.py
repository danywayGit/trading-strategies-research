#!/usr/bin/env python3
"""
Generate Stage 3 summary markdown for a completed DOW-filter run.

Usage:
    python generate_stage3_summary.py <STRATEGY_ID>
    python generate_stage3_summary.py ALL
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

RESULTS_BASE = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")

STRATEGY_META = {
    "SWING2":        {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING3":        {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING4":        {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "SWING5":        {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "EMA_REJ_V1":    {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "DC1":           {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VR1":           {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "AGGR_PULLBACK": {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "MO1":           {"home_tf": "4h", "off_tfs": ["15m", "1h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
    "VP1":           {"home_tf": "1h", "off_tfs": ["15m", "4h", "12h"],
                      "sl_types": ["embedded", "fixed_pct", "fixed_signal", "atr"]},
}

DOW_MASK_ORDER = ["ALL", "MON-FRI", "SAT-SUN", "MON", "TUE", "WED", "THU", "FRI"]


def load_results(strategy_id):
    stage3_dir = RESULTS_BASE / strategy_id / "stage3"
    results = []
    if not stage3_dir.exists():
        return results
    for fpath in stage3_dir.glob("*_dow.json"):
        try:
            results.append(json.loads(fpath.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
    return results


def generate_summary(strategy_id):
    meta    = STRATEGY_META[strategy_id]
    results = load_results(strategy_id)

    done       = len(results)
    improved   = [r for r in results if r.get("dow_improved") is True]
    n_improved = len(improved)
    pct_improved = f"{100*n_improved/done:.1f}%" if done > 0 else "0%"

    winner_counts = Counter(r.get("winner_mask", "ALL") for r in results)

    ranked = sorted(
        [r for r in results if r.get("winner_sharpe") is not None],
        key=lambda r: r.get("winner_sharpe") or 0,
        reverse=True,
    )

    lines = []
    lines.append(f"# {strategy_id} — Stage 3 Summary "
                 f"(home TF: {meta['home_tf'].upper()})")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Combos processed:** {done}")
    lines.append(f"**DOW improvement rate:** {n_improved} / {done} ({pct_improved}) "
                 f"— combos where a DOW mask beat ALL by ≥ 0.10 Sharpe with ≥ 20 trades")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Winner Mask Distribution")
    lines.append("")
    lines.append("| Mask | Times Won | % of Combos |")
    lines.append("|---|---|---|")
    for mask in DOW_MASK_ORDER:
        count = winner_counts.get(mask, 0)
        pct   = f"{100*count/done:.1f}%" if done > 0 else "0%"
        lines.append(f"| {mask} | {count} | {pct} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Top Combos (ranked by Winner Sharpe)")
    lines.append("")
    if ranked:
        lines.append("| Symbol | Off-TF | Direction | SL | Winner Mask | "
                     "Winner Sharpe | Stage2 Sharpe | OOS Trades | DOW Improved |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in ranked:
            lines.append(
                f"| {r.get('symbol','?')} "
                f"| {r.get('timeframe','?')} "
                f"| {r.get('direction','?')} "
                f"| {r.get('sl_type','?')} "
                f"| {r.get('winner_mask','?')} "
                f"| {r.get('winner_sharpe','N/A')} "
                f"| {r.get('stage2_oos_sharpe','N/A')} "
                f"| {r.get('winner_trades','?')} "
                f"| {'✅' if r.get('dow_improved') else '➖'} |"
            )
    else:
        lines.append("_No Stage 3 results yet._")

    lines.append("")
    lines.append(f"**Stage 3 DOW improvement rate: {n_improved} / {done}**")
    lines.append("")

    out_dir = RESULTS_BASE / "stage3_summarized"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{strategy_id}_stage3_summary.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  DOW improved: {n_improved}/{done}  improved rate: {pct_improved}")
    return n_improved, done


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

    total_improved = total_done = 0
    for sid in targets:
        print(f"\n-- {sid} --")
        i, d = generate_summary(sid)
        total_improved += i
        total_done     += d

    if len(targets) > 1:
        print(f"\n{'='*50}")
        pct = f"{100*total_improved/total_done:.1f}%" if total_done > 0 else "0%"
        print(f"ALL strategies Stage 3 — DOW improved: {total_improved}/{total_done} ({pct})")


if __name__ == "__main__":
    main()
