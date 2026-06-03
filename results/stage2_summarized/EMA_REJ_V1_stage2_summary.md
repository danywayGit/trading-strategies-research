# EMA_REJ_V1 — Stage 2 Summary (home TF: 1H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 4h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 489 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 124 / 489

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETHUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| DOGEUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| LINKUSDT | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| LTCUSDT | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ |
| FILUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ |
| INJUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| SANDUSDT | ⬜ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| AXSUSDT | ❌ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ICPUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| FETUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| GMXUSDT | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| APTUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ |
| SEIUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 4H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETHUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| DOGEUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| LINKUSDT | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ✅ |
| LTCUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ✅ |
| FILUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ |
| INJUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ❌ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| SANDUSDT | ⬜ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| AXSUSDT | ✅ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ✅ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| ICPUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| FETUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| GMXUSDT | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APTUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| SEIUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETHUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| DOGEUSDT | ⬜ | ❌ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| LINKUSDT | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| LTCUSDT | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| FILUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ |
| INJUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| NEARUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| SANDUSDT | ⬜ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| AXSUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ICPUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| FETUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| GMXUSDT | ❌ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| APTUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| SEIUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| ATOMUSDT | 4h | both | atr | 2.333 | 1.0095 | 9 | -11.56 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| ATOMUSDT | 4h | short | atr | 2.162 | -0.7142 | 13 | -39.72 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DOTUSDT | 15m | short | fixed_pct | 2.1194 | 0.9032 | 46 | -21.44 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| DOTUSDT | 15m | short | fixed_signal | 2.1194 | 0.9032 | 46 | -21.44 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| FILUSDT | 15m | both | fixed_pct | 2.1002 | 1.097 | 84 | -34.87 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| FILUSDT | 15m | both | fixed_signal | 2.1002 | 1.097 | 84 | -34.87 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| ATOMUSDT | 4h | both | fixed_pct | 2.068 | 1.4838 | 10 | -15.92 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ATOMUSDT | 4h | both | fixed_signal | 2.068 | 1.4838 | 10 | -15.92 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| AVAXUSDT | 15m | short | embedded | 2.0017 | 1.5279 | 66 | -42.15 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| AVAXUSDT | 15m | short | atr | 2.0017 | 1.5279 | 66 | -42.15 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| FILUSDT | 4h | both | fixed_pct | 1.5817 | 1.096 | 16 | -19.56 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| FILUSDT | 4h | both | fixed_signal | 1.5817 | 1.096 | 16 | -19.56 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ADAUSDT | 15m | short | atr | 1.5297 | 1.0392 | 64 | -36.25 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| AVAXUSDT | 15m | short | fixed_pct | 1.3535 | 2.0102 | 40 | -25.27 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| AVAXUSDT | 15m | short | fixed_signal | 1.3535 | 2.0102 | 40 | -25.27 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| FLOWUSDT | 4h | short | fixed_pct | 1.3451 | 0.0164 | 11 | -25.17 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| FLOWUSDT | 4h | short | fixed_signal | 1.3451 | 0.0164 | 11 | -25.17 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| FILUSDT | 15m | short | fixed_pct | 1.3398 | 1.197 | 46 | -27.94 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| FILUSDT | 15m | short | fixed_signal | 1.3398 | 1.197 | 46 | -27.94 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| BNBUSDT | 4h | both | embedded | 1.3322 | 1.0645 | 13 | -25.17 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DOTUSDT | 15m | short | embedded | 1.2926 | 0.6366 | 53 | -19.52 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| DOTUSDT | 15m | short | atr | 1.2926 | 0.6366 | 53 | -19.52 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| SANDUSDT | 15m | both | fixed_pct | 1.1917 | 1.9492 | 113 | -23.29 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| SANDUSDT | 15m | both | fixed_signal | 1.1917 | 1.9492 | 113 | -23.29 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| SHIBUSDT | 15m | both | fixed_pct | 1.1878 | 1.233 | 119 | -30.89 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| SHIBUSDT | 15m | both | fixed_signal | 1.1878 | 1.233 | 119 | -30.89 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| AXSUSDT | 15m | long | embedded | 1.1825 | 0.6542 | 31 | -22.97 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| AXSUSDT | 15m | long | atr | 1.1825 | 0.6542 | 31 | -22.97 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| ATOMUSDT | 15m | both | fixed_pct | 1.1753 | 1.5302 | 131 | -27.72 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| ATOMUSDT | 15m | both | fixed_signal | 1.1753 | 1.5302 | 131 | -27.72 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| LINKUSDT | 15m | short | atr | 1.1734 | 0.5717 | 77 | -25.13 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| BNBUSDT | 15m | long | fixed_pct | 1.1545 | 1.0417 | 52 | -14.36 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| BNBUSDT | 15m | long | fixed_signal | 1.1545 | 1.0417 | 52 | -14.36 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| TAOUSDT | 15m | both | fixed_pct | 1.1225 | 3.9032 | 43 | -18.84 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| TAOUSDT | 15m | both | fixed_signal | 1.1225 | 3.9032 | 43 | -18.84 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| AAVEUSDT | 4h | both | embedded | 1.1028 | 1.831 | 8 | -31.64 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| FILUSDT | 15m | short | embedded | 1.0895 | 1.0872 | 45 | -29.63 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| ATOMUSDT | 15m | both | atr | 1.0441 | 1.0782 | 157 | -40.97 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| LINKUSDT | 4h | both | fixed_pct | 1.0388 | 1.6885 | 15 | -9.96 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| LINKUSDT | 4h | both | fixed_signal | 1.0388 | 1.6885 | 15 | -9.96 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| SHIBUSDT | 4h | both | fixed_pct | 1.0092 | 1.1915 | 15 | -11.76 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SHIBUSDT | 4h | both | fixed_signal | 1.0092 | 1.1915 | 15 | -11.76 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| AXSUSDT | 15m | both | atr | 1.0026 | 0.6724 | 141 | -28.63 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DOTUSDT | 15m | long | fixed_pct | 0.9894 | 0.7905 | 49 | -11.99 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| DOTUSDT | 15m | long | fixed_signal | 0.9894 | 0.7905 | 49 | -11.99 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| SANDUSDT | 4h | short | fixed_pct | 0.9792 | 0.2235 | 8 | -23.82 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| SANDUSDT | 4h | short | fixed_signal | 0.9792 | 0.2235 | 8 | -23.82 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| ICPUSDT | 4h | both | embedded | 0.9688 | 0.5339 | 16 | -44.88 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| AXSUSDT | 4h | both | embedded | 0.9647 | 0.9869 | 9 | -42.81 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| AXSUSDT | 4h | both | atr | 0.9515 | 1.2653 | 13 | -39.88 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| BTCUSDT | 15m | long | fixed_pct | 0.941 | 1.1513 | 56 | -11.72 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| BTCUSDT | 15m | long | fixed_signal | 0.941 | 1.1513 | 56 | -11.72 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| DOTUSDT | 15m | long | embedded | 0.8654 | 0.9026 | 36 | -20.49 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| LINKUSDT | 15m | short | embedded | 0.8547 | 0.5348 | 78 | -22.72 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| DASHUSDT | 15m | long | embedded | 0.8423 | 0.3484 | 36 | -31.57 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DASHUSDT | 15m | long | atr | 0.8423 | 0.3484 | 36 | -31.57 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| LINKUSDT | 4h | short | atr | 0.8335 | -0.3213 | 14 | -34.52 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ATOMUSDT | 15m | long | embedded | 0.8218 | 1.4387 | 46 | -11.71 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| LINKUSDT | 15m | both | fixed_pct | 0.8074 | 0.9357 | 83 | -23.03 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| LINKUSDT | 15m | both | fixed_signal | 0.8074 | 0.9357 | 83 | -23.03 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| OPUSDT | 15m | short | atr | 0.776 | 2.1384 | 71 | -19.77 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| LTCUSDT | 15m | both | embedded | 0.7671 | -0.534 | 126 | -64.05 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| INJUSDT | 15m | long | fixed_pct | 0.7624 | 1.4683 | 48 | -33.06 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| INJUSDT | 15m | long | fixed_signal | 0.7624 | 1.4683 | 48 | -33.06 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| AAVEUSDT | 12h | both | embedded | 0.7468 | 0.4252 | 4 | -45.7 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ARBUSDT | 15m | long | embedded | 0.7376 | 1.1512 | 35 | -28.34 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| AXSUSDT | 15m | long | fixed_pct | 0.6925 | 0.4478 | 46 | -15.97 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| AXSUSDT | 15m | long | fixed_signal | 0.6925 | 0.4478 | 46 | -15.97 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| BTCUSDT | 15m | long | embedded | 0.6901 | 0.4643 | 63 | -16.34 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| BNBUSDT | 12h | both | embedded | 0.6714 | 0.3894 | 8 | -35.2 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DOGEUSDT | 12h | both | atr | 0.6498 | 0.7438 | 9 | -39.16 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| SANDUSDT | 15m | short | fixed_pct | 0.6317 | 1.6658 | 59 | -28.52 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| SANDUSDT | 15m | short | fixed_signal | 0.6317 | 1.6658 | 59 | -28.52 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| ATOMUSDT | 15m | short | embedded | 0.6217 | 1.2245 | 71 | -38.97 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| ATOMUSDT | 15m | short | atr | 0.6217 | 1.2245 | 71 | -38.97 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| DOGEUSDT | 15m | both | atr | 0.5736 | 0.8153 | 94 | -56.61 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| BCHUSDT | 4h | long | fixed_pct | 0.5548 | 0.0885 | 10 | -19.02 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| BCHUSDT | 4h | long | fixed_signal | 0.5548 | 0.0885 | 10 | -19.02 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SHIBUSDT | 12h | both | embedded | 0.5493 | 0.7721 | 4 | -40.15 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SHIBUSDT | 12h | both | atr | 0.5493 | 0.7721 | 4 | -40.15 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ALGOUSDT | 15m | short | embedded | 0.5374 | 1.2876 | 74 | -37.99 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ALGOUSDT | 15m | short | atr | 0.5374 | 1.2876 | 74 | -37.99 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| BTCUSDT | 4h | both | fixed_pct | 0.5225 | -0.2092 | 15 | -20.52 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| BTCUSDT | 4h | both | fixed_signal | 0.5225 | -0.2092 | 15 | -20.52 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| NEARUSDT | 4h | short | fixed_pct | 0.5132 | 0.7698 | 3 | -21.15 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| NEARUSDT | 4h | short | fixed_signal | 0.5132 | 0.7698 | 3 | -21.15 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| BNBUSDT | 15m | long | embedded | 0.5003 | 0.4742 | 66 | -13.82 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| APTUSDT | 15m | short | embedded | 0.4817 | 0.8661 | 33 | -23.61 | `{"ema200_length": 150, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| SUIUSDT | 15m | short | fixed_pct | 0.469 | 2.1269 | 9 | -31.49 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SUIUSDT | 15m | short | fixed_signal | 0.469 | 2.1269 | 9 | -31.49 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| NEARUSDT | 4h | both | embedded | 0.4492 | -0.5102 | 8 | -45.92 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SHIBUSDT | 4h | short | fixed_pct | 0.3983 | 0.1847 | 9 | -29.62 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SHIBUSDT | 4h | short | fixed_signal | 0.3983 | 0.1847 | 9 | -29.62 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SANDUSDT | 15m | long | embedded | 0.3949 | 1.3753 | 41 | -18.73 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| SEIUSDT | 4h | both | fixed_pct | 0.3754 | 1.111 | 7 | -16.14 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SEIUSDT | 4h | both | fixed_signal | 0.3754 | 1.111 | 7 | -16.14 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SEIUSDT | 15m | short | fixed_pct | 0.3728 | 1.8356 | 17 | -12.72 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| SEIUSDT | 15m | short | fixed_signal | 0.3728 | 1.8356 | 17 | -12.72 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| INJUSDT | 15m | long | atr | 0.3376 | 1.5752 | 34 | -38.75 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| LTCUSDT | 12h | both | embedded | 0.3239 | 1.1077 | 15 | -23.02 | `{"ema200_length": 200, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| FLOWUSDT | 15m | short | fixed_pct | 0.3007 | 1.365 | 41 | -28.06 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| FLOWUSDT | 15m | short | fixed_signal | 0.3007 | 1.365 | 41 | -28.06 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| GMXUSDT | 15m | short | fixed_pct | 0.278 | 1.2936 | 47 | -13.89 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| GMXUSDT | 15m | short | fixed_signal | 0.278 | 1.2936 | 47 | -13.89 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| SEIUSDT | 15m | both | fixed_pct | 0.2725 | 1.773 | 80 | -21.17 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| SEIUSDT | 15m | both | fixed_signal | 0.2725 | 1.773 | 80 | -21.17 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| LINKUSDT | 12h | both | embedded | 0.2563 | 0.8094 | 10 | -26.89 | `{"ema200_length": 250, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| DASHUSDT | 4h | short | atr | 0.2504 | 0.2667 | 15 | -31.29 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| BNBUSDT | 15m | long | atr | 0.2485 | 0.8429 | 97 | -8.09 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| BNBUSDT | 15m | both | embedded | 0.2352 | 0.3846 | 79 | -29.25 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| ICPUSDT | 4h | both | atr | 0.2281 | 1.3875 | 19 | -19.46 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 10, "rsi_ema_p...` |
| DASHUSDT | 15m | long | fixed_pct | 0.2121 | 0.4094 | 42 | -20.18 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| DASHUSDT | 15m | long | fixed_signal | 0.2121 | 0.4094 | 42 | -20.18 | `{"ema200_length": 250, "rejection_lookback": 5, "rsi_period": 14, "rsi_ema_pe...` |
| SHIBUSDT | 4h | both | atr | 0.1648 | 0.7626 | 12 | -11.95 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| DOGEUSDT | 15m | both | fixed_pct | 0.1554 | 0.6205 | 88 | -45.05 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| DOGEUSDT | 15m | both | fixed_signal | 0.1554 | 0.6205 | 88 | -45.05 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| ARBUSDT | 15m | short | fixed_pct | 0.1421 | 2.8956 | 30 | -15.43 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ARBUSDT | 15m | short | fixed_signal | 0.1421 | 2.8956 | 30 | -15.43 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| BTCUSDT | 4h | both | atr | 0.1339 | 0.1097 | 15 | -14.48 | `{"ema200_length": 150, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| LINKUSDT | 15m | both | atr | 0.1304 | 1.1121 | 128 | -28.32 | `{"ema200_length": 250, "rejection_lookback": 15, "rsi_period": 14, "rsi_ema_p...` |
| FLOWUSDT | 4h | both | atr | 0.0953 | -0.023 | 18 | -37.31 | `{"ema200_length": 200, "rejection_lookback": 15, "rsi_period": 10, "rsi_ema_p...` |
| ETCUSDT | 4h | both | atr | 0.0818 | 1.2611 | 10 | -15.31 | `{"ema200_length": 150, "rejection_lookback": 10, "rsi_period": 14, "rsi_ema_p...` |
| NEARUSDT | 15m | both | embedded | 0.0587 | 0.7605 | 104 | -38.99 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |
| NEARUSDT | 15m | both | atr | 0.0587 | 0.7605 | 104 | -38.99 | `{"ema200_length": 200, "rejection_lookback": 5, "rsi_period": 10, "rsi_ema_pe...` |

**Stage 2 pass rate: 124 / 489**
