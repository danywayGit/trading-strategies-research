# SWING1 — EMA Wave + Volume Optimization Results

**Symbol:** ETHUSDT  
**Timeframe:** 1H  
**Period:** 2021-01-01 to 2024-12-31 (4 years)  
**Objective:** SQN  
**Combinations tested:** 4,374 (exhaustive)  
**Run time:** 56m 31s (GPU)

---

## Best Parameters

```json
{
  "ema_fast": 9,
  "ema_slow": 18,
  "rsi_period": 10,
  "rsi_long_threshold": 45,
  "rsi_short_threshold": 60,
  "vol_ma_period": 15,
  "atr_stop_mult": 2.5,
  "rr_ratio": 4.0
}
```

## Best Result Metrics

| Metric | Value |
|--------|-------|
| Total Return | +26.4% |
| Sharpe Ratio | 1.04 |
| Sortino Ratio | 1.93 |
| Profit Factor | 1.98 |
| Max Drawdown | -6.5% |
| Win Rate | 31.9% |
| SQN | 1.94 |
| # Trades | 72 |

## Top 10 Combinations

| Rank | SQN | ema_fast | ema_slow | rsi_p | long_thr | short_thr | vol | stop | rr |
|------|-----|----------|----------|-------|----------|-----------|-----|------|----|
| 1 | 1.939 | 9 | 18 | 10 | 45 | 60 | 15 | 2.5 | 4.0 |
| 2 | 1.929 | 7 | 21 | 10 | 45 | 60 | 15 | 2.5 | 4.0 |
| 3 | 1.920 | 7 | 21 | 10 | 45 | 60 | 20 | 2.5 | 4.0 |
| 4 | 1.898 | 12 | 18 | 10 | 45 | 60 | 15 | 2.5 | 4.0 |
| 5 | 1.855 | 9 | 18 | 10 | 45 | 60 | 20 | 2.5 | 4.0 |
| 6 | 1.825 | 12 | 18 | 10 | 45 | 60 | 20 | 2.5 | 4.0 |
| 7 | 1.810 | 7 | 21 | 10 | 45 | 60 | 25 | 2.5 | 4.0 |
| 8 | 1.805 | 7 | 21 | 10 | 45 | 60 | 20 | 2.5 | 2.0 |
| 9 | 1.792 | 12 | 18 | 10 | 45 | 55 | 25 | 2.5 | 4.0 |
| 10 | 1.771 | 7 | 21 | 10 | 45 | 60 | 25 | 2.5 | 2.0 |

## Key Observations

- `rsi_period=10` in **all** top-10 — faster RSI catches momentum crosses better at 1H
- `rsi_long_threshold=45` in **all** top-10 — high RSI bar filters out weak momentum entries
- `atr_stop_mult=2.5` in **all** top-10 — wider stop needed for EMA wave entries
- `rr_ratio=4.0` in 7/10 — ⚠️ same concern as SWING5: large RR exploits big moves
- `ema_slow=18` in 5/10 (vs 21 in 5/10) — both fast EMA pairs competitive
- Only 72 trades over 4 years (18/year) — very selective

---

## Walk-Forward Validation ❌ LIKELY OVERFIT

Train: 2021-01-01 → 2023-10-19 (70%) | Test: 2023-10-19 → 2024-12-31 (30%)

| Metric | Train | Test | Change | Status |
|--------|-------|------|--------|--------|
| Total Return | +26.2% | +0.6% | -97.9% | ⚠️ WARN |
| Sharpe Ratio | 1.36 | 0.10 | -92.5% | ⚠️ WARN |
| Sortino Ratio | 2.78 | 0.15 | -94.7% | ⚠️ WARN |
| Profit Factor | 2.43 | 1.09 | -55.2% | ⚠️ WARN |
| Max Drawdown | -3.8% | -6.4% | -70.6% | ✅ OK |
| Win Rate | 32.7% | 31.6% | -3.4% | ✅ OK |
| SQN | 2.09 | 0.18 | -91.3% | ⚠️ WARN |
| Trades | 52 | 19 | — | — |

**Verdict: ❌ LIKELY OVERFIT** — 5 metrics collapse. Only 19 trades in test period — statistically insufficient. `rr_ratio=4.0` exploits 2021-2023 high-volatility bear cycle; fails in 2024 bull trend where moves are directional rather than whipsaw.

## Diagnosis & Recommended Fix

Root cause: same as SWING5 — `rr_ratio=4.0` at 1H timeframe requires +4× ATR moves to hit TP. These occurred frequently in 2021-23 volatility but rarely in 2024 trend.

**Suggested re-optimization:**
- Fix `rr_ratio` to 2.0–2.5 (remove from grid)
- Reduce `atr_stop_mult` grid to [1.5, 2.0] — tight stop + reasonable TP
- Keep `rsi_period=10`, `rsi_long_threshold=45` (consistent signal across top-10)
- Move to 4H timeframe for fewer false signals and more realistic trade counts

**Status: NOT deployable as-is — re-optimize with lower RR**
