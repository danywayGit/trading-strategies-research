# VP1 — Volume Profile Breakout (POC + VAH/VAL)

**Timeframe:** 1H
**Direction:** Long and Short
**Target R:R:** 1:2
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Constructs an approximate volume profile from recent OHLCV data by binning volume into price levels. Trades breakouts above VAH (Value Area High) or breakdowns below VAL (Value Area Low), confirmed by a volume spike. None of the 9 existing strategies use volume as a primary signal, making this an uncorrelated alpha factor.

### Volume Profile Construction (approximation)
- **Bin size:** `ATR(14) / 4` — adaptive to volatility
- **POC (Point of Control):** Price level with the highest total volume accumulated
- **VAH / VAL:** Upper and lower price boundaries that contain 70% of total volume (Value Area)
- **Update:** Recalculated every new bar from the last `lookback` bars (default 200)

### Entry — Long (VAH Breakout)
All conditions must be true:
1. **Breakout:** Current bar closes above VAH
2. **Volume spike:** Current volume > 150% of the 20-bar average volume
3. **Structure:** Close > POC (price above volume center of gravity = bullish)
4. **Trend filter:** ADX(14) > 20 (avoids false breakouts in compression)

### Entry — Short (VAL Breakdown)
All conditions must be true (inverse logic):
1. Current bar closes below VAL
2. Current volume > 150% of 20-bar average
3. Close < POC
4. ADX(14) > 20

### Stop Loss
- **Long:** `stop = POC` (volume center of gravity as natural support)
- **Short:** `stop = POC` (volume center of gravity as natural resistance)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = abs(entry - POC)`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **TP1:** 50% at `VA_height` (distance from VAH to VAL) above entry (long) or below entry (short)
- **TP2:** 50% at 2 × `VA_height` from entry
- **Stop Loss:** Full exit at POC if it closes back inside the Value Area
- **Max holding:** 300 bars (~12.5 days on 1H)

### Filters
- Max 1 active trade at a time
- No trade if Value Area height < 0.5% of price (market too compressed, no room for breakout)
- No re-entry within 20 bars after exiting (cooldown to avoid chop)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `profile_lookback` | 200 | [100, 200, 300] |
| `value_area_pct` | 70 | [60, 70, 80] |
| `volume_spike_mult` | 1.5 | [1.2, 1.5, 2.0] |
| `volume_avg_period` | 20 | [14, 20, 30] |
| `adx_threshold` | 20 | [15, 20, 25] |
| `tp1_mult` | 1.0 | [0.8, 1.0, 1.5] |
| `tp2_mult` | 2.0 | [1.5, 2.0, 3.0] |
| `min_va_pct` | 0.5 | [0.3, 0.5, 0.8] |
| `cooldown_bars` | 20 | [10, 20, 30] |

---

## Suggested Test Symbols
ETHUSDT, SOLUSDT, LINKUSDT (assets with clear volume accumulation patterns)

## Notes
- Volume profile approximation is inherently noisy — bin size matters enormously. Test different ATR divisions (3, 4, 5)
- POC as stop loss is conceptually elegant but may be wide on assets with flat volume profiles — expect smaller position sizes
- The ADX filter is a judgment call: remove it to test whether volume alone is sufficient
- VAH/VAL breakout is conceptually similar to SWING5 (Keltner breakout), but volume-weighted — they should diverge in choppy conditions
- Real volume profile on TradingView uses session-based data; this approximation may over-fit on backtest if lookback window is wrong
- Expect higher hit rate on 1H than 4H — breakouts need a tighter timeframe to avoid premature signals
