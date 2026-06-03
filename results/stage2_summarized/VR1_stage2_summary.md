# VR1 — Stage 2 Summary (home TF: 1H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 4h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 189 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 27 / 189

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ❌ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ✅ | ❌ | ⬜ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 4H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| DYDXUSDT | 15m | long | fixed_signal | 1.9389 | -0.4347 | 40 | -26.51 | `{"band_mult": 2.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| SUIUSDT | 15m | long | embedded | 1.4269 | 0.8921 | 19 | -8.4 | `{"band_mult": 2.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| INJUSDT | 15m | long | fixed_signal | 1.3457 | 0.7126 | 41 | -26.06 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| FILUSDT | 15m | long | atr | 1.1077 | 0.6654 | 31 | -30.05 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| INJUSDT | 15m | both | embedded | 0.9918 | 0.7803 | 77 | -24.04 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| NEARUSDT | 15m | both | atr | 0.9883 | 1.3479 | 32 | -31.41 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| TAOUSDT | 15m | both | fixed_pct | 0.9749 | 2.2397 | 9 | -17.87 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| BCHUSDT | 15m | long | atr | 0.9746 | 0.619 | 49 | -54.44 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| SEIUSDT | 15m | both | atr | 0.9214 | 1.2799 | 37 | -34.45 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| DYDXUSDT | 15m | short | fixed_pct | 0.8404 | 0.5546 | 19 | -13.01 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| FETUSDT | 4h | long | embedded | 0.7999 | 1.1442 | 5 | -9.06 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| LTCUSDT | 15m | long | embedded | 0.7791 | -0.244 | 33 | -17.2 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| SEIUSDT | 15m | short | atr | 0.7752 | 1.3543 | 7 | -33.63 | `{"band_mult": 2.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| INJUSDT | 4h | long | fixed_signal | 0.7629 | 0.7215 | 6 | -15.45 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| SUIUSDT | 15m | long | atr | 0.7096 | 1.8215 | 6 | -10.65 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| BCHUSDT | 4h | both | atr | 0.6372 | 1.5089 | 14 | -22.06 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| GMXUSDT | 15m | long | fixed_signal | 0.5918 | -0.6845 | 25 | -19.14 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.2, "rsi_oversold_floor": ...` |
| BTCUSDT | 15m | long | atr | 0.3983 | 0.7651 | 33 | -41.03 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| FETUSDT | 15m | long | atr | 0.347 | 1.6574 | 15 | -23.15 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| FETUSDT | 4h | long | atr | 0.3389 | 0.2144 | 5 | -35.33 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.5, "rsi_oversold_floor": ...` |
| OPUSDT | 15m | short | fixed_pct | 0.3336 | 1.1654 | 23 | -24.52 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| FLOWUSDT | 15m | long | embedded | 0.3019 | 0.4823 | 23 | -9.14 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.2, "rsi_oversold_floor": ...` |
| DYDXUSDT | 15m | both | fixed_pct | 0.2242 | 1.9274 | 15 | -11.64 | `{"band_mult": 2.0, "volume_exhaustion_threshold": 0.2, "rsi_oversold_floor": ...` |
| DOGEUSDT | 15m | long | atr | 0.0663 | 1.1655 | 28 | -32.59 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| DOGEUSDT | 15m | long | fixed_pct | 0.0478 | 1.0362 | 27 | -20.6 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| ARBUSDT | 15m | long | fixed_signal | 0.0391 | 0.8366 | 18 | -7.7 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |
| ARBUSDT | 15m | long | atr | 0.0034 | 2.3107 | 23 | -6.38 | `{"band_mult": 1.5, "volume_exhaustion_threshold": 0.3, "rsi_oversold_floor": ...` |

**Stage 2 pass rate: 27 / 189**
