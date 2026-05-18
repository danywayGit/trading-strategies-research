# Strategy : VWAP Mean Reversion

## Overview

| Field | Value |
|---|---|
| **ID** | `VR1` |
| **Name** | VWAP + Z-score |
| **Timeframe** | 1H |
| **Type** | Order Flow / Mean Reversion |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

VWAP = institutional benchmark reference. When price deviates strongly from VWAP **without** volume supporting continuation → mean reversion toward VWAP.

**Angle**: EMA_REJ_V1 works with EMA200 (long-term). VWAP is a similar anchor but more responsive (daily reset) and volume-weighted.

## Calculations

```
VWAP = Σ(Typical Price × Volume) / Σ(Volume)
Typical Price = (High + Low + Close) / 3
Daily reset

VWAP Bands = VWAP ± N × Std Deviation(price-VWAP over N periods)
Volume Anomaly Ratio = Volume[current] / MeanVolume[20]
```

## Entry Logic

### Long — Short exhaustion + low volume → Reversion
1. **Price < VWAP - 2σ (σ = standard deviation)**
2. **Volume Anomaly < 0.3** (abnormally low volume → no aggressive buyers)
3. **RSI(14) > 35** (confirms oversold)
4. Entry on reversal close

### Short — Long exhaustion + low volume → Reversion
1. Price > VWAP + 2σ
2. Volume < 0.3 average
3. RSI > 65
4. Entry on reversal close

## Risk Management

- SL: ± 1σ beyond the extreme (3σ total)
- TP: VWAP (mean) or VWAP ± 2σ (extension)
- Filter: no trade if VWAP band width < 0.5% (market too compressed)

## altFINS Relevance

- ✅ OHLCV with volume → VWAP calculable
- ✅ Screener VOLUME_RELATIVE confirmed
- ✅ Complementary with EMA_REJ_V1