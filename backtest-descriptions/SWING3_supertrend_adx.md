# SWING3 — Supertrend + ADX (Strong Trend Following / Trailing)

**Timeframe:** 1H or 4H  
**Direction:** Long and Short  
**Target:** Trail via Supertrend (no fixed TP)  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Trend-following strategy using Supertrend as both entry signal and trailing stop. ADX confirms the trend is strong enough to trade. EMA50 acts as a directional bias filter. Position is held until Supertrend flips direction — designed to capture large trending moves.

### Entry — Long
1. Supertrend direction flips from bearish → bullish (flip up signal)
2. ADX(14) > 25 (strong trend confirmed)
3. Close > EMA(50) (uptrend bias)

### Entry — Short
1. Supertrend direction flips from bullish → bearish (flip down signal)
2. ADX(14) > 25 (strong trend confirmed)
3. Close < EMA(50) (downtrend bias)

### Supertrend Parameters
- Period: 10
- Factor (ATR multiplier): 3.0

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 2.5` (used for initial sizing only)
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Trailing:** Close long when Supertrend turns bearish. Close short when Supertrend turns bullish.
- **No fixed take profit** — let the trend run until reversal.

### Filters
- Day-of-week filter (all days enabled by default)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `st_period` | 10 | [7, 10, 14] |
| `st_factor` | 3.0 | [2.0, 3.0, 4.0] |
| `adx_threshold` | 25 | [20, 25, 30] |
| `ema_filter` | 50 | [50, 100, 200] |
| `adx_period` | 14 | [10, 14] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT (high-liquidity trending assets first)

## Notes
- No fixed TP makes this strategy highly sensitive to trailing stop parameters
- Best in clearly trending markets — will underperform in ranging crypto (altcoins in accumulation)
- Consider testing with and without EMA50 filter to measure its impact on signal quality
- ADX > 25 is standard "trending" threshold; ADX > 30 gives fewer but higher-quality entries
