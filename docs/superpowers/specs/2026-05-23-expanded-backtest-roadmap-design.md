# Expanded Backtest Optimization — Design Spec

**Date:** 2026-05-23  
**Status:** Approved — pending implementation plan  
**Scope:** Wave 1 of 2 · 7 strategies · 44 symbols · 4 TFs · 3 SL types · DOW filter

---

## 1. Objective

Run a structured, GPU-accelerated multi-symbol optimization campaign across all 19 implemented BacktestingMCP strategies, in two waves. Results feed BACKTEST-ROADMAP.md as a living progress tracker. Winners eventually deploy to TradingView → Trading-WebHook-Bot.

---

## 2. Wave Structure

| Wave | Strategies | Trigger to start Wave 2 |
|---|---|---|
| Wave 1 | 7 (shortlisted by existing results) | All 7 have a SUMMARY.md in results/ |
| Wave 2 | 12 (remaining strategies) | After Wave 1 Stage 4 complete |

---

## 3. Wave 1 Strategy Shortlist

Selected based on actual backtest results (trade count, walk-forward verdict, robustness):

| # | Strategy | Reason for inclusion |
|---|---|---|
| 1 | SWING2 — BB Squeeze Breakout | 148 trades, generalizable breakout logic |
| 2 | SWING3 — Supertrend + ADX | Best WF pass, 50.9% win rate, clean SQN |
| 3 | SWING4 — MACD Divergence | 294 trades, marginal WF pass, robust top-10 cluster |
| 4 | SWING5 — Keltner Breakout | 252 trades, OOS metrics hold |
| 5 | EMA_REJ_V1 — EMA200 Rejection | 89 trades, best of rejection strategies |
| 6 | DC1 — Donchian Channel | Price-only, classic turtle, designed to generalize |
| 7 | RR1 — Range Mean Reversion | Counter-trend, complements trend strategies |

---

## 4. Symbol Universe (44 coins)

All Binance USDT-M perpetuals. Ranked by 24h futures volume as of 2026-05-23. Stablecoins, wrapped tokens, commodities, and stock synthetics excluded.

### TOP 27
| # | Symbol | | # | Symbol | | # | Symbol |
|---|---|---|---|---|---|---|---|
| 1 | BTCUSDT | | 10 | BNBUSDT | | 19 | ENAUSDT |
| 2 | ETHUSDT | | 11 | SUIUSDT | | 20 | UNIUSDT |
| 3 | SOLUSDT | | 12 | ADAUSDT | | 21 | AAVEUSDT |
| 4 | HYPEUSDT | | 13 | TAOUSDT | | 22 | DOTUSDT |
| 5 | SHIBUSDT | | 14 | LINKUSDT | | 23 | ATOMUSDT |
| 6 | NEARUSDT | | 15 | TONUSDT | | 24 | LTCUSDT |
| 7 | DOGEUSDT | | 16 | BCHUSDT | | 25 | POLUSDT |
| 8 | ONDOUSDT | | 17 | FILUSDT | | 26 | DASHUSDT |
| 9 | (reserved) | | 18 | INJUSDT | | 27 | TRXUSDT |

### MID 8
FET, ICP, RENDER, CHZ, ARB, APT, ETC, OP

### SMALL 9
ALGO, SAND, MANA, FLOW, AXS, GMX, DYDX, RUNE, SEI

---

## 5. Optimization Dimensions

| Dimension | Values |
|---|---|
| Timeframes | 15m, 1H, 4H, 12H |
| Directions | Long only, Short only, Both |
| Stop-loss types | Fixed % · ATR + multiplier · Embedded dynamic SL |
| DOW filter | Applied in Stage 3 only (see below) |

**SL type rule:** If a strategy has a built-in dynamic SL (e.g. SWING3 Supertrend trail, DC1 ATR trail), that counts as the "embedded" variant. The other two (fixed % and ATR multiplier) are tested as alternative configurations.

