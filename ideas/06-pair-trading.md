# Strategy : Pair Trading BTC/ETH (Z-score)

## Overview

| Field | Value |
|---|---|
| **ID** | `PT1` |
| **Name** | BTC/ETH Statistical Arbitrage |
| **Timeframe** | 1H |
| **Type** | Pair / Market-Neutral |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Trade the BTC/ETH ratio. When the ratio deviates strongly from its mean (Z-score), bet on mean reversion.

**Unique**: Only market-neutral approach. Existing results: drawdowns -15% to -32%. Pair trading reduces beta exposure.

## Calculations

```
Ratio = Price(BTC) / Price(ETH)
Z-score = (ratio - mean_50) / std_50
Entry |Z| > 2, Exit Z→ 0
```

## Logic

- **Z < -2** → Long BTC, Short ETH (ETH too expensive)
- **Z > +2** → Short BTC, Long ETH (BTC too expensive)
- Close both sides when Z → 0
- Sizing: equal notional on both sides

## Risk Management

- SL: Z exceeds ±3 OR combined drawdown > 5%
- Max holding: 200 bars
- 2x trading fees → validate that signal justifies the costs

## altFINS Relevance

- ✅ Multi-symbol OHLCV (BTC + ETH)
- ✅ Screener data for real-time correlation
- ✅ Requires Binance Futures for short side