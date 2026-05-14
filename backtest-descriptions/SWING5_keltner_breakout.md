# SWING5 — Keltner Channel Breakout (Trend Continuation)

**Timeframe:** 1H  
**Direction:** Long and Short  
**Target R:R:** 1:3  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Keltner Channel breakout strategy targeting trend continuation after volatility expansion. Enters when price closes outside the Keltner Channel bands. CCI filter avoids entries when price is already over-extended (CCI at extremes), improving entry quality.

### Keltner Channel Construction
- **Midline (EMA):** EMA(20)
- **Upper band:** EMA(20) + ATR(20) × 2.0
- **Lower band:** EMA(20) - ATR(20) × 2.0

### Entry — Long
1. Close **above** upper Keltner band (bullish breakout)
2. CCI(20) > -100 (not deeply oversold — confirms bullish momentum, not a dead-cat bounce)

### Entry — Short
1. Close **below** lower Keltner band (bearish breakdown)
2. CCI(20) < 100 (not deeply overbought)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** EMA midline price at entry (price returning to midline = failed breakout)
- **Take Profit:** `entry + stop_distance × 3` (long) / `entry - stop_distance × 3` (short) → 1:3 R:R

### Implementation Note on Stop Loss
Using EMA as stop means the stop-loss distance is dynamic:
- At entry, `stop = entry_price - ema_at_entry`
- This is different from ATR-based stop
- For backtesting: calculate `stop_distance = entry_price - ema_at_entry` and use `rr_ratio × stop_distance` for TP

### Filters
- Day-of-week filter (all days enabled by default)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `kc_length` | 20 | [15, 20, 25] |
| `kc_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `cci_period` | 20 | [14, 20, 28] |
| `cci_long_min` | -100 | [-100, -50, 0] |
| `cci_short_max` | 100 | [0, 50, 100] |
| `atr_stop_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `rr_ratio` | 3.0 | [2.0, 3.0, 4.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, LINKUSDT

## Notes
- CCI filter is intentionally loose (>-100 for longs) — it's meant to exclude extreme cases only
- Keltner Channels are less susceptible to volatility spikes than Bollinger Bands (use ATR not StdDev)
- Consider also testing a variant where close must be ABOVE upper KC for 2 consecutive bars (confirmation)
