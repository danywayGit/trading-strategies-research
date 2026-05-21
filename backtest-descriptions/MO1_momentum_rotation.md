# MO1 — Cross-Asset Momentum Rotation

**Timeframe:** 4H
**Direction:** Long and Short (single asset at a time)
**Target R:R:** 1:2 (trailing exit)
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Rank assets by relative momentum (RSI vs BTC benchmark). Go long the top-performing asset and/or short the worst-performing asset, validated by ADX trend strength. Asset selection is dynamic — the alpha lies in **which** asset trades, not just when.

### Universe
- Fixed basket: BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, LINKUSDT (top 5 by volume)
- Benchmark: BTCUSDT (always in universe, acts as relative baseline)
- Minimum 4 symbols active for ranking to be valid

### Momentum Calculation
- **Relative RSI:** `RSI(asset, 14) - RSI(BTC, 14)`
- Positive value = asset outperforming BTC, negative = underperforming
- Re-calculated every bar; ranking updated from sorted list

### Entry — Long (Top Performer)
All conditions must be true:
1. **Rank #1:** Asset has highest Relative RSI in the basket
2. **Momentum threshold:** Relative RSI > 5 (gap large enough to matter)
3. **Trend confirmation on that asset:** `ADX(14) > 20` on the selected asset (trend exists)
4. **No trade if rotation churn prevention:** Last rotation for this asset was < 200 bars ago (minimum holding period)

### Entry — Short (Bottom Performer) — Optional
Inverse logic; disable for long-only mode:
1. **Rank last (bottom):** Asset has lowest Relative RSI
2. **Momentum threshold:** Relative RSI < -5
3. **Trend confirmation:** `ADX(14) > 20`
4. **Rotation churn prevention:** Same 200-bar minimum

### Exit
- **Trailing stop:** `ATR(14) × 2` trailed every bar (move with price, never widen)
- **Rotation trigger:** Exit current position if another asset displaces it from Rank #1 or Rank #last
- **ADX fade:** Exit if `ADX(14) < 15` (trend dying)
- **Max holding:** 200 bars (~33 days on 4H)

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2`
- `qty = (equity × risk_pct) / stop_distance`

### Filters
- No trade if the top/bottom asset's Relative RSI gap from the median is < 3 (market is flat, no real alpha)
- No new entry if a trade was closed on trailing stop within the last 10 bars (cool-down)
- Maximum 1 open trade at a time (not a pair)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `universe_symbols` | [BTC, ETH, SOL, BNB, LINK] | [top 3, top 5, top 10] |
| `rsi_period` | 14 | [10, 14, 21] |
| `momentum_threshold` | 5 | [3, 5, 8] |
| `adx_trend_confirm` | 20 | [15, 20, 25] |
| `adx_exit_fade` | 15 | [10, 15, 20] |
| `sl_atr_mult` | 2.0 | [1.5, 2.0, 3.0] |
| `atr_period` | 14 | [10, 14, 21] |
| `min_rotation_gap` | 200 bars | [50, 100, 200] |
| `max_hold_bars` | 200 | [100, 200, 400] |

---

## Suggested Test Symbols
Dynamic — selected from universe basket via relative ranking

## Notes
- This is the **only** strategy that ranks across multiple assets simultaneously — requires multi-symbol OHLCV
- Momentum rotation works best when crypto markets are not in a panic dump (BTC dominance stable)
- Test with and without `ADX < 15` exit filter — ADX fade may prevent premature exits
- If the top asset's Relative RSI is barely above threshold, the rotation churn prevention (200 bars) becomes load-bearing
- Fee impact: expect 5–15 trades/month → validate that average win covers 2x fees (entry + exit)
- altFINS screener can provide live SHORT_TERM_TREND as a secondary filter for rotation candidates
- Correlation risk: if ETH and SOL are both in the basket, they may flip-flop between #1 and #2 frequently → monitor rotation frequency
