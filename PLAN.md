# Trading Strategies Research — Continuation Plan

Created: 2024-12-30 (Q4 2024 / planning for Q1 2025)
Last updated: 2024-12-30
Status: Active — Phase 1 underway

---

## Current State Summary

| Artifact | Status | Count |
|--|---|---|
| Original SWING1–6 specs + fixes | ✅ Complete | 6 |
| EMA_REJ_V1/V2 specs | ✅ Complete | 2 |
| AGGR_PB spec | ✅ Complete | 1 |
| Phase 1 ideas (RR1, VP1, VR1, A01) | ✅ Complete | 4 |
| Phase 2 ideas (MO1, DC1, PT1, AR1, EC1) | ✅ Complete | 5 |
| SFP1 swing failure pattern | ✅ Complete | 1 |
| **Total Strategies Defined** |  | **19** |

**Backtests Already Run:**
- SWING1, SWING2, SWING3, SWING4, SWING5 on ETHUSDT
- SWING3 multi-symbol robustness test (ETH, BTC, SOL, BNB, LINK)
- AGGR_PB, EMA_REJ_V1 preliminary passes

**Key Insight from Existing Results:**
All ETHUSDT optimizations flagged as **LIKELY OVERFIT** in walk-forward validation. Common root causes:
- `rr_ratio=4.0` exploits 2021–2023 volatility cycle, fails in 2024 bull trend
- Very low trade counts (<80 trades/4 years) → statistically insufficient
- Some filters (CCI in SWING5) proved inactive

---

## Plan Overview

### Phase 1: Fix & Re-optimize Existing Strategies (Priority: 🔴 High)
**Goal:** Make SWING1–5 deployable by addressing identified overfit issues

| Strategy | Issue | Action | Est. Time |
|--|--|--|--|
| SWING1 | Overfit RR4.0, low trade count | Re-optimize with `rr_ratio∈[2.0, 2.5]`, tighten `atr_stop_mult∈[1.5, 2.0]`, move to 4H | 1h |
| SWING2 | Need walk-forward pass/fail | Re-run with constrained grid, add walk-forward split | 1h |
| SWING3 | 0 trades on BTC at 1H, whipsaws on alts | Re-optimize on 4H for BTC, per-symbol param search for SOL/LINK | 2h |
| SWING4 | Overfit in train/test split | Tighten RR grid, reduce params, add regime filter | 1h |
| SWING5 | CCI filter inactive, overfit RR | Drop CCI entirely or swap for ADX, lower RR to 2.0–2.5 | 1h |
| SWING6 | Not yet backtested | Implement dual-TF backtest (30m entry / 4H bias) | 2h |

**Acceptance Criteria for Phase 1:**
- [ ] All 6 SWING strategies have walk-forward validation with ✅ verdict
- [ ] Trade count ≥50 per 2-year test window (statistical significance)
- [ ] At least 2 strategies pass robustness check on BTC + ETH
- [ ] Pine Script files updated with corrected parameters

---

### Phase 2: Backtest Phase 1 Ideas (RR1, VP1, VR1, A01) (Priority: 🟡 Medium-High)
**Goal:** Initial optimization runs on ETHUSDT + BTCUSDT for the first 4 new ideas

| Strategy | Type | Complexity | Est. Time |
|--|--|--|--|
| **RR1** | Range Mean Reversion (RSI+BB+Stoch) | Low — single TF, well-known indicators | 2h |
| **VP1** | Volume Profile Breakout (POC/VAH/VAL) | Medium — need VAH/VAL calculation | 2h |
| **VR1** | VWAP Mean Reversion (Z-score) | Low — single TF, standard stats | 2h |
| **A01** | Screener Composite (altFINS signals) | **High** — needs external data pipeline | 4h |

**Execution Order:**
1. RR1 → VR1 → VP1 (self-contained, fast to run)
2. A01 last (depends on altFINS data availability in BacktestingMCP)

**Deliverables:**
- [ ] 4 new optimization result files in `results/`
- [ ] Walk-forward validation on each
- [ ] Multi-symbol check (ETH + BTC minimum)
- [ ] Pine Script implementations in `TradingView/`

---

### Phase 3: Backtest Phase 2 Ideas (MO1, DC1, PT1, AR1, EC1) (Priority: 🟢 Medium)
**Goal:** Advanced strategies with multi-asset or regime-aware logic

| Strategy | Type | Complexity | Est. Time | Notes |
|--|--|--|--|--|
| **DC1** | Donchian + ATR (Mini Turtle) | Low — classic breakout | 2h | Similar to SWING5 but cleaner |
| **MO1** | Momentum Rotation | High — cross-asset relative strength | 3h | Requires asset universe management |
| **PT1** | BTC/ETH Pair Trading | Medium — cointegration + z-score | 3h | Needs spread calculation |
| **AR1** | Adaptive Regime Switcher | **Very High** — meta-strategy | 5h | Must detect regime THEN switch |
| **EC1** | Event Catalyst Alpha | **Very High** — external catalyst data | 5h | Depends on altFINS event feed |

**Execution Order:**
1. DC1 first (simplest, fast feedback)
2. PT1 → MO1 (both multi-asset but self-contained)
3. AR1 last (depends on having good sub-strategies to switch between)
4. EC1 last (depends on external catalyst data)

**Dependencies:**
- AR1 needs at least 2–3 successful base strategies from Phases 1–2 to manage
- EC1 needs altFINS event classification pipeline