---

## 6. Funnel Architecture (4 Stages)

### Stage 1 — Home TF Run

Each strategy runs on its spec-recommended timeframe across all 44 symbols.

| Strategy | Home TF |
|---|---|
| SWING2 | 4H |
| SWING3 | 1H |
| SWING4 | 4H |
| SWING5 | 1H |
| EMA_REJ_V1 | 1H |
| DC1 | 4H |
| RR1 | 4H |

**Per strategy:** 44 symbols × 3 directions × 3 SL types = 396 optimization runs  
**Test window:** 2022-01-01 → 2024-12-31 (3 years: covers bull + bear + sideways)  
**Walk-forward split:** 70% train / 30% OOS  
**Pass filter:** ≥30 trades over full window AND Sharpe > 0 in OOS period  
**Output:** `results/{STRATEGY}/stage1/{SYMBOL}_{TF}_{DIR}_{SL}.json`

### Stage 2 — Off-TF Expansion

Take Stage 1 passing combos. Run them on the 3 remaining timeframes.  
Same pass filter applies.  
**Output:** `results/{STRATEGY}/stage2/{SYMBOL}_{TF}_{DIR}_{SL}.json`

### Stage 3 — DOW Filter

Take Stage 2 passing combos. Apply 8 DOW masks on top of best params:

| Mask | Description |
|---|---|
| ALL | No filter (baseline) |
| MON-FRI | Weekdays only |
| SAT-SUN | Weekend only |
| MON | Monday only |
| TUE | Tuesday only |
| WED | Wednesday only |
| THU | Thursday only |
| FRI | Friday only |

**Selection rule:** Pick mask with highest OOS Sharpe, provided it has ≥20 trades. If no mask beats `ALL` by >5% Sharpe → record `ALL` as winner (no filter needed).  
**Output:** `results/{STRATEGY}/stage3/{SYMBOL}_{TF}_dow_analysis.md`

### Stage 4 — Summary & Robustness

For each strategy:
1. Collect all passing symbol+TF+dir+SL+DOW combos
2. Write `results/{STRATEGY}/SUMMARY.md` — ranked table: Sharpe, Max DD, trades, best params, DOW mask
3. Run parameter sensitivity: nudge each best param ±10%, flag if OOS Sharpe drops >20%
4. Update BACKTEST-ROADMAP.md Stage Tracker with ✅ counts and best combo per strategy

**Wave 1 complete** when all 7 strategies have a `SUMMARY.md`.

---

## 7. BACKTEST-ROADMAP.md Updates

A new **"Wave 1 — Expanded Optimization"** section is appended to the existing file containing:
- Progress legend (⬜ / 🔄 / ✅ / ❌)
- Stage tracker table (7 rows × stage columns)
- Symbol universe list
- Per-strategy Stage 1 detail sub-tables (populated as runs complete)
- Wave 2 placeholder section (12 remaining strategies)

The roadmap is updated after each stage completes per strategy — not in bulk at the end.

---

## 8. Wave 2 Placeholder

After Wave 1 Stage 4, Wave 2 covers the remaining 12 strategies:

SWING1, SWING6, EMA_REJ_V2, AGGR_PB, RR1*, VP1, VR1, A01, MO1, PT1, AR1, EC1, SFP1

> *RR1 is in Wave 1. Wave 2 will add the remaining strategies using the same 4-stage funnel.

Wave 2 symbol universe and strategy shortlisting will be revisited based on Wave 1 findings.

---

## 9. Out of Scope

- Pine Script updates (Phase 6 in PLAN.md — after backtesting proves a winner)
- Live deployment (Trading-WebHook-Bot)
- EMA_REJ_V2, AGGR_PB, SWING1, SWING6 (Wave 2 — overfit or insufficient trade count issues)
- SFP1 (Wave 2 — dual-TF 1H+5m, most complex, deferred)
