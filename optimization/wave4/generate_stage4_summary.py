#!/usr/bin/env python3
"""
Generate Stage 4 SUMMARY.md per strategy and update BACKTEST-ROADMAP.md.

Usage:
    python generate_stage4_summary.py <STRATEGY_ID>
    python generate_stage4_summary.py ALL
"""
import json
import sys
from pathlib import Path
from datetime import datetime

RESULTS_BASE   = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results")
ROADMAP_PATH   = Path(r"C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\BACKTEST-ROADMAP.md")
ROADMAP_MARKER = "## Wave 1 — Optimization Results"

STRATEGY_META = {
    "SWING2":        {"home_tf": "4h"},
    "SWING3":        {"home_tf": "1h"},
    "SWING4":        {"home_tf": "4h"},
    "SWING5":        {"home_tf": "1h"},
    "EMA_REJ_V1":    {"home_tf": "1h"},
    "DC1":           {"home_tf": "4h"},
    "VR1":           {"home_tf": "1h"},
    "AGGR_PULLBACK": {"home_tf": "4h"},
    "MO1":           {"home_tf": "4h"},
    "VP1":           {"home_tf": "1h"},
}


def _read_pass_line(summary_path: Path, pattern: str) -> str:
    """Extract pass/improved rate string from a stage summary md."""
    if not summary_path.exists():
        return "?"
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        if pattern in line:
            # Find last X/Y pattern
            for tok in reversed(line.split()):
                if "/" in tok:
                    return tok.strip("*():")
    return "?"


def load_sensitivity_results(strategy_id: str) -> list:
    stage4_dir = RESULTS_BASE / strategy_id / "stage4"
    results = []
    if not stage4_dir.exists():
        return results
    for fpath in stage4_dir.glob("*_sensitivity.json"):
        try:
            results.append(json.loads(fpath.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"Warning: could not parse {fpath}: {e}", file=sys.stderr)
    return results


def generate_summary(strategy_id: str) -> tuple:
    """Write results/{STRATEGY}/SUMMARY.md. Returns (n_robust, n_total)."""
    meta    = STRATEGY_META[strategy_id]
    results = load_sensitivity_results(strategy_id)

    n_total  = len(results)
    n_robust = sum(1 for r in results if r.get("robust") is True)
    pct      = f"{100*n_robust/n_total:.1f}%" if n_total > 0 else "0%"

    ranked = sorted(
        [r for r in results if r.get("winner_sharpe") is not None],
        key=lambda r: r.get("winner_sharpe") or 0,
        reverse=True,
    )

    lines = []
    lines.append(f"# {strategy_id} — Summary (home TF: {meta['home_tf'].upper()})")
    lines.append("")
    lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Combos analysed:** {n_total}")
    lines.append(f"**Robust:** {n_robust} / {n_total} ({pct})")
    lines.append(f"  _(Robust = no param nudge ±10% drops OOS Sharpe by >20%)_")
    lines.append(f"  _(Note: sensitivity measures SL/TP params; indicator params use pre-computed signals per spec §9)_")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Top Combos")
    lines.append("")

    if ranked:
        lines.append("| Symbol | Off-TF | Direction | SL | Winner Mask | "
                     "Winner Sharpe | Stage2 Sharpe | Trades | Robust |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in ranked:
            robust_icon = "✅" if r.get("robust") else "❌"
            lines.append(
                f"| {r.get('symbol','?')} "
                f"| {r.get('timeframe','?')} "
                f"| {r.get('direction','?')} "
                f"| {r.get('sl_type','?')} "
                f"| {r.get('winner_mask','?')} "
                f"| {r.get('winner_sharpe','N/A')} "
                f"| {r.get('stage2_oos_sharpe','N/A')} "
                f"| {r.get('winner_trades','?')} "
                f"| {robust_icon} |"
            )
    else:
        lines.append("_No Stage 4 results yet._")

    lines.append("")
    lines.append(f"**Robust rate: {n_robust} / {n_total}**")
    lines.append("")

    out_path = RESULTS_BASE / strategy_id / "SUMMARY.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written: {out_path}")
    print(f"  Robust: {n_robust}/{n_total} ({pct})")
    return n_robust, n_total


def _best_combo_str(strategy_id: str) -> str:
    stage4_dir = RESULTS_BASE / strategy_id / "stage4"
    if not stage4_dir.exists():
        return "—"
    best = None
    for fpath in stage4_dir.glob("*_sensitivity.json"):
        try:
            r = json.loads(fpath.read_text(encoding="utf-8"))
            ws = r.get("winner_sharpe")
            if ws and (best is None or ws > best.get("winner_sharpe", 0)):
                best = r
        except Exception:
            continue
    if not best:
        return "—"
    return (f"{best.get('symbol','?')} {best.get('timeframe','?')} "
            f"{best.get('direction','?')} {best.get('sl_type','?')} "
            f"{best.get('winner_mask','?')} Ŝ={best.get('winner_sharpe',0):.3f}")


def update_roadmap(strategy_stats: dict) -> None:
    """Append Wave 1 results section to BACKTEST-ROADMAP.md (idempotent)."""
    content = ROADMAP_PATH.read_text(encoding="utf-8")
    if ROADMAP_MARKER in content:
        print(f"BACKTEST-ROADMAP.md: '{ROADMAP_MARKER}' already exists — skipping.")
        return

    s1_base = RESULTS_BASE / "stage1_summarized"
    s2_base = RESULTS_BASE / "stage2_summarized"
    s3_base = RESULTS_BASE / "stage3_summarized"

    rows = []
    for sid, (n_robust, n_total) in strategy_stats.items():
        home_tf = STRATEGY_META[sid]["home_tf"]
        s1 = _read_pass_line(s1_base / f"{sid}_stage1_summary.md", "Pass rate:")
        s2 = _read_pass_line(s2_base / f"{sid}_stage2_summary.md", "Stage 2 pass rate:")
        s3 = _read_pass_line(s3_base / f"{sid}_stage3_summary.md", "Stage 3 DOW improvement rate:")
        best = _best_combo_str(sid)
        rows.append(
            f"| {sid} | {home_tf} | {s1} | {s2} | {s3} "
            f"| {n_robust}/{n_total} | {best} |"
        )

    section = [
        "",
        "---",
        "",
        ROADMAP_MARKER + " (Stages 1–4)",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d')}  ",
        "**Strategies:** 10 · **Symbols:** 39 · **Test window:** 2022-01-01 → 2024-12-31",
        "",
        "| Strategy | Home TF | S1 Pass | S2 Pass | S3 DOW Improved | S4 Robust | Best Combo |",
        "|---|---|---|---|---|---|---|",
        *rows,
        "",
    ]

    updated = content.rstrip() + "\n" + "\n".join(section) + "\n"
    ROADMAP_PATH.write_text(updated, encoding="utf-8")
    print(f"Updated: {ROADMAP_PATH}")


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

    strategy_stats = {}
    for sid in targets:
        print(f"\n-- {sid} --")
        n_robust, n_total = generate_summary(sid)
        strategy_stats[sid] = (n_robust, n_total)

    if len(targets) > 1:
        total_r = sum(v[0] for v in strategy_stats.values())
        total_t = sum(v[1] for v in strategy_stats.values())
        pct = f"{100*total_r/total_t:.1f}%" if total_t > 0 else "0%"
        print(f"\n{'='*50}")
        print(f"ALL strategies Stage 4 — robust: {total_r}/{total_t} ({pct})")
        update_roadmap(strategy_stats)


if __name__ == "__main__":
    main()
