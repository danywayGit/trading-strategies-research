# SWING5 — Keltner Channel Breakout Optimization Results

**Symbol:** ETHUSDT  
**Timeframe:** 1H  
**Period:** 2021-01-01 to 2024-12-31 (4 years)  
**Objective:** SQN  
**Combinations tested:** 729 (exhaustive)  
**Run time:** 12m 18s (GPU)

---

## Best Parameters

```json
{
  "kc_length": 25,
  "kc_mult": 2.0,
  "cci_period": 14,
  "cci_long_min": -100,
  "cci_short_max": 50,
  "rr_ratio": 4.0
}
```

## Best Result Metrics

| Metric | Value |
|--------|-------|
| Total Return | +61.3% |
| Sharpe Ratio | 0.94 |
| Sortino Ratio | 1.77 |
| Profit Factor | 1.32 |
| Max Drawdown | -13.6% |
| Win Rate | 28.6% |
| SQN | 1.85 |
| # Trades | 252 |

## Top 10 Combinations

| Rank | SQN | kc_len | kc_mult | cci_p | cci_long_min | cci_short_max | rr |
|------|-----|--------|---------|-------|--------------|---------------|----|
| 1–10 | **1.8531** | 25 | 2.0 | 14–28 | -100–0 | 0–100 | 4.0 |

## ⚠️ Key Warning: CCI Filter is Inactive

All top-10 combinations share **identical SQN of 1.8531** with `kc_length=25, kc_mult=2.0, rr_ratio=4.0` fixed — only `cci_period`, `cci_long_min`, `cci_short_max` vary. This means:

- The CCI filter produces **zero discrimination** — trades fire regardless of CCI value
- The actual signal is purely `close > upper KC` / `close < lower KC` with EMA stop
- The optimizer found the KC breakout geometry, not a filtered entry

---

## Walk-Forward Validation ❌ LIKELY OVERFIT

Train: 2021-01-01 → 2023-10-19 (70%) | Test: 2023-10-19 → 2024-12-31 (30%)

| Metric | Train | Test | Change | Status |
|--------|-------|------|--------|--------|
| Total Return | +50.4% | +9.0% | -82.1% | ⚠️ WARN |
| Sharpe Ratio | 1.07 | 0.70 | -34.9% | ✅ OK |
| Sortino Ratio | 2.10 | 1.19 | -43.7% | ⚠️ WARN |
| Profit Factor | 1.43 | 1.14 | -20.3% | ✅ OK |
| Max Drawdown | -13.6% | -8.6% | +37.1% | ✅ OK |
| Win Rate | 28.2% | 30.1% | +6.7% | ✅ OK |
| SQN | 1.83 | 0.70 | -61.5% | ⚠️ WARN |
| Trades | 170 | 83 | — | — |

**Verdict: ❌ LIKELY OVERFIT** — 3 metrics collapse. `rr_ratio=4.0` exploits the 2021–2023 volatile bear cycle (big moves) but doesn't generalise to the 2024 bull trend.

## Diagnosis & Recommended Fix

The real strategy here is a **pure Keltner breakout** (no useful CCI filter). Issues:
1. `rr_ratio=4.0` requires huge moves — works in bear/volatility, fails in trend
2. CCI filter does nothing — identical results across all CCI settings
3. EMA stop (back to midline) + `rr=4.0` means TP is very far; most winners reverse before hitting TP

**Suggested redesign:**
- Drop CCI filter entirely (or replace with ADX trend strength filter)
- Lower `rr_ratio` to 2.0–2.5
- Add `kc_mult` range extension to 3.0 for tighter breakout quality
- Re-test on 4H (bigger breakouts, fewer false signals)

**Status: NOT deployable — needs redesign**
