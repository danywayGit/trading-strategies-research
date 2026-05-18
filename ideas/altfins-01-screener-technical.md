# 100% altFINS Strategy : Screener Technical Signal

## Overview

| Field | Value |
|---|---|
| **ID** | `A01` |
| **Name** | Screener Signal Composite |
| **Timeframe** | 4H |
| **Type** | Composite signal / Trend |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

The altFINS Screener API returns a pre-calculated technical signal (`SHORT_TERM_TREND`) based on multiple indicators. Use this signal as an entry component, combined with relative volume to validate signal strength.

**Unique**: None of the 9 existing backtests use `SHORT_TERM_TREND` or VOLUME_RELATIVE. This is a way to validate whether the Screener tool itself generates alpha.

## Logic

### Long
1. Screener SHORT_TERM_TREND = **BUY**
2. Screener VOLUME_RELATIVE > **100** (abnormally high volume on the trend)
3. Confirmation: Price > EMA(50) via separate OHLCV call (confirm structure)

### Short
1. Screener SHORT_TERM_TREND = **SELL**
2. Screener VOLUME_RELATIVE > 100
3. Price < EMA(50)

## Risk Management

- SL: ATR(14) × 2
- TP: ATR trailing stop
- Exit if SHORT_TERM_TREND = HOLD / NEUTRAL
- Max 1 active trade at a time (the screener already selects the optimal asset)

## altFINS Relevance

- ✅ **100% screener-dependent** — SHORT_TERM_TREND, VOLUME_RELATIVE
- ✅ `screener_getCryptoAssets` → filter → select → entry
- ✅ Complementary: no duplicate technical indicators