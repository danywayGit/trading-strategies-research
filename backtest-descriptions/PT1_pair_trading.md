# PT1 — BTC/ETH Pair Trading (Z-score)

**Timeframe:** 1H
**Direction:** Long BTC / Short ETH OR vice versa (market-neutral legs)
**Target R:R:** Return to mean (Z → 0), trailing stop on spread
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Trade the BTC/ETH price ratio using a Z-score mean-reversion approach. When the ratio deviates significantly from its rolling mean, enter the counter-directional side. This is the **only market-neutral strategy** in the portfolio — net beta exposure is ~0 if sized correctly, removing directional market risk.

### Ratio Construction
- **Ratio:** `Ratio = Price(BTCUSDT) / Price(ETHUSDT)`
- **Rolling Mean:** `mean_50 = SMA(Ratio, lookback)`
- **Rolling Std:** `std_50 = StdDev(Ratio, lookback)`
- **Z-score:** `z = (Ratio - mean) / std`

### Entry — Long BTC / Short ETH (Ratio Too Low → ETH Expensive)
All conditions must be true:
1. **Z < -z_entry** (ratio is more than `z_entry` standard deviations below mean)
2. **Correlation check:** Rolling 50-bar correlation between BTC and ETH > 0.7 (pair relationship valid)
3. **No existing position:** Both legs closed before entering

### Entry — Short BTC / Long ETH (Ratio Too High → BTC Expensive)
All conditions must be true:
1. **Z > +z_entry**
2. Same correlation check

### Stop Loss
- **Z-stop:** Exit if `|z|` exceeds `z_max` (e.g., Z > ±3) → divergence continuing against you
- **Combined drawdown stop:** Exit if the unrealized P&L of the combined position exceeds `-max_dd_pct` of equity (e.g., -5%)
- **Max holding:** 200 bars (~8.3 days on 1H)

### Position Sizing
Equal Notional on both legs to maintain market neutrality:
- `notional = equity × allocation_pct` (e.g., 10% of equity split across pair)
- **BTC Qty:** `qty_btc = notional / Price(BTC)`
- **ETH Qty:** `qty_eth = notional / Price(ETH)`
- One leg is long, one is short (not direction, just opposite sides)

### Exit
- **Primary:** Close both legs when `|z| < z_exit` (ratio returns to mean zone)
- **Z-stop hit:** Close both legs
- **Combined DD hit:** Close both legs
- **Time exit:** Close at max holding regardless of Z

### Filters
- Minimum correlation threshold (rolling): 0.7 → if pairs decouple, Z is meaningless
- No trade if ratio spread volatility is below 0.03 (ratio too flat, insufficient move)
- Maximum 1 pair trade at a time

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `lookback` | 50 | [30, 50, 100] |
| `z_entry` | 2.0 | [1.5, 2.0, 2.5] |
| `z_exit` | 0.5 | [0.0, 0.3, 0.5] |
| `z_max` | 3.0 | [2.5, 3.0, 4.0] |
| `allocation_pct` | 10.0 | [5, 10, 20] |
| `max_dd_pct` | 5.0 | [3, 5, 10] |
| `min_correlation` | 0.7 | [0.5, 0.7, 0.9] |
| `max_hold_bars` | 200 | [100, 200, 400] |

---

## Suggested Test Symbols
Pair only: BTCUSDT + ETHUSDT

## Notes
- **Fee impact is doubled** — 2 positions, 2 entry + 2 exit fees per trade. Average win must clear 2x fees to be viable
- BTC/ETH ratio can be range-bound for months or diverge sharply during bull runs (ETH outperformance) → test across multiple market cycles
- Correlation check is critical: during 2022 crash, BTC and ETH decoupled briefly → Z-score loses meaning, correlation filter should reject
- Pair trading is mathematically elegant but practically noisy on crypto (exchanges are not perfectly arbitrage-enforcing pairs). Test with and without the correlation filter
- Alternative pair: BTC/SOL if ETH correlation weakens over time
- If `z_exit = 0.0`, trade closes only at exact mean → test whether `0.0, 0.3, 0.5` significantly changes win rate vs average win
- Not a true arbitrage — this is statistical mean-reversion, not simultaneous cash-and-carry
