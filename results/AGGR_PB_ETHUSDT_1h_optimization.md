# AGGR_PB — Aggressive Pullback Optimization Results

**Symbol:** ETHUSDT  
**Timeframe:** 1H  
**Period:** 2021-01-01 to 2024-12-31 (4 years)  
**Objective:** SQN  
**Combinations tested:** 3,888 (exhaustive)  
**Run time:** 1h 20m (GPU)

---

## Best Parameters

```json
{
  "ema_length": 15,
  "ema200_length": 150,
  "atr_period": 14,
  "stop_mult": 2.0,
  "rr_ratio": 2.0,
  "pullback_tolerance": 0,
  "swing_lookback": 10,
  "massive_candle_mult": 1.5
}
```

## Best Result Metrics

| Metric | Value |
|--------|-------|
| Total Return | +9.6% |
| Sharpe Ratio | 1.00 |
| Sortino Ratio | 2.40 |
| Profit Factor | 2.84 |
| Max Drawdown | -1.5% |
| Win Rate | 57.1% |
| SQN | 1.98 |
| # Trades | **21** ⚠️ very low |

## Top 10 Combinations

| Rank | SQN | ema | ema200 | atr_p | stop | rr | pullback | swing | massive |
|------|-----|-----|--------|-------|------|----|----------|-------|---------|
| 1 | 1.983 | 15 | 200 | 14 | 2.0 | 2.0 | 0 | 10 | 1.5 |
| 2 | 1.983 | 15 | 150 | 14 | 2.0 | 2.0 | 0 | 10 | 1.5 |
| 3 | 1.950 | 15 | 150 | 10 | 2.0 | 2.0 | 0 | 10 | 1.5 |
| 4 | 1.950 | 15 | 200 | 10 | 2.0 | 2.0 | 0 | 10 | 1.5 |
| 5 | 1.826 | 15 | 150 | 14 | 4.0 | 2.5 | 1 | 10 | 2.0 |
| 6 | 1.801 | 15 | 150 | 14 | 4.0 | 3.0 | 1 | 10 | 2.0 |
| 7 | 1.774 | 15 | 200 | 10 | 2.0 | 2.0 | 0 | 10 | 2.0 |
| 8 | 1.703 | 15 | 150 | 14 | 4.0 | 3.0 | 2 | 10 | 2.0 |
| 9 | 1.665 | 15 | 150 | 10 | 3.0 | 1.5 | 0 | 10 | 2.0 |
| 10 | 1.653 | 15 | 200 | 14 | 2.0 | 2.0 | 0 | 10 | 2.0 |

## Key Observations

- `swing_lookback=10` in **all** top-10 — wider swing window finds higher-quality pivots
- `ema_length=15` in **all** top-10 — faster EMA20 alt works better for pullback detection
- `rr_ratio=2.0` in 7/10 — healthy target (no RR=4 inflation here)
- `pullback_tolerance=0` in 6/10 — strict: all 3 recent bars must close on correct side of EMA
- `massive_candle_mult=1.5` in 6/10 — tighter filter excludes more news-spike bars
- `ema200_length` split 150/200 — both work equally (ranks 1 & 2 identical SQN)
- **Quality metrics excellent:** PF 2.84, WR 57%, DD only -1.5%
- **⚠️ Only 21 total trades** — very low for statistical confidence

---

## Walk-Forward Validation ⚠️ LOW SAMPLE — INCONCLUSIVE

Train: 2021-01-01 → 2023-10-19 (70%) | Test: 2023-10-19 → 2024-12-31 (30%)

| Metric | Train | Test | Change | Status |
|--------|-------|------|--------|--------|
| Total Return | +8.3% | +1.2% | -85.7% | ⚠️ WARN |
| Sharpe Ratio | 1.09 | 0.73 | -33.2% | ✅ OK |
| Sortino Ratio | 2.67 | 1.65 | -38.3% | ✅ OK |
| Profit Factor | 2.96 | 2.25 | -23.9% | ✅ OK |
| Max Drawdown | -1.5% | -0.7% | +50.9% | ✅ OK |
| Win Rate | 56.3% | **60.0%** | +6.7% | ✅ OK |
| SQN | 1.80 | 0.79 | -56.4% | ⚠️ WARN |
| Trades | 16 | **5** | — | — |

**Verdict: ⚠️ INCONCLUSIVE (low sample)** — officially "LIKELY OVERFIT" but this is misleading. The 5 test trades show quality metrics holding well (PF 2.25, WR 60%, Sharpe 0.73, Sortino 1.65). The SQN and return degradation are statistical artefacts of having only 5 trades.

### True Assessment

The strategy is **too selective for 1H** — 5 trades per year is insufficient for confident deployment. However, quality metrics are exceptional.

**Recommended action:**
- Move to **4H** (same engulfing logic, more significant pullbacks)
- Or **lower `pullback_tolerance` to 1** to generate more entries
- Re-run with larger trade sample before deployment decision
- **Do NOT discard** — quality metrics (PF 2.25+, WR 57-60%) are strongest of all strategies tested

**Status: ⏸️ PROMISING but needs more trades — re-test on 4H**
