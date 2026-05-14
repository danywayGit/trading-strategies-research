# SWING6 — Multi-Timeframe EMA Stack (HTF Bias + LTF Entry)

**Timeframe:** 30m entry / 4H bias  
**Direction:** Long and Short  
**Target R:R:** 1:2.5  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Multi-timeframe trend-following strategy. Uses a higher timeframe (4H) EMA as a directional bias filter, then enters on a fast/slow EMA crossover on the lower timeframe (30m) only when aligned with the HTF bias. Reduces false signals from LTF noise by requiring HTF confluence.

### Higher Timeframe Bias (4H)
- **Bull bias:** 4H close > 4H EMA(20)
- **Bear bias:** 4H close < 4H EMA(20)

### Lower Timeframe Entry (30m or current TF)
- **Long cross:** EMA(9) crosses **above** EMA(21)
- **Short cross:** EMA(9) crosses **below** EMA(21)

### Entry — Long
1. HTF bull bias active (4H close > 4H EMA20)
2. LTF EMA(9) crosses above EMA(21)

### Entry — Short
1. HTF bear bias active (4H close < 4H EMA20)
2. LTF EMA(9) crosses below EMA(21)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - ATR×2` (long) / `entry + ATR×2` (short)
- **Take Profit:** 1:2.5 R:R

### Filters
- Day-of-week filter (all days enabled by default)
- Background color visualization: green when bull bias, red when bear bias

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `htf_ema` | 20 | [20, 50, 100] |
| `ltf_fast` | 9 | [7, 9, 12] |
| `ltf_slow` | 21 | [18, 21, 26] |
| `htf_timeframe` | "240" (4H) | ["240", "360", "D"] |
| `atr_stop_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `rr_ratio` | 2.5 | [2.0, 2.5, 3.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT

## Notes
- Entry TF (30m) must be passed to BacktestingMCP as the data resolution
- HTF EMA is recalculated via request.security — in Python backtesting, compute 4H EMA on resampled OHLCV data
- This is the most implementation-complex strategy due to multi-timeframe resampling
- Consider starting the backtest on the 1H timeframe with "D" HTF bias to simplify first pass
