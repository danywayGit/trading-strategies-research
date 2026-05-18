# Strategy : Volume Profile Breakout

## Overview

| Field | Value |
|---|---|
| **ID** | `VP1` |
| **Name** | Volume Profile + Breakout |
| **Timeframe** | 1H |
| **Type** | Volume-driven / Breakout |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Build an approximate volume profile (POC, VAH, VAL) from historical OHLCV. Trade volume zone breakouts with volume spike confirmation.

**Angle**: None of the 9 existing backtests use volume as a primary signal. This is an uncorrelated factor.

## Volume Profile Construction (approximation)

1. Volume histogram per price level (bin = ATR/4)
2. **POC** = price level with highest volume
3. **VAH/VAL** = boundaries containing 70% of total volume
4. Update every new bar

## Logic

### Long — VAH Breakout
1. Price closes above VAH
2. Volume > 150% of 20-bar average
3. Price > POC (confirms bullish structure)

### Short — VAL Breakdown
1. Price closes below VAL
2. Volume > 150% average
3. Price < POC

## Risk Management

- SL: POC (volume center of gravity)
- TP: Opposite extreme of the VA
- Filter: ADX > 20 (anti-false-breakout in flat ranges)

## altFINS Relevance

- ✅ Screener data includes VOLUME, VOLUME_RELATIVE, SHORT_TERM_TREND
- ✅ Filtering assets with abnormally high volume
- ✅ 1H OHLCV for full backtest