# SWING2 — BB Squeeze Breakout (Volatility Expansion)

**Timeframe:** 4H  
**Direction:** Long and Short  
**Target R:R:** 1:2.5  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Bollinger Band squeeze breakout strategy. Waits for BB width to contract (low volatility squeeze) for a sustained period, then enters when price breaks outside the bands with MACD as momentum direction confirmation. Targets the volatility expansion that typically follows a squeeze.

### Squeeze Detection
- `BB width = (upper_band - lower_band) / basis`
- A squeeze is occurring when: `bb_width < ta.lowest(bb_width, squeeze_bars)[1]`
- Entry is valid when: `ta.barssince(squeeze) <= squeeze_bars` (recently in a squeeze)

### Entry — Long
1. Was in BB squeeze recently (within last `squeeze_bars` bars)
2. Current close breaks **above** upper Bollinger Band
3. MACD line > Signal line (upward momentum)

### Entry — Short
1. Was in BB squeeze recently
2. Current close breaks **below** lower Bollinger Band
3. MACD line < Signal line (downward momentum)

### Indicators
- **Bollinger Bands:** SMA(20), multiplier 2.0
- **MACD:** fast=12, slow=26, signal=9
- **ATR:** period=14 (for stops)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2.5`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - ATR×2.5` (long) / `entry + ATR×2.5` (short)
- **Take Profit:** 1:2.5 R:R

### Filters
- Day-of-week filter (all days enabled by default)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `bb_length` | 20 | [15, 20, 25] |
| `bb_mult` | 2.0 | [1.8, 2.0, 2.2] |
| `squeeze_bars` | 5 | [3, 5, 8] |
| `macd_fast` | 12 | [10, 12] |
| `macd_slow` | 26 | [24, 26] |
| `macd_signal` | 9 | [7, 9] |
| `atr_stop_mult` | 2.5 | [2.0, 2.5, 3.0] |
| `rr_ratio` | 2.5 | [2.0, 2.5, 3.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, ADAUSDT, ATOMUSDT

## Notes
- 4H timeframe means fewer signals — need at least 2-3 years of data for meaningful results
- Squeeze detection is relative (local minimum of width), not absolute — adapts to market volatility
- MACD confirmation avoids entering breakouts that immediately fail (whipsaw)
