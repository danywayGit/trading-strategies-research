# EMA_REJ_V1 — EMA200 Rejection Optimization Results

**Symbol:** ETHUSDT  
**Timeframe:** 1H  
**Period:** 2021-01-01 to 2024-12-31 (4 years)  
**Objective:** SQN  
**Combinations tested:** 300 (random sample of 5,832 total)  
**Run time:** 3m 56s (GPU)

---

## Best Parameters

```json
{
  "ema200_length": 150,
  "rejection_lookback": 5,
  "rsi_period": 14,
  "rsi_ema_period": 14,
  "rsi_confirm_window": 2,
  "htf_bars": 9,
  "stop_mult": 4.0,
  "rr_ratio": 2.0
}
```

## Best Result Metrics

| Metric | Value |
|--------|-------|
| Total Return | +34.9% |
| Sharpe Ratio | 0.90 |
| Sortino Ratio | 1.56 |
| Profit Factor | 1.54 |
| Max Drawdown | -9.7% |
| Win Rate | 42.7% |
| SQN | 1.88 |
| # Trades | 89 |

## Top 10 Combinations

| Rank | SQN | ema200 | lookback | rsi_p | rsi_ema | confirm | htf | stop | rr |
|------|-----|--------|----------|-------|---------|---------|-----|------|----|
| 1 | 1.883 | 150 | 5 | 14 | 14 | 2 | 9 | 4.0 | 2.0 |
| 2 | 1.415 | 150 | 10 | 14 | 9 | 5 | 9 | 4.0 | 2.0 |
| 3 | 1.270 | 150 | 15 | 10 | 7 | 5 | 9 | 4.0 | 2.0 |
| 4 | 1.252 | 150 | 15 | 14 | 14 | 2 | 9 | 4.0 | 2.0 |
| 5 | 1.221 | 150 | 10 | 10 | 9 | 5 | 9 | 4.0 | 2.0 |
| 6 | 1.184 | 200 | 15 | 10 | 14 | 2 | 6 | 3.0 | 1.5 |
| 7 | 0.945 | 150 | 15 | 14 | 7 | 3 | 9 | 4.0 | 2.0 |
| 8 | 0.916 | 200 | 10 | 14 | 7 | 2 | 6 | 3.0 | 2.0 |
| 9 | 0.888 | 150 | 5 | 14 | 7 | 2 | 9 | 3.0 | 3.0 |
| 10 | 0.882 | 150 | 5 | 10 | 14 | 5 | 9 | 3.0 | 2.5 |

## Key Observations

- `htf_bars=9` appears in 9/10 top combos — **9H HTF context is the strongest structural signal**
- `ema200_length=150` in 8/10 — faster EMA catches trends earlier
- `stop_mult=4.0` in 8/10 — rejection entries need room for re-tests, wide stop required
- `rr_ratio=2.0` stable across all top combos
- Large gap between rank 1 (1.88) vs rank 2 (1.41) with random sampling — potential lucky hit (see walk-forward)

---

## Walk-Forward Validation ⚠️

Train: 2021-01-01 → 2023-10-19 (70%) | Test: 2023-10-19 → 2024-12-31 (30%)

| Metric | Train | Test | Status |
|--------|-------|------|--------|
| Total Return | +32.8% | +1.8% | ⚠️ WARN |
| Sharpe Ratio | 1.12 | 0.17 | ⚠️ WARN |
| Sortino Ratio | 2.02 | 0.27 | ⚠️ WARN |
| Profit Factor | 1.77 | 1.03 | ⚠️ WARN |
| Max Drawdown | -9.7% | -10.0% | ✅ OK |
| Win Rate | 47% | 34% | ✅ OK |
| SQN | 2.04 | 0.21 | ⚠️ WARN |
| Trades | 60 | 29 | — |

**Verdict: LIKELY OVERFIT** — 5 metrics collapse on test data. The 300-sample random search likely found a params combination that harvested the 2021-2023 bear+recovery period but doesn't generalise.

## Walk-Forward: Default Params ✅ MARGINAL PASS

Train: 2021-01-01 → 2023-10-19 | Test: 2023-10-19 → 2024-12-31

| Metric | Train | Test | Status |
|--------|-------|------|--------|
| Total Return | +1.1% | **+4.6%** | ✅ OK |
| Sharpe Ratio | 0.04 | **0.46** | ✅ OK |
| Sortino Ratio | 0.06 | **0.79** | ✅ OK |
| Profit Factor | 0.92 | **1.14** | ✅ OK |
| Max Drawdown | -15.9% | -7.5% | ⚠️ WARN (train DD higher) |
| Win Rate | 37.8% | 36.8% | ✅ OK |
| SQN | 0.08 | 0.54 | ✅ OK |
| Trades | 90 | 38 | — |

**Verdict: MARGINAL** — only 1 flag (train DD -15.9% vs -7.5% test, actually better on test). All return/quality metrics improve on test data, same as SWING3. **The default params are MORE robust than the optimized ones.**

### Default vs Optimized Walk-Forward Comparison

| | Default params | Optimized params |
|---|---|---|
| Test Return | +4.6% | +1.8% |
| Test Sharpe | 0.46 | 0.17 |
| Test Profit Factor | 1.14 | 1.03 |
| Walk-forward verdict | ✅ MARGINAL PASS | ⚠️ OVERFIT |

**Conclusion: Use default params for live trading. The 300-sample optimization overfitted to 2021-2023 choppiness.**
