# Strategy : Momentum Rotation Multi-Asset

## Overview

| Field | Value |
|---|---|
| **ID** | `MO1` |
| **Name** | Cross-Asset Momentum Rotation |
| **Timeframe** | 4H |
| **Type** | Rotation / Relative Momentum |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Calculate relative momentum for each asset (BTC, ETH, SOL, BNB, LINK). **Long the top performer**, short the worst performer, or **cash** if signals are weak.

**Asset selection is dynamic** — that’s where the alpha lies.

## Calculations

```
Relative Strength Index (RSI-like)
RS_asset_i = RSI(asset_i, 14) - RSI(benchmark, 14)

Benchmark = BTC by default

Top 1 = Long, Bottom 1 = Short (or cash if gap < threshold)
```

## Logic

1. **Top momentum asset**: Long with confirmation (ADX > 20 on that asset)
2. **Bottom asset**: Short if ADX > 20 (or cash for market-neutral mode)
3. **Rotating**: Switch when ranking changes OR when ADX < 15 (momentum fades)

## Risk Management

- SL: ATR × 2 on the traded asset
- TP: ATR-based trailing stop
- Max 1 long trade + 1 short trade (if pair mode)
- Minimum rotation period: 200 bars (~8.3 days) to avoid churn

## altFINS Relevance

- ✅ Multi-asset screener data — filter by SHORT_TERM_TREND + VOLUME_RELATIVE
- ✅ Get top performers/decliners in real time
- ✅ Multi-symbol OHLCV support