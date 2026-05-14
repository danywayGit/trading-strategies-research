# SWING2 — BB Squeeze Breakout Optimization Results

**Symbol:** ETHUSDT  
**Timeframe:** 4H  
**Period:** 2021-01-01 to 2024-12-31 (4 years, bull+bear+recovery)  
**Objective:** SQN (System Quality Number)  
**Combinations tested:** 972  
**Run time:** 4m 44s (GPU)

---

## Best Parameters

```json
{
  "bb_length": 15,
  "bb_mult": 2.2,
  "squeeze_bars": 3,
  "macd_fast": 10,
  "macd_slow": 24,
  "atr_stop_mult": 2.5,
  "rr_ratio": 2.5
}
```

## Best Result Metrics

| Metric | Value |
|--------|-------|
| Total Return | +67.2% |
| Sharpe Ratio | 0.82 |
| Sortino Ratio | 1.59 |
| Profit Factor | 1.32 |
| Max Drawdown | -16.1% |
| Win Rate | 39.2% |
| SQN | 1.83 |
| # Trades | 148 |

---

## Top 10 Combinations

| Rank | SQN | bb_length | bb_mult | squeeze_bars | macd_fast | macd_slow | atr_stop_mult | rr_ratio |
|------|-----|-----------|---------|--------------|-----------|-----------|---------------|----------|
| 1 | 1.832 | 15 | 2.2 | 8 | 10 | 24 | 2.5 | 2.5 |
| 2 | 1.832 | 15 | 2.2 | 3 | 10 | 24 | 2.5 | 2.5 |
| 3 | 1.832 | 15 | 2.2 | 5 | 10 | 24 | 2.5 | 2.5 |
| 4 | 1.827 | 15 | 2.2 | 8 | 12 | 24 | 2.5 | 2.5 |
| 5 | 1.827 | 15 | 2.2 | 3 | 12 | 24 | 2.5 | 2.5 |
| 6 | 1.827 | 15 | 2.2 | 5 | 12 | 24 | 2.5 | 2.5 |
| 7 | 1.793 | 15 | 2.2 | 8 | 12 | 26 | 2.5 | 2.5 |
| 8 | 1.793 | 15 | 2.2 | 5 | 12 | 26 | 2.5 | 2.5 |
| 9 | 1.793 | 15 | 2.2 | 3 | 12 | 26 | 2.5 | 2.5 |
| 10 | 1.793 | 15 | 2.2 | 8 | 10 | 26 | 2.5 | 2.5 |

---

## Key Observations

- **squeeze_bars is irrelevant** — ranks 1/2/3 are identical except for squeeze_bars (3/5/8), all scoring 1.832. The squeeze detection threshold doesn't change results → MACD direction is doing the real filtering work.
- **bb_length=15 dominates** all top 10 — tighter/faster BB responds better than the standard 20.
- **bb_mult=2.2** wins over 2.0 — slightly wider bands reduce false breakouts.
- **macd_slow=24** beats 26 in top combos — slightly faster MACD improves timing.
- **atr_stop_mult=2.5 and rr_ratio=2.5** locked across all top 10 — these are stable.

## Walk-Forward Validation

Train: 2021-01-01 → 2023-10-19 (70%) | Test: 2023-10-19 → 2024-12-31 (30%)

| Metric | Train | Test | Status |
|--------|-------|------|--------|
| Total Return | +69% | +1.3% | ⚠️ WARN |
| Sharpe Ratio | 1.05 | 0.07 | ⚠️ WARN |
| Profit Factor | 1.56 | 0.95 | OK |
| Max Drawdown | -16.1% | -12.8% | ✅ OK |
| Win Rate | 44% | 33% | OK |
| SQN | 2.24 | -0.09 | ⚠️ WARN |
| Trades | 88 | 60 | — |

**Verdict: LIKELY OVERFIT** — 4 metrics collapse on test data (2023-2024 bull run). Strategy performed well in the 2021-2022 volatile period but does not generalise to the test window. Needs simplification (likely: remove squeeze condition, fewer params).

## Next Steps

- [ ] ~~Walk-forward validation~~ ⚠️ **Overfit — re-evaluate strategy**
- [ ] Run same optimization on BTCUSDT, SOLUSDT, BNBUSDT to test robustness
- [ ] Update TradingView Pine Script `swing_bb_breakout_strategy` with optimized params
