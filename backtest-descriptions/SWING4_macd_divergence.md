# SWING4 — MACD Divergence (Momentum Reversal)

**Timeframe:** 2H  
**Direction:** Long and Short  
**Target R:R:** 1:2  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Counter-trend reversal strategy. Detects divergence between price action and MACD histogram to identify momentum exhaustion points. Enters when price makes a new extreme (high or low) that is NOT confirmed by the MACD histogram — classic divergence signal. RSI adds an additional confirmation layer to avoid entering too early.

### Divergence Detection (lookback = 5 bars)

**Bullish Divergence:**
- Price: current low is **below** the lowest low of the previous 5 bars (new low)
- MACD Histogram: current histogram is **above** the lowest histogram of previous 5 bars (histogram does NOT confirm the new low)
- → Price makes lower low but MACD makes higher low = bullish divergence

**Bearish Divergence:**
- Price: current high is **above** the highest high of the previous 5 bars (new high)
- MACD Histogram: current histogram is **below** the highest histogram of previous 5 bars (histogram does NOT confirm the new high)
- → Price makes higher high but MACD makes lower high = bearish divergence

### Entry — Long
1. Bullish divergence detected (price LL, histogram HL)
2. RSI(14) < 45 (still in weak/oversold territory — confirms not already recovered)

### Entry — Short
1. Bearish divergence detected (price HH, histogram LH)
2. RSI(14) > 55 (still in strong/overbought territory)

### Indicators
- **MACD:** fast=12, slow=26, signal=9 (using histogram only for divergence)
- **RSI:** period=14

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - ATR×2` (long) / `entry + ATR×2` (short)
- **Take Profit:** 1:2 R:R

### Filters
- Day-of-week filter (all days enabled by default)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `macd_fast` | 12 | [10, 12] |
| `macd_slow` | 26 | [24, 26] |
| `macd_signal` | 9 | [7, 9] |
| `rsi_period` | 14 | [10, 14] |
| `divergence_lookback` | 5 | [3, 5, 8, 10] |
| `rsi_long_max` | 45 | [40, 45, 50] |
| `rsi_short_min` | 55 | [50, 55, 60] |
| `atr_stop_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `rr_ratio` | 2.0 | [1.5, 2.0, 2.5] |

---

## Suggested Test Symbols
ETHUSDT, BTCUSDT, LINKUSDT, AAVEUSDT (mid-cap alts with cleaner divergences)

## Notes
- This is a counter-trend strategy — will struggle in strong uninterrupted trends
- 2H timeframe gives reasonable signal frequency
- Divergence detection is a simplified version (bar-level, not swing-to-swing pivot detection)
  → For production, consider upgrading to proper pivot-based divergence detection
- RSI filter is critical to avoid entering when momentum is already reversing against you
