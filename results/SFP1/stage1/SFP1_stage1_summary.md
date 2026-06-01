# SFP1 — Stage 1 Summary (5M, 39 symbols)

**Date:** 2026-06-01
**Pass filter:** num_trades ≥ 30 AND OOS Sharpe > 0
**Total combos:** 117 / 117  (39 symbols × 3 dir × 1 SL types)
**Pass rate:** 35 / 117

---

## Pass/Fail Table

| Symbol | both/emb | long/emb | short/emb |
|---|---|---|---|
| BTCUSDT | ❌ | ❌ | ❌ |
| ETHUSDT | ❌ | ❌ | ❌ |
| SOLUSDT | ✅ | ❌ | ❌ |
| BNBUSDT | ❌ | ❌ | ❌ |
| ADAUSDT | ✅ | ❌ | ❌ |
| DOGEUSDT | ✅ | ❌ | ❌ |
| DOTUSDT | ❌ | ❌ | ✅ |
| LINKUSDT | ✅ | ❌ | ✅ |
| LTCUSDT | ✅ | ❌ | ❌ |
| BCHUSDT | ✅ | ❌ | ❌ |
| UNIUSDT | ❌ | ❌ | ❌ |
| AAVEUSDT | ❌ | ❌ | ❌ |
| ATOMUSDT | ✅ | ❌ | ❌ |
| FILUSDT | ✅ | ❌ | ❌ |
| INJUSDT | ✅ | ✅ | ❌ |
| AVAXUSDT | ✅ | ❌ | ❌ |
| NEARUSDT | ✅ | ❌ | ❌ |
| TRXUSDT | ✅ | ❌ | ❌ |
| ALGOUSDT | ❌ | ❌ | ❌ |
| SANDUSDT | ❌ | ✅ | ✅ |
| MANAUSDT | ❌ | ❌ | ❌ |
| RUNEUSDT | ❌ | ❌ | ❌ |
| AXSUSDT | ✅ | ❌ | ❌ |
| DASHUSDT | ✅ | ❌ | ❌ |
| ETCUSDT | ❌ | ❌ | ✅ |
| CHZUSDT | ✅ | ✅ | ✅ |
| SHIBUSDT | ❌ | ❌ | ✅ |
| ICPUSDT | ❌ | ❌ | ❌ |
| FLOWUSDT | ❌ | ❌ | ❌ |
| FETUSDT | ✅ | ❌ | ❌ |
| DYDXUSDT | ❌ | ❌ | ❌ |
| OPUSDT | ✅ | ❌ | ❌ |
| GMXUSDT | ❌ | ❌ | ✅ |
| APTUSDT | ❌ | ✅ | ❌ |
| ARBUSDT | ✅ | ✅ | ✅ |
| SUIUSDT | ❌ | ❌ | ❌ |
| SEIUSDT | ❌ | ✅ | ❌ |
| ENAUSDT | ❌ | ✅ | ✅ |
| TAOUSDT | ✅ | ❌ | ❌ |

---

## Passing Combos (proceed to Stage 2)

| Symbol | Direction | SL Type | OOS Sharpe | Train Sharpe | Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|
| ENAUSDT | short | embedded | 2.0921 | 1.381 | 54 | -9.07 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ARBUSDT | long | embedded | 1.9478 | -0.4682 | 127 | -19.64 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| CHZUSDT | both | embedded | 1.5329 | 1.2364 | 284 | -48.75 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| DOGEUSDT | both | embedded | 1.4721 | 0.2927 | 778 | -64.42 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| TAOUSDT | both | embedded | 1.4548 | 1.8772 | 192 | -40.36 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| GMXUSDT | short | embedded | 1.3849 | 1.7093 | 204 | -14.69 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ADAUSDT | both | embedded | 1.1801 | 0.8191 | 371 | -35.81 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| SOLUSDT | both | embedded | 1.0851 | 1.1543 | 1020 | -60.78 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| SANDUSDT | long | embedded | 0.961 | -0.3761 | 259 | -34.27 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| INJUSDT | both | embedded | 0.8845 | 1.032 | 654 | -61.36 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ATOMUSDT | both | embedded | 0.8455 | 0.4279 | 827 | -75.05 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| OPUSDT | both | embedded | 0.7359 | 1.2429 | 162 | -43.0 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| SEIUSDT | long | embedded | 0.7317 | 2.1899 | 54 | -7.69 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ENAUSDT | long | embedded | 0.7238 | 1.3249 | 187 | -23.49 | `{"lookback_bars": 24, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| DASHUSDT | both | embedded | 0.6913 | 0.8759 | 730 | -40.78 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| FETUSDT | both | embedded | 0.6489 | 1.0154 | 227 | -56.92 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| APTUSDT | long | embedded | 0.6343 | 1.2509 | 135 | -17.28 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| SANDUSDT | short | embedded | 0.5478 | 0.5028 | 740 | -25.46 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| CHZUSDT | long | embedded | 0.5138 | 0.5569 | 389 | -16.76 | `{"lookback_bars": 24, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ARBUSDT | both | embedded | 0.5041 | 1.0663 | 516 | -55.92 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ARBUSDT | short | embedded | 0.4915 | 1.6861 | 117 | -14.72 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| AVAXUSDT | both | embedded | 0.4899 | 0.4085 | 744 | -64.23 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| DOTUSDT | short | embedded | 0.4793 | 0.2633 | 240 | -27.35 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| LTCUSDT | both | embedded | 0.4588 | 1.4991 | 776 | -33.16 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| FILUSDT | both | embedded | 0.4286 | 1.109 | 213 | -39.81 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| BCHUSDT | both | embedded | 0.3823 | 0.9894 | 487 | -31.59 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| NEARUSDT | both | embedded | 0.2111 | 0.3559 | 1334 | -74.48 | `{"lookback_bars": 24, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| INJUSDT | long | embedded | 0.2013 | 0.9993 | 772 | -35.67 | `{"lookback_bars": 72, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| SHIBUSDT | short | embedded | 0.1765 | -0.1235 | 206 | -19.65 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| LINKUSDT | short | embedded | 0.1647 | -0.8569 | 482 | -40.7 | `{"lookback_bars": 24, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| TRXUSDT | both | embedded | 0.1527 | 0.5112 | 403 | -45.63 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| LINKUSDT | both | embedded | 0.1017 | 0.4495 | 1274 | -66.84 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| AXSUSDT | both | embedded | 0.0938 | 0.3576 | 789 | -72.21 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| CHZUSDT | short | embedded | 0.0336 | 0.3403 | 547 | -39.89 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |
| ETCUSDT | short | embedded | 0.0155 | 0.5307 | 237 | -20.24 | `{"lookback_bars": 48, "swing_lookback": 3, "max_ltf_wait_bars": 12, "use_bias...` |

**Stage 1 pass rate: 35 / 117**
