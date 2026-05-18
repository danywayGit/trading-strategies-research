# Strategy : Event Catalyst Alpha

## Overview

| Field | Value |
|---|---|
| **ID** | `EC1` |
| **Name** | Calendar + News → Alpha |
| **Timeframe** | 1H–4H |
| **Type** | Event-driven |
| **Status** | Raw idea |
| **Date** | 2026-03-29 |

## Concept

Use events (listings, airdrops, mainnets, partnerships) detected by altFINS to adjust positions and trade fundamental catalysts.

**Unique**: None of the 9 existing backtests integrate fundamental data. Events create abnormal volatility not predicted by technical indicators.

## altFINS Sources

| altFINS Tool | Role |
|---|---|
| `getCryptoCalendarEvents` | Retrieves listings, airdrops, conferences, partnerships, protocol releases |
| `news_getCryptoNewsMessages` | Recent articles for an asset → context enrichment |
| Screener data | Technical context around the event |

## Logic

**Pre-event phase (24h before)**
1. Detect high-impact event (e.g., major exchange listing, protocol airdrop)
2. Reduce leverage / exit positions → avoid unmanageable volatility
3. Optional: tighten SL to ATR × 1

**Post-event phase (post-discovery)**
1. Wait 200 bars post-event (24h) for price discovery to settle
2. Evaluate the new regime: trend continuation OR mean reversion
3. Re-enter with existing strategies (SWING3, EMA_REJ) but wider SL (× 3 ATR) during stabilization

## Risk Management

- **Pre-event exit**: no position if major event within 24h.
- **Post-event sizing**: position size reduced by 50% during stabilization phase.
- **Max drawdown stop**: exit if -5% post-event → catalyst negates initial thesis.

## altFINS Relevance

- ✅ 100% dependent on altFINS APIs
- ✅ Purely fundamental alpha → complementary to all technical baskets
- ✅ Requires webhook bot integration for real-time execution