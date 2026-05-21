# AR1 — Adaptive Regime Switcher

**Timeframe:** 4H
**Direction:** Long and Short (inherited from sub-strategies)
**Target R:R:** Inherited from active sub-strategy
**Exchange:** Binance Futures (USDT-M)

---

## Strategy Logic

### Concept
A meta-strategy that detects the current market regime and activates the most appropriate sub-strategy. No single strategy works well in all market conditions — AR1 rotates between Trend, Range, and Breakout strategies based on a simple ADX + EMA regime classifier.

### Regime Classification (evaluated every 50 bars)
| Regime | Condition | Active Sub-Strategy |
|---|---|---|
| **Trend Up** | `ADX(20) > adx_up` AND `close > EMA(200)` | SWING3 (Supertrend + ADX) |
| **Trend Down** | `ADX(20) > adx_down` AND `close < EMA(200)` | SWING3 (short mode only) |
| **Range / Choppy** | `ADX(20) < adx_range` | RR1 (Range Mean Reversion) |
| **Ambiguous (Grey Zone)** | `adx_range ≤ ADX ≤ adx_up/down` | No trade (standby) |

### Entry
1. Regime is classified → corresponding sub-strategy becomes active
2. Sub-strategy's own entry signals are evaluated
3. If the sub-strategy generates a valid entry → execute trade
4. If the sub-strategy has no signal → no trade

### Exit
- Inherits the sub-strategy's exit rules completely (SL, TP, time stop)
- **Regime switch override:** If the regime changes while a trade is open, evaluate:
  - If the existing trade's sub-strategy is now "wrong regime":
    - If trade is profitable (+0.5R or more): **Close immediately** and switch to new regime's strategy
    - If trade is not yet profitable: **Hold** until the trade's own exit triggers (don't cut winners early, but don't double down on wrong regime)

### Position Sizing
- Inherits risk per trade from the active sub-strategy (typically 1% equity)
- **Regime transition penalty:** If regime switches >2 times in 20 bars, reduce position size by 50% for the next entry (churn protection)

### Filters
- Grey Zone `adx_range=20` to `adx_up_down=25` → no trades, prevents whipsaw
- Maximum 1 active trade at a time
- Regime classification uses a **4H** timeframe regardless of sub-strategy's native timeframe (unified view)

---

## Parameters to Optimize

| Parameter | Default | Test Values |
|---|---|---|
| `adx_up` | 25 | [20, 25, 30] |
| `adx_down` | 25 | [20, 25, 30] |
| `adx_range` | 20 | [15, 20, 25] |
| `ema_trend` | 200 | [100, 200, 300] |
| `adx_lookback` | 20 | [14, 20, 30] |
| `reclass_interval` | 50 bars | [20, 50, 100] |
| `profit_take_on_switch` | 0.5R | [0.3, 0.5, 1.0R] |
| `churn_threshold_switches` | 2 | [1, 2, 3] |

### Sub-Strategy Parameters (inherited but optimizable)
- SWING3 parameters optimized independently
- RR1 parameters optimized independently
- AR1's own parameters are the regime boundaries + switch logic

---

## Suggested Test Symbols
BTCUSDT, ETHUSDT (liquid perps where all sub-strategies have historical data)

## Notes
- AR1 is a **meta-strategy** — it does not have its own entry/exit logic, it delegates to sub-strategies
- The key test: does knowing the regime matter? Or is it better to run all strategies simultaneously with equal weight?
- Grey zone is critical — if `adx_range` is too high, you miss trades. If too low, you enter whipsaws. Test carefully
- Regime switching frequency should be low in stable markets, higher in transitions. Monitor via backtest logs
- altFINS screener `SHORT_TERM_TREND = BUY/SELL/NEUTRAL` can serve as a second classifier layer if ADX-only classification proves insufficient
- Walk-forward test recommendation: optimize regime boundaries on 2024 data, test on 2025 live data
- This is the only strategy that **cannot** run standalone without its sub-strategies implemented first
