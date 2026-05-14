# SWING1 — EMA Wave + Volume (Trend Following)

**Timeframe:** 1H  
**Direction:** Long and Short  
**Target R:R:** 1:3  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
EMA wave trend-following strategy with volume confirmation. Enters when the fast EMA is above/below the slow EMA (trend direction), RSI crosses the momentum threshold (entry timing), price is on the correct side of the fast EMA, and volume is above its moving average (confirmation of participation).

### Entry — Long
1. Fast EMA(9) > Slow EMA(21) → uptrend structure
2. RSI(14) crosses **above** 40 → momentum turning up
3. Close > Fast EMA(9) → price respecting trend
4. Volume > SMA(volume, 20) → above-average participation

### Entry — Short
1. Fast EMA(9) < Slow EMA(21) → downtrend structure
2. RSI(14) crosses **below** 60 → momentum turning down
3. Close < Fast EMA(9) → price respecting trend
4. Volume > SMA(volume, 20) → above-average participation

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - ATR×2` (long) / `entry + ATR×2` (short)
- **Take Profit:** `entry + ATR×6` (long) / `entry - ATR×6` (short) → 1:3 R:R

### Filters
- Day-of-week filter (all days enabled by default)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `ema_fast` | 9 | [7, 9, 12] |
| `ema_slow` | 21 | [18, 21, 26] |
| `rsi_period` | 14 | [10, 14] |
| `rsi_long_threshold` | 40 | [35, 40, 45] |
| `rsi_short_threshold` | 60 | [55, 60, 65] |
| `volume_ma_period` | 20 | [15, 20, 25] |
| `atr_stop_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `rr_ratio` | 3.0 | [2.0, 3.0, 4.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, LINKUSDT, AAVEUSDT

## Notes
- Designed for trending markets — expect poor results in range-bound periods
- RSI cross condition means entries are on momentum confirmation, not EMA cross itself
- Volume filter significantly reduces trade count but improves quality
