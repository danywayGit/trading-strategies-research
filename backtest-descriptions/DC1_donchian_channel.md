# DC1 — Donchian Channel + ATR Filter (Mini Turtle)

**Timeframe:** 4H (primary), 1H (secondary test)
**Direction:** Long and Short
**Target R:R:** Trailing exit (no fixed TP)
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Classic Donchian Channel breakout (price breaks 20-bar high/low) validated by ADX trend strength and exited with an ATR trailing stop. Simpler and less prone to overfitting than Keltner channels (SWING5), because Donchian uses raw price extremes rather than moving-average-weighted volatility bands.

### Donchian Channel Construction
- **Upper Band:** Highest high of last `donchian_length` bars
- **Lower Band:** Lowest low of last `donchian_length` bars
- **Middle Band:** (Upper + Lower) / 2 (informational only)

### Entry — Long
All conditions must be true:
1. **Breakout:** `close > upper_band` (price closes above 20-period highest high)
2. **ADX confirmation:** `ADX(14) > adx_threshold` → trend is strong enough to follow
3. **Volume spike:** `volume > SMA(volume, vol_avg_period) × vol_mult` → breakout has conviction

### Entry — Short
All conditions must be true (inverse logic):
1. `close < lower_band`
2. `ADX(14) > adx_threshold`
3. `volume > SMA(volume, vol_avg_period) × vol_mult`

### Stop Loss
- **Initial SL:** `stop = entry - (ATR(14) × sl_atr_mult)` for long; inverse for short
- **Trailing Stop:** Activate trailing after price moves +1R in profit. Trail distance = `ATR(14) × trail_atr_mult`
  - Trailing moves with price (never widens), updated every bar

### Exit
- **Trailing stop hit:** Primary exit
- **ADX reversal:** Close if `ADX(14) < adx_exit` (trend dies)
- **Donchian exit:** Close if price closes back inside the channel AND opposite Donchian signal triggers (e.g., long exits on lower band break)
- **Max holding:** 200 bars (~33 days on 4H)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × sl_atr_mult`
- `qty = (equity × risk_pct) / stop_distance`

### Filters
- No new entry within 20 bars of the previous exit (avoid whipsaw after breakout failure)
- Minimum channel width: `(upper_band - lower_band) / close > 0.01` (1% width minimum → market not compressed)
- No entry on the first 4 bars after a Donchian signal fire (wait for confirmation close)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `donchian_length` | 20 | [15, 20, 25, 55] |
| `adx_threshold` | 25 | [20, 25, 30] |
| `adx_exit` | 20 | [15, 20, 25] |
| `sl_atr_mult` | 2.0 | [1.5, 2.0, 3.0] |
| `trail_atr_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `atr_period` | 14 | [10, 14, 21] |
| `vol_avg_period` | 20 | [14, 20, 30] |
| `vol_mult` | 1.0 | [0.8, 1.0, 1.2] |
| `min_channel_width_pct` | 1.0 | [0.5, 1.0, 2.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT (liquid perps where breakout signals are most reliable)

## Notes
- Donchian is famously prone to **breakout whipsaws** in ranging markets — the ADX filter is critical, but test whether `ADX > 25` is too loose
- The trailing stop means there is no theoretical profit cap → large trends capture significant R (Turtle advantage)
- Test Donchian vs Keltner (SWING5) head-to-head: Donchian should have fewer false signals, Keltner may catch earlier entries in volatile regimes
- Volume spike filter prevents "fake" breakouts that lack participation. If `vol_mult = 1.0`, any volume above average qualifies. Test if `1.2` is more realistic
- Channel width filter avoids trading in hyper-compressed markets where `upper - lower` is too narrow for meaningful SL placement
- Walk-forward recommendation: optimize `donchian_length` per market regime (20 for trends, 55 for volatile/choppy)
