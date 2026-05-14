# Pine Script Bug Report

Review date: 2026-05-14  
Reviewer: Claude (automated review)

---

## Critical Bugs

### BUG-001 — `loss=` / `profit=` vs `stop=` / `limit=`
**Affects:** SWING1, SWING2, SWING4, SWING5, SWING6  
**Severity:** 🔴 Critical — stops and take-profits are essentially never triggered

**Explanation:**  
`strategy.exit(loss=X)` expects a **distance in points** from entry (e.g. `500`).  
`strategy.exit(stop=X)` expects an **absolute price** (e.g. `44500`).

All 5 strategies pass absolute prices to `loss=` / `profit=`, meaning:
- `loss=close - stop_dist` → e.g. `44000` points of loss before stopping → never stops
- `profit=close + (stop_dist * 3)` → requires ~130,000 point gain → never profits

**Fix:** Replace `loss=` with `stop=` and `profit=` with `limit=` throughout.

```pine
// WRONG
strategy.exit("Exit", "Long", loss=close - stop_dist, profit=close + (stop_dist * 3))

// CORRECT
strategy.exit("Exit", "Long", stop=close - stop_dist, limit=close + (stop_dist * 3))
```

---

### BUG-002 — Chat artifacts in source code
**Affects:** SWING1, SWING2, SWING4, SWING6  
**Severity:** 🔴 Critical — Pine Script will not compile

**Explanation:**  
Telegram/Discord chat messages were accidentally included in the code when copying:
```
[08.04.2026 04:30] TVRemix: tial_capital=100000, currency="USD")
```
These break syntax. The code must start directly with `//@version=5`, not with the word `pinescript`.

**Files affected:**
- `swing_ema_wave_volumes_strategy.pinescript` — line 1 `pinescript`, lines 19-20 split mid-code
- `swing_bb_breakout_strategy.pinescript` — line 1 `pinescript`, line 72 split
- `swing_macd_divergence_strategy.pinescript` — line 1 `pinescript`, line 68 split
- `swing_kelner_breakout_strategy.pinescript` — line 1 `pinescript`
- `swing_super_trend_adx_strategy.pinescript` — line 1 `pinescript`

---

### BUG-003 — EMA Rejection v2: `shortStayedBelow` / `longStayedAbove` always false
**Affects:** `ema_rejection_strategy_v2.pinescript`  
**Severity:** 🔴 Critical — Zero short trades will fire

**Explanation:**  
`shortEmaRejection` triggers on `priceCrossBelowEma` (the bar where close crosses BELOW EMA200).  
At that exact bar, `close[1]` was definitionally ABOVE EMA200 (that's what a crossunder means).  
So `shortStayedBelow` iterates bars [1..N] and finds `close[1] > ema200[1]` immediately → `barsBelow = 0` → `shortStayedBelow = false` → condition never fires.

Same logic applies to `longStayedAbove`.

**Fix options:**
1. Remove the `shortStayedBelow` / `longStayedAbove` conditions (v1 logic, cleaner)
2. Use a persistent counter that accumulates AFTER the rejection bar fires

**Recommended fix:** Remove those conditions — v1 (`ema_rejection_strategy.pinescript`) is logically correct and produces the intended behavior.

---

## Minor Issues

### BUG-004 — SWING3: Trade lines show static TP that doesn't match strategy
**Affects:** `swing_super_trend_adx_strategy.pinescript`  
**Severity:** 🟡 Visual only — no impact on backtest results

The strategy uses a Supertrend trailing exit (no fixed TP), but the trade lines plot `_entry + stop_dist * 2` as a green TP line. This is misleading in TradingView — the green line does not represent an actual exit target.

**Fix:** Either remove the TP line or add a note label clarifying it's indicative only.

---

## Fixed Files

See corrected versions in this folder:
- `SWING1_fixed.pinescript`
- `SWING2_fixed.pinescript`
- `SWING4_fixed.pinescript`
- `SWING5_fixed.pinescript`
- `SWING6_fixed.pinescript`
- `EMA_Rejection_v2_fixed.pinescript`
