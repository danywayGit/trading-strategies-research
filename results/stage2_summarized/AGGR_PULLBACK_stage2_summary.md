# AGGR_PULLBACK — Stage 2 Summary (home TF: 4H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 1h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 297 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 143 / 297

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ATOMUSDT | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| FILUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ✅ | ✅ |
| OPUSDT | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| ARBUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 1H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ✅ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ATOMUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| FILUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ✅ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ |
| OPUSDT | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| ARBUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ATOMUSDT | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| FILUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| OPUSDT | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| ARBUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| CHZUSDT | 1h | both | atr | 2.8854 | 1.6445 | 46 | -48.88 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| TRXUSDT | 1h | long | fixed_pct | 2.6798 | 1.8128 | 22 | -19.96 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| TRXUSDT | 1h | long | fixed_signal | 2.6798 | 1.8128 | 22 | -19.96 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| DOTUSDT | 1h | both | fixed_pct | 2.415 | 1.4159 | 17 | -10.43 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| DOTUSDT | 1h | both | fixed_signal | 2.415 | 1.4159 | 17 | -10.43 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| AXSUSDT | 15m | short | fixed_pct | 2.3436 | 1.4643 | 23 | -37.05 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| AXSUSDT | 15m | short | fixed_signal | 2.3436 | 1.4643 | 23 | -37.05 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| DOGEUSDT | 1h | both | embedded | 2.1279 | 1.0816 | 16 | -33.35 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| TRXUSDT | 1h | both | fixed_pct | 2.1049 | 0.9924 | 41 | -30.65 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| TRXUSDT | 1h | both | fixed_signal | 2.1049 | 0.9924 | 41 | -30.65 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 15m | short | fixed_pct | 2.0279 | 1.7851 | 71 | -21.45 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 15m | short | fixed_signal | 2.0279 | 1.7851 | 71 | -21.45 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ARBUSDT | 15m | both | fixed_pct | 1.9423 | 2.3135 | 46 | -23.0 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ARBUSDT | 15m | both | fixed_signal | 1.9423 | 2.3135 | 46 | -23.0 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ATOMUSDT | 1h | both | embedded | 1.9312 | 1.4382 | 36 | -40.04 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 1h | both | fixed_pct | 1.8613 | 1.1341 | 22 | -21.68 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 1h | both | fixed_signal | 1.8613 | 1.1341 | 22 | -21.68 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ALGOUSDT | 15m | both | embedded | 1.8175 | 2.5999 | 67 | -15.7 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| DOGEUSDT | 15m | both | embedded | 1.7225 | 1.0521 | 98 | -52.57 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| AXSUSDT | 1h | short | fixed_pct | 1.6486 | 1.3971 | 20 | -26.97 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| AXSUSDT | 1h | short | fixed_signal | 1.6486 | 1.3971 | 20 | -26.97 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ATOMUSDT | 1h | short | atr | 1.5873 | 1.5425 | 14 | -29.75 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| CHZUSDT | 1h | both | embedded | 1.5776 | 1.512 | 14 | -37.25 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| DOTUSDT | 15m | both | fixed_pct | 1.5551 | 2.2129 | 36 | -25.04 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| DOTUSDT | 15m | both | fixed_signal | 1.5551 | 2.2129 | 36 | -25.04 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| ARBUSDT | 1h | both | fixed_pct | 1.5451 | 2.0644 | 49 | -22.38 | `{"ema_length": 20, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| ARBUSDT | 1h | both | fixed_signal | 1.5451 | 2.0644 | 49 | -22.38 | `{"ema_length": 20, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| CHZUSDT | 15m | both | embedded | 1.5351 | 1.8229 | 12 | -20.18 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| FILUSDT | 1h | both | embedded | 1.4859 | 1.4277 | 26 | -26.35 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| SUIUSDT | 1h | both | atr | 1.4493 | 1.833 | 18 | -25.81 | `{"ema_length": 20, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| TRXUSDT | 15m | long | fixed_pct | 1.3268 | 1.0071 | 25 | -30.94 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| TRXUSDT | 15m | long | fixed_signal | 1.3268 | 1.0071 | 25 | -30.94 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ALGOUSDT | 1h | short | atr | 1.32 | 2.4883 | 50 | -25.24 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| CHZUSDT | 15m | both | atr | 1.2822 | 1.7636 | 36 | -25.85 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| TRXUSDT | 15m | both | fixed_pct | 1.2772 | 0.3203 | 92 | -56.0 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| TRXUSDT | 15m | both | fixed_signal | 1.2772 | 0.3203 | 92 | -56.0 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 15m | both | fixed_pct | 1.2706 | 2.7166 | 168 | -25.23 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 15m | both | fixed_signal | 1.2706 | 2.7166 | 168 | -25.23 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| DYDXUSDT | 1h | short | atr | 1.23 | 1.5027 | 13 | -16.53 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| UNIUSDT | 15m | long | fixed_pct | 1.2249 | 1.1064 | 60 | -26.41 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| UNIUSDT | 15m | long | fixed_signal | 1.2249 | 1.1064 | 60 | -26.41 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ALGOUSDT | 15m | both | atr | 1.2215 | 2.496 | 67 | -19.8 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| APTUSDT | 15m | short | atr | 1.2078 | 1.8028 | 9 | -7.82 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| AVAXUSDT | 1h | short | embedded | 1.2005 | 2.3395 | 19 | -34.33 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| DYDXUSDT | 1h | short | embedded | 1.1781 | 1.1164 | 29 | -47.06 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| UNIUSDT | 15m | short | embedded | 1.173 | 1.4363 | 11 | -18.07 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| SOLUSDT | 15m | both | atr | 1.1659 | 1.3763 | 177 | -47.98 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 12h | both | fixed_pct | 1.1091 | 0.3941 | 15 | -30.39 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| DYDXUSDT | 12h | both | fixed_signal | 1.1091 | 0.3941 | 15 | -30.39 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 15m | short | embedded | 1.1056 | 1.1837 | 63 | -21.32 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| DYDXUSDT | 1h | short | fixed_pct | 1.0976 | 1.2445 | 13 | -15.23 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 1h | short | fixed_signal | 1.0976 | 1.2445 | 13 | -15.23 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| UNIUSDT | 15m | both | fixed_pct | 1.0863 | 1.3988 | 12 | -8.68 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| UNIUSDT | 15m | both | fixed_signal | 1.0863 | 1.3988 | 12 | -8.68 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| AVAXUSDT | 1h | short | atr | 1.0086 | 2.498 | 29 | -26.21 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 1h | short | embedded | 0.998 | 2.0301 | 28 | -35.53 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| GMXUSDT | 1h | both | embedded | 0.9921 | 2.5957 | 54 | -35.28 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| BTCUSDT | 15m | both | atr | 0.9564 | 1.1185 | 43 | -10.02 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| UNIUSDT | 15m | long | atr | 0.9388 | 1.0434 | 51 | -34.46 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| UNIUSDT | 15m | both | embedded | 0.9381 | 1.2007 | 11 | -26.22 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| AVAXUSDT | 1h | both | atr | 0.9217 | 2.4084 | 57 | -54.01 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| LINKUSDT | 15m | both | fixed_pct | 0.8979 | 1.2048 | 62 | -19.74 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 15m | both | fixed_signal | 0.8979 | 1.2048 | 62 | -19.74 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| ETCUSDT | 15m | both | fixed_pct | 0.8434 | 0.9456 | 105 | -39.19 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ETCUSDT | 15m | both | fixed_signal | 0.8434 | 0.9456 | 105 | -39.19 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| AXSUSDT | 1h | short | atr | 0.8363 | 1.2137 | 49 | -54.27 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 1h | both | fixed_pct | 0.8332 | 1.4627 | 33 | -25.55 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ATOMUSDT | 1h | both | fixed_signal | 0.8332 | 1.4627 | 33 | -25.55 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| CHZUSDT | 15m | long | atr | 0.8227 | 1.6688 | 72 | -32.2 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| ATOMUSDT | 1h | short | fixed_pct | 0.82 | 2.1501 | 15 | -14.55 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ATOMUSDT | 1h | short | fixed_signal | 0.82 | 2.1501 | 15 | -14.55 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ALGOUSDT | 1h | both | fixed_pct | 0.7841 | 1.9839 | 61 | -27.02 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 1h | both | fixed_signal | 0.7841 | 1.9839 | 61 | -27.02 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 1h | short | embedded | 0.7256 | 1.9262 | 18 | -28.48 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| AXSUSDT | 15m | short | atr | 0.7159 | 1.6672 | 54 | -46.12 | `{"ema_length": 20, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| OPUSDT | 15m | both | fixed_pct | 0.6983 | 0.8764 | 64 | -32.27 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| OPUSDT | 15m | both | fixed_signal | 0.6983 | 0.8764 | 64 | -32.27 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| MANAUSDT | 15m | both | atr | 0.6936 | 1.7066 | 80 | -28.4 | `{"ema_length": 20, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| FILUSDT | 15m | short | atr | 0.6462 | 1.3507 | 53 | -34.51 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| AVAXUSDT | 15m | short | atr | 0.6366 | 1.3966 | 94 | -39.56 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| LINKUSDT | 1h | both | fixed_pct | 0.6268 | 1.4307 | 17 | -24.45 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 1h | both | fixed_signal | 0.6268 | 1.4307 | 17 | -24.45 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 15m | long | fixed_pct | 0.6132 | 0.3757 | 122 | -46.0 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| LINKUSDT | 15m | long | fixed_signal | 0.6132 | 0.3757 | 122 | -46.0 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| AVAXUSDT | 1h | both | embedded | 0.609 | 2.4887 | 56 | -32.28 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| AVAXUSDT | 1h | both | fixed_pct | 0.5998 | 2.9057 | 44 | -15.04 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| AVAXUSDT | 1h | both | fixed_signal | 0.5998 | 2.9057 | 44 | -15.04 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ICPUSDT | 15m | both | fixed_pct | 0.5834 | 0.8966 | 131 | -48.19 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| ICPUSDT | 15m | both | fixed_signal | 0.5834 | 0.8966 | 131 | -48.19 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| DOGEUSDT | 1h | both | fixed_pct | 0.5772 | 1.9591 | 43 | -19.84 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| DOGEUSDT | 1h | both | fixed_signal | 0.5772 | 1.9591 | 43 | -19.84 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| LINKUSDT | 1h | long | atr | 0.544 | 0.5652 | 9 | -38.19 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 12h | both | fixed_pct | 0.5359 | 0.2039 | 4 | -21.88 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| LINKUSDT | 12h | both | fixed_signal | 0.5359 | 0.2039 | 4 | -21.88 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| ALGOUSDT | 15m | short | fixed_pct | 0.5273 | 2.3343 | 68 | -32.75 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 15m | short | fixed_signal | 0.5273 | 2.3343 | 68 | -32.75 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 5, "massive_can...` |
| DOTUSDT | 12h | both | fixed_pct | 0.5132 | 0.6925 | 4 | -21.29 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| DOTUSDT | 12h | both | fixed_signal | 0.5132 | 0.6925 | 4 | -21.29 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| ALGOUSDT | 12h | both | fixed_pct | 0.4379 | 1.1591 | 10 | -17.39 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 12h | both | fixed_signal | 0.4379 | 1.1591 | 10 | -17.39 | `{"ema_length": 20, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| ATOMUSDT | 15m | short | atr | 0.4361 | 1.4554 | 17 | -21.23 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| DYDXUSDT | 15m | short | atr | 0.4345 | 1.3832 | 63 | -29.06 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| AVAXUSDT | 15m | short | embedded | 0.3924 | 1.2775 | 58 | -40.3 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| UNIUSDT | 1h | both | embedded | 0.3894 | 1.0722 | 31 | -46.0 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| ICPUSDT | 1h | short | atr | 0.3878 | 1.5393 | 38 | -18.43 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| LINKUSDT | 1h | long | fixed_pct | 0.385 | 0.5368 | 11 | -17.78 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 1h | long | fixed_signal | 0.385 | 0.5368 | 11 | -17.78 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| GMXUSDT | 15m | both | embedded | 0.3849 | 2.1323 | 35 | -20.1 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| UNIUSDT | 15m | short | atr | 0.3759 | 1.4393 | 7 | -7.97 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| UNIUSDT | 1h | short | embedded | 0.3644 | 1.0819 | 20 | -41.71 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| AVAXUSDT | 15m | both | atr | 0.3625 | 1.3345 | 129 | -58.66 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| OPUSDT | 15m | both | embedded | 0.3517 | 0.8722 | 24 | -58.6 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| DOGEUSDT | 15m | both | fixed_pct | 0.2977 | 1.1383 | 158 | -43.26 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| DOGEUSDT | 15m | both | fixed_signal | 0.2977 | 1.1383 | 158 | -43.26 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| BNBUSDT | 15m | both | embedded | 0.2959 | 1.1232 | 116 | -22.16 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| APTUSDT | 15m | short | fixed_pct | 0.2767 | 1.3024 | 45 | -33.21 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| APTUSDT | 15m | short | fixed_signal | 0.2767 | 1.3024 | 45 | -33.21 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| CHZUSDT | 15m | long | fixed_pct | 0.2671 | 1.7544 | 70 | -24.04 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| CHZUSDT | 15m | long | fixed_signal | 0.2671 | 1.7544 | 70 | -24.04 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| RUNEUSDT | 1h | both | embedded | 0.2437 | 2.1116 | 36 | -24.02 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| UNIUSDT | 1h | short | atr | 0.2342 | 1.141 | 16 | -21.82 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 10, "massive_ca...` |
| BTCUSDT | 15m | both | fixed_pct | 0.2304 | 0.8552 | 39 | -19.97 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| BTCUSDT | 15m | both | fixed_signal | 0.2304 | 0.8552 | 39 | -19.97 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| AVAXUSDT | 15m | both | embedded | 0.2257 | 1.5942 | 128 | -63.56 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| ALGOUSDT | 15m | short | embedded | 0.2228 | 2.6318 | 61 | -19.0 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| AVAXUSDT | 15m | both | fixed_pct | 0.2059 | 1.9725 | 124 | -32.29 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| AVAXUSDT | 15m | both | fixed_signal | 0.2059 | 1.9725 | 124 | -32.29 | `{"ema_length": 15, "pullback_tolerance": 0, "swing_lookback": 5, "massive_can...` |
| SUIUSDT | 15m | both | atr | 0.198 | 2.2694 | 19 | -10.14 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| SUIUSDT | 15m | both | fixed_pct | 0.1925 | 3.1084 | 19 | -7.24 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| SUIUSDT | 15m | both | fixed_signal | 0.1925 | 3.1084 | 19 | -7.24 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| ATOMUSDT | 15m | both | fixed_pct | 0.174 | 1.9589 | 37 | -15.64 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| ATOMUSDT | 15m | both | fixed_signal | 0.174 | 1.9589 | 37 | -15.64 | `{"ema_length": 20, "pullback_tolerance": 0, "swing_lookback": 10, "massive_ca...` |
| SUIUSDT | 1h | both | fixed_pct | 0.1666 | 2.0234 | 27 | -24.72 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| SUIUSDT | 1h | both | fixed_signal | 0.1666 | 2.0234 | 27 | -24.72 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |
| RUNEUSDT | 15m | both | embedded | 0.1585 | 1.989 | 129 | -41.79 | `{"ema_length": 25, "pullback_tolerance": 0, "swing_lookback": 7, "massive_can...` |
| MANAUSDT | 1h | both | atr | 0.149 | 2.068 | 27 | -17.79 | `{"ema_length": 25, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| BTCUSDT | 12h | both | fixed_pct | 0.1109 | -0.8097 | 10 | -45.58 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| BTCUSDT | 12h | both | fixed_signal | 0.1109 | -0.8097 | 10 | -45.58 | `{"ema_length": 15, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| DYDXUSDT | 15m | short | fixed_pct | 0.0906 | 1.3908 | 56 | -33.46 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 15m | short | fixed_signal | 0.0906 | 1.3908 | 56 | -33.46 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 7, "massive_can...` |
| DYDXUSDT | 15m | long | atr | 0.0704 | 0.4835 | 31 | -13.45 | `{"ema_length": 15, "pullback_tolerance": 1, "swing_lookback": 10, "massive_ca...` |
| LINKUSDT | 15m | long | atr | 0.0618 | 0.3642 | 143 | -52.31 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 5, "massive_can...` |
| DOTUSDT | 12h | both | atr | 0.0492 | 0.835 | 4 | -34.4 | `{"ema_length": 25, "pullback_tolerance": 2, "swing_lookback": 7, "massive_can...` |

**Stage 2 pass rate: 143 / 297**
