# EMA_REJ_V2 — EMA200 Rejection v2 (Confirmed Stay + RSI Threshold)

**Timeframe:** 1H or 4H (recommended)
**Direction:** Long and Short
**Target R:R:** 1:2
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Improved version of EMA_REJ_V1. Same core idea — trade failed recoveries and failed breakdowns at the EMA200 — but with two additional quality filters to reduce false signals in choppy markets:

1. **Minimum confirmation bars**: Price must have stayed on the rejection side of EMA200 for at least N bars *before* the initial false cross, proving it had context there.
2. **RSI threshold filter**: RSI must be below a ceiling (short) or above a floor (long) at entry, preventing entries into over-extended momentum.

### Rejection Pattern (3-phase)

**Short (failed recovery):**
- Phase 1: Price below EMA200 for ≥ `min_bars_below_ema` consecutive bars (context)
- Phase 2: Price briefly crosses ABOVE EMA200 (false recovery)
- Phase 3: Price crosses back BELOW EMA200 within `rejection_lookback` bars → SHORT entry

**Long (failed breakdown):**
- Phase 1: Price above EMA200 for ≥ `min_bars_above_ema` consecutive bars (context)
- Phase 2: Price briefly crosses BELOW EMA200 (false breakdown)
- Phase 3: Price crosses back ABOVE EMA200 within `rejection_lookback` bars → LONG entry

### Higher Timeframe Bias
- HTF approximated by EMA(ema200_length × htf_bars) on the current timeframe
- Short only when: close < HTF EMA (confirmed downtrend context)
- Long only when: close > HTF EMA (confirmed uptrend context)

### RSI Confirmation
- Use RSI(14) and EMA(9) of RSI as signal line
- **Short confirm:** RSI crossed below its EMA within last `rsi_confirm_window` bars
- **Long confirm:** RSI crossed above its EMA within last `rsi_confirm_window` bars
- **Short threshold:** RSI < `rsi_threshold_short` (default 55) — not overbought at entry
- **Long threshold:** RSI > `rsi_threshold_long` (default 45) — not oversold at entry

### Key Fix vs Original
The original Pine Script bug (`shortStayedBelow` always false) is corrected by tracking a **persistent bar counter** (`barsBeforeLastCrossAbove`) that snapshots how many consecutive bars price was below EMA200 immediately before the false cross-above occurred. This correctly captures Phase 1.

In Python: track `_bars_below_ema` (increments each bar close < EMA200, resets on cross above). On the moment of `cross_above`, snapshot `_bars_before_cross_above = _bars_below_ema`. The short entry fires when `_bars_before_cross_above >= min_bars_below_ema`.

### Stop Loss and Take Profit
- `stop_dist = ATR(14) × stop_mult` (default 3.0)
- **Long:** stop = entry − stop_dist, TP = entry + stop_dist × rr_ratio
- **Short:** stop = entry + stop_dist, TP = entry − stop_dist × rr_ratio

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `qty = (equity × risk_pct / 100) / stop_dist`

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `ema200_length` | 200 | [150, 200, 250] |
| `htf_bars` | 9 | [6, 9, 12] |
| `rejection_lookback` | 10 | [5, 10, 15] |
| `min_bars_below_ema` | 3 | [2, 3, 5, 8] |
| `min_bars_above_ema` | 3 | [2, 3, 5, 8] |
| `rsi_period` | 14 | [10, 14] |
| `rsi_ema_period` | 9 | [7, 9, 14] |
| `rsi_confirm_window` | 3 | [2, 3, 5] |
| `rsi_threshold_short` | 55 | [45, 50, 55, 60] |
| `rsi_threshold_long` | 45 | [40, 45, 50, 55] |
| `stop_mult` | 3.0 | [2.0, 3.0, 4.0] |
| `rr_ratio` | 2.0 | [1.5, 2.0, 2.5, 3.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, LINKUSDT

## Difference from EMA_REJ_V1

| Feature | V1 | V2 |
|---|---|---|
| Confirmation bars | None | ≥ N bars on correct side before false cross |
| RSI threshold | None | RSI < 55 (short) / RSI > 45 (long) |
| Signal frequency | Higher | Lower but higher quality |
| Chop resistance | Lower | Higher |

## Notes
- The 3-phase pattern is stricter and will fire less frequently than V1 — expect 20–40% fewer trades
- `min_bars_below/above_ema` is the key differentiator — higher values = stronger trend context required
- RSI thresholds prevent entering near exhaustion; test whether they add meaningful edge
- In fast trending markets (ADX > 30), V2 may miss many entries due to the mandatory context bars
- Pair with a volume filter (next iteration) to further improve quality
