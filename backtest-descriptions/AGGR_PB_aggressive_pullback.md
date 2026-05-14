# AGGR_PB — Aggressive Pullback to EMA20 (Engulfing Reversal)

**Timeframe:** 1H or 4H (recommended)  
**Direction:** Long and Short  
**Target R:R:** 1:2  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Trades high-quality engulfing reversal candles that form during a pullback to EMA20, in the direction of the EMA200 major trend. Combines candlestick pattern (engulfing), trend context (EMA200), pullback quality filter, swing structure requirement, and a massive-candle exclusion filter.

### Entry — Long
All conditions must be true:
1. **Trend:** Close > EMA(20) AND Close > EMA(200) → price in uptrend on both scales
2. **Pattern:** Bullish engulfing candle:
   - Current: close > open (green candle)
   - Previous: close < open (red candle)
   - Current close > previous open (full engulf top)
   - Current open ≤ previous close (full engulf bottom)
3. **Pullback quality:** Max 1 bar of last 3 closed BELOW EMA20 → price was near EMA, not far away
4. **Swing structure:** Current candle OR previous candle is the 7-bar lowest low
5. **Not a massive candle:** True range < ATR × 2 (avoids entering on news spikes)

### Entry — Short
All conditions must be true (inverse logic):
1. Close < EMA(20) AND Close < EMA(200)
2. Bearish engulfing candle (red engulfs previous green)
3. Max 1 bar of last 3 closed ABOVE EMA20
4. Current or previous bar is the 7-bar highest high
5. True range < ATR × 2

### Stop Loss Calculation (dynamic, wider than pure ATR)
- **Long:** `stop_distance = (close - lowest_low_7bars) + ATR(14) × 3`
  - Places stop below the swing low + ATR buffer
- **Short:** `stop_distance = (highest_high_7bars - close) + ATR(14) × 3`

> **Note:** Stop can be wide on large engulfing candles. This reduces position size automatically via risk-based sizing.

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - stop_distance` (long) / `entry + stop_distance` (short)
- **Take Profit:** 1:2 R:R

### Filters
- Day-of-week and hour-of-day filters
- Trade direction: Long / Short / Both

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `ema_length` | 20 | [15, 20, 25] |
| `ema200_length` | 200 | [150, 200] |
| `atr_period` | 14 | [10, 14] |
| `stop_mult` | 3.0 | [2.0, 3.0, 4.0] |
| `rr_ratio` | 2.0 | [1.5, 2.0, 2.5, 3.0] |
| `pullback_tolerance` | 1 | [0, 1, 2] |
| `swing_lookback` | 7 | [5, 7, 10] |
| `massive_candle_atr_mult` | 2.0 | [1.5, 2.0, 3.0] |

---

## Suggested Test Symbols
ETHUSDT, BTCUSDT, SOLUSDT, LINKUSDT, BNBUSDT

## Notes
- Most conditions-dense strategy of the set → fewest signals, highest quality
- The pullback tolerance filter (max 1 bar below EMA in last 3) is key — test with 0 and 2 as well
- Swing low/high requirement adds structure confluence — may miss some valid engulfings
- Expect lower trade frequency on 4H vs 1H — 4H will have the cleanest setups
- The wide dynamic stop (swing + ATR buffer) is realistic — small positions, large reward potential
