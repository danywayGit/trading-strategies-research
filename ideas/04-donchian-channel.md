# Strategy : Donchian Channel + ATR Filter

## Overview

| Field | Value |
|---|---|
| **ID** | `DC1` |
| **Name** | Donchian Turtle |
| **Timeframe** | 1H–4H |
| **Type** | Breakout |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Break 20-period highs/lows (Mini Turtle) with ADX filter and ATR trailing stop.

**Why**: SWING5 (Keltner) failed walk-forward. Keltner = EMA + 1.5×ATR (weighted). Donchian = highest high / lowest low — less prone to overfitting but potentially more robust.

## Logic

### Long
1. Price closes > highest high of last 20 periods
2. ADX(14) > 25 → trend confirmed

### Short
1. Price closes < lowest low of last 20 periods
2. ADX(14) > 25 → trend confirmed

## Risk Management

- Initial SL: ATR(14) × 2 below/above entry
- Trailing stop: ATR × 2, updated every bar
- No fixed TP — exit via trailing stop

## altFINS Relevance

- ✅ Screener data: SHORT_TERM_TREND filters assets in breakout
- ✅ VOLUME_RELATIVE confirms the breakout
- ✅ 1H historical data