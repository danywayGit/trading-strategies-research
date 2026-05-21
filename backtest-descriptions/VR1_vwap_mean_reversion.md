# VR1 — VWAP Mean Reversion (Z-score + Volume Exhaustion)

**Timeframe:** 1H
**Direction:** Long and Short
**Target R:R:** 1:1.5 to VWAP
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
VWAP is the institutional benchmark reference. When price deviates strongly from VWAP **without** volume supporting continuation, the move is likely exhausted and will revert. VWAP bands (± standard deviation) define the extremes. This complements EMA_REJ_V1, which uses EMA200 as a long-term anchor — VWAP is a shorter-term, volume-weighted anchor with daily reset.

### VWAP Construction
- **VWAP:** Cumulative sum of `(typical_price × volume) / cumulative_sum(volume)`, daily reset
- **Typical Price:** `(high + low + close) / 3`
- **VWAP Bands:** `VWAP ± band_mult × stddev(close - VWAP, period)`
- **Volume Anomaly Ratio:** `volume / SMA(volume, vol_avg_period)`

### Entry — Long (Short Exhaustion + Low Volume → Reversion)
All conditions must be true:
1. **Lower extreme:** Price closes below `VWAP − 2σ` (band_mult = 2)
2. **Volume exhaustion:** Volume Anomaly Ratio < 0.3 (abnormally low volume = no conviction)
3. **Oversold confirmation:** RSI(14) > 35 (not too extreme — some oversold but reversal-capable)
4. **Reversal trigger:** Next bar closes back above the lower band boundary

### Entry — Short (Long Exhaustion + Low Volume → Reversion)
All conditions must be true (inverse logic):
1. Price closes above `VWAP + 2σ`
2. Volume Anomaly Ratio < 0.3
3. RSI(14) < 65
4. Next bar closes back below the upper band boundary

### Stop Loss
- **Long:** `stop = entry − (band_width × 1.5)` where `band_width = VWAP − lower_band`
  - Effectively places SL ~1.5σ beyond the entry extreme
- **Short:** `stop = entry + (band_width × 1.5)`

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = abs(entry - stop)`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **TP1:** Close at VWAP (mean) — primary target for most trades
- **TP2:** Optional extension target at `2σ` on the opposite side of VWAP (takes larger moves)
- **Stop Loss:** Full exit at SL price
- **Max holding:** 150 bars (~6.25 days on 1H)

### Filters
- Max 1 active trade at a time
- No trade if VWAP band width < 0.5% of price → market too compressed, insufficient room
- Daily reset: no new entries in the first 2 bars after reset (VWAP instability zone)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `vwap_period` | daily reset | [daily, 200 bars] |
| `band_mult` | 2.0 | [1.5, 2.0, 2.5] |
| `band_std_period` | 50 | [30, 50, 100] |
| `volume_exhaustion_threshold` | 0.3 | [0.2, 0.3, 0.4] |
| `volume_avg_period` | 20 | [14, 20, 30] |
| `rsi_period` | 14 | [10, 14, 21] |
| `rsi_oversold_floor` | 35 | [30, 35, 40] |
| `rsi_overbought_ceil` | 65 | [60, 65, 70] |
| `min_band_width_pct` | 0.5 | [0.3, 0.5, 0.8] |
| `tp_extension` | 1.0 | [0.5, 1.0, 2.0] |

---

## Suggested Test Symbols
ETHUSDT, BTCUSDT, SOLUSDT (high-liquidity perps with reliable VWAP behavior)

## Notes
- VWAP daily reset behavior on Binance: ensure reset happens at 00:00 UTC (Binance server time), not local time
- Volume exhaustion filter is the key edge — breakouts on low volume are statistically more likely to fail. Test whether 0.3 is optimal or too tight
- RSI floor/ceil prevents entering when price is already reversing (RSI already bounced back)
- Band width filter prevents overtrading in hyper-compressed markets where 2σ may be 0.1% away
- VWAP mean reversion works best during Asian/London overlap on crypto — consider testing session filters
- Complementary to EMA_REJ_V1: VWAP catches shorter deviations, EMA200 catches macro rejections. They may overlap in counter-trend moves — be careful if running live together