---

### Phase 4: SFP1 Swing Failure Pattern (Priority: 🔵 Medium-Low, High Interest)
**Goal:** Most labor-intensive implementation but highest perceived edge

| Component | Complexity | Est. Time |
|--|--|--|--|
| Dual-TF backtest engine (1H HTF + 5m LTF) | **Very High** — multi-resolution resampling | 4h |
| Session mode testing (NY, London, Asian, Any) | Medium — 4 separate runs | 2h |
| FVG zone detection & entry logic | High — precise candle-level logic | 3h |
| Multi-asset validation (BTC, ETH, BNB) | Medium | 2h |

**Why last:**
- Most complex implementation (dual timeframe alignment)
- Highest risk of edge cases (session boundaries, timezone conversion)
- But also highest conviction from user interest

**Success Criteria:**
- [ ] SFP detection on 1H: swing high/low marking + raid confirmation
- [ ] FVG zone formed within 2–5 candles of SFP
- [ ] Entry fills on 5m retrace into FVG zone
- [ ] ≥30 trades over 2-year test window
- [ ] Walk-forward Sharpe ≥0.8, Max DD ≤8%

---

### Phase 5: Cross-Validation & Robustness (Priority: 🟡 Medium-High)
**Goal:** Prove strategies work across symbols and market regimes

For each strategy that passes individual backtests with ✅ walk-forward:

| Test | Description |
|--|--|
| **Multi-Asset** | Re-run on BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT |
| **Regime Stability** | Split 2021–2024 into 4 years, verify no single-year dependency |
| **Parameter Insensitivity** | Nudge each parameter by ±10%, verify metrics don't collapse |
| **Monte Carlo Shuffle** | Shuffle trade order 1000×, verify equity curve stability |

**Deliverable:** `results/ROBUSTNESS_SUMMARY.md` with pass/fail matrix

---

### Phase 6: Pine Script & Live Deployment (Priority: 🟢 Medium)
**Goal:** Turn top 3–5 strategies into live TradingView alerts

| Strategy | Priority | Reason |
|--|--|--|
| SWING3 (if fixed) | 1 | Already has multi-symbol data, just needs fixes |
| DC1 | 2 | Clean breakout, easy to read alert |
| RR1 | 3 | Counter-trend diversification |
| SFP1 | 4 | High conviction but complex (last to deploy) |
| PT1 | 5 | Market-neutral, good hedge |

**Per Strategy:**
1. Write Pine Script v6 strategy file with `strategy.exit()` (absolute prices)
2. Verify chart matches BacktestingMCP results (trade count, P&L within 5%)
3. Set up 3 TradingView alerts per strategy (LONG, SHORT, INFO)
4. Configure webhook to `Trading-WebHook-Bot` Flask endpoint
5. Paper-trade for 2 weeks, compare to backtest expectations

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|--|--|--|--|
| Walk-forward overfit repeats | High | Strategy appears profitable but fails live | Always use ≥2-year test window, check trade count |
| Dual-TF alignment bugs (SFP1) | Medium | False signals, wrong entries | Unit test swing detector + FVG finder separately |
| altFINS data gaps (A01/EC1) | Medium | Missing signals, incomplete backtest | Implement fallback: skip bar if data missing, log gap |
| Over-optimization on ETH only | High | ETH-specific edge doesn't transfer | Require ≥2-symbol validation before calling it done |
| Pine Script drift from Python | Low | Chart shows different trades than backtest | Add comparison test: export trades from both, diff P&L |

---

## Implementation Template

Each new strategy implementation follows this pipeline:

```
backtest-descriptions/{ID}_*.md
    ↓ (read spec)
src/strategies/strategies/{id_lowercase}_strategy.py
    ↓ (register in templates.py STRATEGY_REGISTRY)
BacktestingMCP/ run: backtest --strategy {ID} --data ETHUSDT_1h --years 2022-2024
    ↓ (output: results/)
results/{ID}_ETHUSDT_1h_optimization.md
    ↓ (if ✅ pass)
results/{ID}_multi_symbol_robustness.md
    ↓ (if ✅ pass)
TradingView/{id}_strategy.pinescript
    ↓ (deploy to TradingView)
Trading-WebHook-Bot/ alerts.json + Flask routes
```

---

## Time Estimates

| Phase | Est. Hours | Notes |
|--|--|--|
| Phase 1 (Re-optimize SWING1–6) | 8h | Most critical — existing work needs fixing |
| Phase 2 (RR1/VP1/VR1/A01) | 11h | Fast feedback, good diversification ideas |
| Phase 3 (MO1/DC1/PT1/AR1/EC1) | 18h | Advanced strategies, multi-asset complexity |
| Phase 4 (SFP1) | 11h | Highest complexity, highest interest |
| Phase 5 (Cross-Validation) | 10h+ | Per winning strategy |
| Phase 6 (Pine + Live) | 15h+ | Per deployed strategy |
| **Total Estimated Effort** | **~73h** | ~4 weeks full-time |

---

## Next Immediate Actions

1. [ ] **Today:** Pick top 2 strategies from Phase 1 to re-optimize with constrained RR ratios
2. [ ] **This Week:** Complete Phase 2 (RR1 → VR1 → VP1) — 3 fast backtests
3. [ ] **Next Week:** Start SFP1 dual-TF engine (Phase 4) — hardest piece first
4. [ ] **Ongoing:** Document every optimization result with walk-forward verdict
