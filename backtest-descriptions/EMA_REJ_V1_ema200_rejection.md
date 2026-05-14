# EMA_REJ_V1 — EMA200 Rejection (Failed Breakout/Breakdown)

**Timeframe:** 1H or 4H (recommended)  
**Direction:** Long and Short (configurable)  
**Target R:R:** 1:2  
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
Counter-trend strategy that trades failed recoveries and failed breakdowns at the EMA200. When price briefly crosses to the "wrong" side of EMA200 then quickly reverses back, it signals strong rejection — the EMA200 is acting as hard resistance/support. A RSI momentum cross confirms the reversal.

### Key Signal: EMA200 Rejection

**Short (Failed Recovery):**
- Price was below EMA200 (downtrend)
- Price briefly crossed ABOVE EMA200 (attempted recovery)
- Price now crosses back BELOW EMA200 within `rejectionLookback` bars
- = Failed recovery → continue short

**Long (Failed Breakdown):**
- Price was above EMA200 (uptrend)
- Price briefly crossed BELOW EMA200 (attempted breakdown)
- Price now crosses back ABOVE EMA200 within `rejectionLookback` bars
- = Failed breakdown → continue long

### Higher Timeframe Context
- **HTF timeframe:** 9H (540 min) — confirming the dominant trend
- Short only when: HTF close < HTF EMA200 (confirmed downtrend)
- Long only when: HTF close > HTF EMA200 (confirmed uptrend)

### RSI Confirmation
- Uses RSI(14) and a smoothed EMA of RSI as signal line
- **Short confirm:** RSI crossed below its EMA within last `rsiConfirmWindow` bars
- **Long confirm:** RSI crossed above its EMA within last `rsiConfirmWindow` bars

> **Backtesting implementation note:** The Pine Script version uses an external RSI indicator as input source. For Python backtesting, compute RSI(14) inline and use EMA(9) of RSI as the signal line.

### Position Sizing
Risk-based: risk 1% of equity per trade.
- `stop_distance = ATR(14) × 3`
- `qty = (equity × risk_pct) / stop_distance`

### Exit
- **Stop Loss:** `entry - ATR×3` (long) / `entry + ATR×3` (short)
- **Take Profit:** 1:2 R:R

### Filters
- Day-of-week and hour-of-day filters
- Trade direction: Long / Short / Both

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|-----------|---------|-------------|
| `ema200_length` | 200 | [150, 200, 250] |
| `rejection_lookback` | 10 | [5, 10, 15] |
| `rsi_period` | 14 | [10, 14] |
| `rsi_ema_period` | 9 | [7, 9, 14] |
| `rsi_confirm_window` | 3 | [2, 3, 5] |
| `htf_timeframe` | "540" (9H) | ["240", "360", "540", "D"] |
| `stop_mult` | 3.0 | [2.0, 3.0, 4.0] |
| `rr_ratio` | 2.0 | [1.5, 2.0, 2.5, 3.0] |

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT, SOLUSDT, BNBUSDT, LINKUSDT

## Notes
- This is a counter-trend entry but WITH-trend at the HTF level — it's a pullback/rejection play
- The EMA200 is one of the most watched levels by institutional traders → self-fulfilling to some extent
- 3× ATR stop is wide by design (rejection entries need room for re-tests)
- Short bias on this strategy is stronger than long in bear markets — consider testing each direction separately
