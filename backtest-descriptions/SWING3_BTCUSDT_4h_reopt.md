# SWING3 — Supertrend + ADX on BTCUSDT 4H (Re-Optimization)

**Reason for Re-Opt:** BTCUSDT 1H produced 0 trades (Supertrend never flipped with factor=3.0 + ADX>30). Moving to 4H for bigger moves and looser thresholds.

**Period:** 2023-01-01 → 2024-12-31 (2 years, 4H bars)

---

## Modified Spec

### Changes from Original
1. **Timeframe:** 1H → 4H (wider swings, Supertrend has room to flip)
2. **Symbol:** BTCUSDT (was ETHUSDT)
3. **ADX threshold:** 30 → 20 (lower bar to increase signal frequency)
4. **EMA filter:** 100 → 200 (slower filter for 4H timeframe)
5. **ATR stop mult:** 2.5 → 2.0 (wider stops relative to 4H ATR)

### Parameters to Re-Optimize

| Parameter | Values |
|--|--|
| `st_period` | [7, 10, 14] |
| `st_factor` | [2.5, 3.0, 3.5] |
| `adx_threshold` | [20, 25] |
| `adx_period` | [14] |
| `ema_filter` | [50, 100, 200] |
| `atr_stop_mult` | [2.0, 2.5] |

**Combinations:** 3×3×2×1×3×2 = **108**

### Position Sizing
- Risk 1% equity per trade
- `stop_distance = ATR(14) × atr_stop_mult`
- `qty = (equity × 0.01) / stop_distance`

### Exit
- Supertrend flip (trailing)
- No fixed TP

---

## Walk-Forward Split
- **Train:** 2023-01-01 → 2024-06-15 (70%)
- **Test:** 2024-06-15 → 2024-12-31 (30%)
- **Acceptance:** Test Sharpe ≥ Train Sharpe × 0.70, test trade count ≥20
