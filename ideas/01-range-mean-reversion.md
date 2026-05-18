# Strategy : Range Mean Reversion (RSI + BB + Stoch)

## Overview

| Field | Value |
|---|---|
| **ID** | `RR1` |
| **Name** | Range Mean Reversion |
| **Timeframe** | 4H |
| **Type** | Mean Reversion / Anti-trend |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Identify range-bound phases (ADX < 20) and trade extremes with multi-indicator confirmation: RSI, Bollinger Band, Stochastic.

## Entry Logic

### Long
1. **ADX(14) < 20** → sideways market
2. **Price touches/crosses lower BB** (SMA20 ± 2×ATR)
3. **RSI(14) < 30** → oversold
4. **Stochastic(14,3,3) %K crosses above %D** in zone < 20
5. Entry on confirmation close

### Short (reversed)
1. ADX < 20
2. Price touches upper BB
3. RSI > 70
4. Stochastic %K crosses below %D, zone > 80

## Risk Management

- SL: Opposite extreme of the range
- TP: SMA20 (mean) for TP1 (50%), opposite extreme for TP2 (50%)
- Max 1 trade (either long or short, not both)

## Backtest Parameters

```json
{
  "symbol": "ETH",
  "timeframe": "4h",
  "period": "2025-01-01 to 2026-03-29",
  "walk_forward": true,
  "test_matrix": {
    "rr_ratio": [1.5, 2.0, 2.5],
    "adx_threshold": [15, 20, 25],
    "rsi_oversold": [25, 30, 35],
    "rsi_overbought": [65, 70, 75]
  }
}
```

## Relevance

- **Gap**: No pure mean reversion strategy among the 9 existing ones
- **Complementarity**: Works when SWING3 (MACD trend) is inactive

## Verified altFINS Data

- ✅ Screener data: SHORT_TERM_TREND, RSI, ATR available
- ✅ Screener filters allow targeting range-bound assets
- ✅ OHLCV for backtest via `ohlc_getHistoryData`