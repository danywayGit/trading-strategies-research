# Strategy : Adaptive Regime Switcher

## Overview

| Field | Value |
|---|---|
| **ID** | `AR1` |
| **Name** | Market Regime Switcher |
| **Timeframe** | 4H |
| **Type** | Regime-based / Dynamic |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Detect the current market regime and automatically switch the active strategy.

| Regime | Characteristics | Active Strategy |
|---|---|---|
| Trend ↑ | ADX > 25 + Price > EMA200 | SWING3 (MACD trend) |
| Trend ↓ | ADX > 25 + Price < EMA200 | EMA_REJ_V1 (short side) |
| Range | ADX < 20 | RR1 (Mean rev) to be created |

## Logic

1. Classify regime every 50 bars
2. Switch to the optimal strategy for that regime
3. Filter: no trade if regime is ambiguous (ADX grey zone 20–25)

## Risk Management

- Inherits risk from each underlying strategy
- Max 1 active trade (switcher chooses, not a set)

## altFINS Relevance

- ✅ Screener SHORT_TERM_TREND = regime indicator
- ✅ ADX available in screener data types
- ✅ Walk-forward test possible on sub-strategies