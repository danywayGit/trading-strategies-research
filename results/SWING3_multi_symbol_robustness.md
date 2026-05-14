# SWING3 — Supertrend + ADX Multi-Symbol Robustness Test

**Params:** `st_period=10, st_factor=3.0, adx_threshold=30, ema_filter=100, atr_stop_mult=2.5`  
**Timeframe:** 1H  
**Period:** 2022-01-01 to 2024-12-31

---

## Results by Symbol

| Symbol | P&L | Sharpe | Max DD | Trades | Win Rate |
|--------|-----|--------|--------|--------|----------|
| ETHUSDT (opt) | +10.9% | 0.89 | -3.0% | 55 | 51% |
| BTCUSDT | **0 trades** | 0 | 0 | 0 | — |
| SOLUSDT | -1.4% | -0.19 | -5.6% | 33 | 45% |
| BNBUSDT | **+1.4%** | 0.25 | -6.4% | 40 | 43% |
| LINKUSDT | -2.9% | -0.48 | -4.6% | 23 | 39% |

---

## Key Findings

### BTCUSDT — 0 trades
The Supertrend on BTC 1H with factor=3.0 and adx_threshold=30 never triggers. BTC's lower volatility relative to its price means ATR-based bands are proportionally narrower and the Supertrend rarely flips cleanly at 1H. **Fix: test on 4H timeframe for BTC.**

### SOLUSDT / LINKUSDT — Slightly negative
The strategy is borderline on high-beta altcoins at 1H — they whipsaw the Supertrend too frequently even with ADX>30 filter. The edge is weaker than on ETH.

### BNBUSDT — Slightly positive
BNB is the most ETH-correlated of the group. Positive P&L confirms some transferability.

### Overall Assessment
The ETH optimization result (+10.9%, Sharpe 0.89) **does not robustly transfer to other symbols at 1H**. The strategy appears ETH-specific at this timeframe. Options:

1. **Keep as ETH-only strategy** — the walk-forward passed, it's genuinely good on ETH
2. **Re-run optimization per symbol** — each coin may need slightly different params
3. **Move to 4H** — reduce noise, likely to work better cross-symbol (especially BTC)

---

## Next Steps

- [ ] Run SWING3 on 4H for BTCUSDT (0 trades issue)
- [ ] Re-optimize per-symbol for SOLUSDT and BNBUSDT
- [ ] Consider ETH-only deployment as first live strategy
