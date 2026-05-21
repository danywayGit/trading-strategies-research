# A01 — Screener Signal Composite (SHORT_TERM_TREND + VOLUME_RELATIVE)

**Timeframe:** 4H
**Direction:** Long and Short
**Target R:R:** 1:2
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
The altFINS Screener API returns pre-calculated technical signals (`SHORT_TERM_TREND`) and volume context (`VOLUME_RELATIVE`) for each asset. Use the screener's BUY/SELL signal as the primary entry trigger, validate signal strength with relative volume, and confirm market structure with a separate EMA(50) structural filter. This is the first strategy in the portfolio that is 100% dependent on altFINS Screener data, designed to validate whether pre-packaged technical signals generate alpha.

### Data Source
- **Screener:** `screener_getCryptoAssets` → returns list of assets with technical properties
- **OHLCV:** Used separately to fetch EMA(50) and ATR(14) for the signal asset
- **Signal Frequency:** Screener data queried every bar (4H)

### Entry — Long
All conditions must be true:
1. **Screener Signal:** `SHORT_TERM_TREND = BUY`
2. **Volume Strength:** `VOLUME_RELATIVE > 100` (volume above historical average confirms conviction)
3. **Structural Confirmation:** `close > EMA(50)` fetched via separate OHLCV call (price above trend)
4. **ADX filter:** `ADX(14) > 20` on the asset (trend is strong enough to follow)

### Entry — Short
All conditions must be true (inverse logic):
1. `SHORT_TERM_TREND = SELL`
2. `VOLUME_RELATIVE > 100`
3. `close < EMA(50)`
4. `ADX(14) > 20`

### Asset Selection
- Scan the top 20 highest-volume USDT-M perpetuals via screener
- Select the **first asset** (highest market cap) that meets all conditions
- If no asset qualifies, no trade

### Stop Loss
- `stop_distance = ATR(14) × 2`
- **Long:** `stop = entry - stop_distance`
- **Short:** `stop = entry + stop_distance`

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **TP1:** 50% at 1R (take half at 1x risk)
- **TP2:** 50% at 2R (trail rest with ATR×2 trailing stop)
- **Signal Reversal:** Close all if `SHORT_TERM_TREND` flips to opposite signal (BUY→SELL or SELL→BUY) or switches to `NEUTRAL/HOLD`
- **Max holding:** 200 bars (~33 days on 4H)

### Filters
- `VOLUME_RELATIVE` must be in the **top quartile** of the current screener scan (volume spike relative to peers, not just >100 in absolute terms)
- No trade if the asset has a major event within the next 24h (if calendar integration is available)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `volume_relative_threshold` | 100 | [80, 100, 120] |
| `volume_quartile_filter` | 75 | [50, 75, 90] |
| `ema_structural` | 50 | [20, 50, 100] |
| `adx_threshold` | 20 | [15, 20, 25] |
| `atr_period` | 14 | [10, 14, 21] |
| `sl_atr_mult` | 2.0 | [1.5, 2.0, 3.0] |
| `tp1_rr` | 1.0 | [0.8, 1.0, 1.5] |
| `tp2_rr` | 2.0 | [1.5, 2.0, 3.0] |
| `max_assets_scanned` | 20 | [10, 20, 50] |

---

## Suggested Test Symbols
Dynamic — selected from top 20 USDT-M perps by screener scan

## Notes
- This is the **only** strategy that does not hard-code a symbol list — asset selection is live and dynamic
- The screener's `SHORT_TERM_TREND` is a black-box composite of unknown indicators → backtest validates whether pre-packaged signals have edge
- If `SHORT_TERM_TREND` is derived from indicators already in SWING3/AGGR_PB, signals may overlap → check decorrelation
- Volume relative threshold of 100 means "at or above average" — the **quartile filter** is the real edge (volume must be abnormally high vs peers)
- Test with and without EMA(50) structural confirmation to measure its impact on whipsaw reduction
- Screener data freshness is critical — if the API returns stale data, signals will be misaligned. Add a staleness check (reject if data older than X minutes)
- Expect higher latency in execution vs pure OHLCV strategies due to API call overhead
