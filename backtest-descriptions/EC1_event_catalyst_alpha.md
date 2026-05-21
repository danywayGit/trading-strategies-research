# EC1 — Event Catalyst Alpha (News + Calendar → Alpha)

**Timeframe:** 1H–4H
**Direction:** Long or Short (context-dependent)
**Target R:R:** Variable (1:1 to 1:3 depending on event magnitude)
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Fundamental data (calendar events, news, announcements) creates volatility that technical indicators cannot predict. This strategy uses altFINS API data to detect high-impact events, position pre-event, and trade the post-event regime shift.

**Unique:** The only strategy in the portfolio that uses fundamental events as a primary alpha source. All other strategies are purely technical.

### Data Sources (altFINS API)
| API | What It Provides | Role |
|---|---|---|
| `screener_getCryptoAssets` | Asset list with technical filters | Universe selection |
| `news_getCryptoNewsMessages` | Recent news per asset | Sentiment enrichment |
| `getCryptoCalendarEvents` | Listings, airdrops, mainnets, partnerships, releases | Event detection |

### Phase 1 — Pre-Event Detection (Event → Prepare)
1. Query calendar for high-impact events (exchange listing, major partnership, protocol upgrade, airdrop)
2. Event must be:
   - Confirmed (not rumor/speculation)
   - High impact score ≥ `event_impact_min` (7/10)
   - Within the next `event_lookahead_hours` hours (default 48h)
3. Reduce position size by `pre_event_size_reduction` (default 75%) or exit entirely
4. Tighten SL to `ATR(14) × pre_event_sl_mult` (default 1.0× → half-width stop)
5. No new entries if a high-impact event is within the lookahead window → prevent entering into volatility

### Phase 2 — Post-Event Entry (Variance Expansion → Trade)
After the event timestamp passes:
1. Wait `post_event_wait_bars` bars (default: 4 bars = 1 day on 4H) for price discovery to settle
2. Identify the new prevailing direction:
   - **Bullish catalyst:** Price closes > `entry_ema` (e.g., EMA50) within 10 bars post-event
   - **Bearish catalyst:** Price closes < `entry_ema`
3. Enter in the discovered direction
4. Use wider SL during stabilization: `ATR(14) × post_event_sl_mult` (default 3.0×)

### Phase 3 — Exit
- **TP1:** 50% at `post_event_tp_rr` (default 1.5R)
- **TP2:** 50% trailed with `ATR(14) × trail_mult` (default 2.0×)
- **Stop Loss:** Wider stop during stabilization phase (×3 ATR)
- **Max holding:** `post_event_max_bars` (default 150 bars)
- **Catalyst invalidation:** If news sentiment flips to negative post-event → close immediately
- **Max drawdown stop:** Exit if -`max_dd_pct` (default 5%) post-event entry → event failed to move as expected

### Position Sizing
Risk-based with event-specific adjustments:
- **Pre-event:** Position size reduced by 75% (avoid overexposure to volatility)
- **Post-event entry:** `stop_distance = ATR(14) × post_event_sl_mult`
- `qty = (equity × risk_pct_post) / stop_distance`
- `risk_pct_post` = 0.5% (half-normal risk, events are unpredictable)

### Filters
- Minimum event impact score: ≥ 7 (only "notable" events)
- Maximum 1 event trade at a time
- No trade if the asset has a second high-impact event within 24h of the first (compounding volatility)
- altFINS news sentiment: no entry if news sentiment is mixed/contradictory

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `event_impact_min` | 7 | [5, 7, 9] |
| `event_lookahead_hours` | 48 | [24, 48, 72] |
| `post_event_wait_bars` | 4 | [2, 4, 8] |
| `entry_ema` | 50 | [20, 50, 100] |
| `pre_event_sl_mult` | 1.0 | [0.5, 1.0, 1.5] |
| `post_event_sl_mult` | 3.0 | [2.0, 3.0, 4.0] |
| `post_event_tp_rr` | 1.5 | [1.0, 1.5, 2.0] |
| `trail_mult` | 2.0 | [1.5, 2.0, 3.0] |
| `risk_pct_post` | 0.5 | [0.3, 0.5, 1.0] |
| `max_dd_pct` | 5.0 | [3, 5, 10] |

---

## Suggested Test Symbols
Dynamic — selected per event (any USDT-M perpetual with a high-impact calendar entry)

## Notes
- **This is the only altFINS-dependent strategy that is not technical** — alpha comes from event timing, not indicators
- Requires reliable altFINS API uptime and near-real-time event data → backtest will use simulated event timestamps from historical calendars
- Pre-event protection (reduce size / tighten SL) is as important as post-event entry
- Event types matter: exchange listings tend to pump, protocol upgrades can go either way, airdrops often pump-dump. Optimize per-event-type sub-strategies
- Post-event wait period prevents getting wrecked by immediate variance explosions
- Test event frequency: expect 5–15 high-impact events/month across the entire alt coin universe → low trade frequency, high conviction
- altFINS news sentiment API provides a second confirmation layer: if the technical pattern says "long" but news says "bearish" → skip
- Historical validation: align major known events (e.g., SOL mainnet upgrade, BNB listings) with price action to verify the framework
