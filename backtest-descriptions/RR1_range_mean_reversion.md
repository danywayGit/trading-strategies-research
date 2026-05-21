# RR1 — Range Mean Reversion (RSI + Bollinger Bands + Stochastic)

**Timeframe:** 4H
**Direction:** Long and Short
**Target R:R:** 1:1.5 (TP1 50%) / 1:2.5 (TP2 50%)
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Identifies range-bound (sideways) market phases via ADX < threshold, then trades reversals at extremes using triple-indicator confirmation: Bollinger Band touch, RSI overshoot, and Stochastic cross. Designed to work when trend-following strategies are flat — complementing SWING3 and EMA_REJ_V1.

### Entry — Long
All conditions must be true:
1. **Range filter:** ADX(14) < 20 → market is not trending
2. **Lower BB touch:** Price closes at or below the lower Bollinger Band (SMA20 − 2 × ATR)
3. **Oversold:** RSI(14) < 30
4. **Stochastic cross:** Stochastic(14,3,3) %K crosses above %D while both are below 20

### Entry — Short
All conditions must be true (inverse logic):
1. ADX(14) < 20
2. Price closes at or above the upper Bollinger Band (SMA20 + 2 × ATR)
3. RSI(14) > 70
4. Stochastic %K crosses below %D while both are above 80

### Stop Loss
- **Long:** `stop = range_high + ATR(14) × 0.5` (opposite extreme + buffer)
  - `range_high` = highest high over the last 20 bars
- **Short:** `stop = range_low − ATR(14) × 0.5`
  - `range_low` = lowest low over the last 20 bars

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = abs(entry - stop)`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **TP1:** 50% of position at SMA20 (mean) → partial close
- **TP2:** remaining 50% at opposite extreme of range (high/low of last 20 bars)
- **Stop Loss:** Full exit at SL price
- **Max holding:** 200 bars (~33 days on 4H) to avoid stale positions

### Filters
- Max 1 active trade at a time (either long or short, never both)
- No new entry if ADX(14) crosses above 25 during holding (regime change to trending)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `adx_threshold` | 20 | [15, 20, 25] |
| `adx_period` | 14 | [10, 14] |
| `rsi_period` | 14 | [10, 14, 21] |
| `rsi_oversold` | 30 | [25, 30, 35] |
| `rsi_overbought` | 70 | [65, 70, 75] |
| `bb_length` | 20 | [20, 30, 50] |
| `bb_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `stoch_k` | 14 | [14, 18, 21] |
| `stoch_d` | 3 | [3, 5] |
| `stoch_slow` | 3 | [3, 5] |
| `tp1_pct` | 50 | [40, 50, 60] |
| `sl_buffer_atr` | 0.5 | [0.3, 0.5, 1.0] |

---

## Suggested Test Symbols
ETHUSDT, BTCUSDT, LINKUSDT, DOGEUSDT (altcoins with clear range phases)

## Notes
- Pure mean reversal — no trend-following strategy currently fills this niche in the portfolio
- Triple confirmation (BB + RSI + Stoch) reduces whipsaw but may miss early entries
- ADX regime filter is critical — entering mean reversion logic in a trending market is the #1 drawdown driver
- The partial TP approach (50% at SMA20, 50% at range extreme) keeps the position alive for the full range capture while locking in mean-reversion profits early
- Test ADX crossover exit as a safety: if ADX spikes above 25 while holding, close immediately
- Expected lower win rate in trending months (Q1, post-halving) — regime filter is the key defense
