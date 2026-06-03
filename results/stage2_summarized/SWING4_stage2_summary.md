# SWING4 — Stage 2 Summary (home TF: 4H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 1h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 204 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 101 / 204

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ❌ | ✅ | ✅ | ❌ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |

## Pass/Fail Table — 1H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ | ❌ | ✅ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ✅ | ✅ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| ENAUSDT | 15m | long | atr | 4.8866 | 1.588 | 75 | -53.4 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| ENAUSDT | 1h | long | fixed_pct | 4.8262 | 0.3254 | 50 | -55.74 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| ENAUSDT | 1h | long | fixed_signal | 4.8262 | 0.3254 | 50 | -55.74 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| ENAUSDT | 1h | long | embedded | 4.272 | 0.6119 | 50 | -51.87 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| ENAUSDT | 12h | both | fixed_pct | 3.7967 | 2.2032 | 15 | -25.48 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| ENAUSDT | 12h | both | fixed_signal | 3.7967 | 2.2032 | 15 | -25.48 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| ENAUSDT | 1h | both | fixed_pct | 3.1885 | 0.8039 | 82 | -52.27 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| ENAUSDT | 1h | both | fixed_signal | 3.1885 | 0.8039 | 82 | -52.27 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| ENAUSDT | 1h | long | atr | 3.1031 | 0.6822 | 57 | -46.51 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| ENAUSDT | 15m | long | embedded | 2.7634 | 1.5572 | 98 | -41.81 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| TAOUSDT | 15m | short | embedded | 1.8318 | 0.5008 | 62 | -66.81 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| SUIUSDT | 1h | long | embedded | 1.7663 | 1.493 | 55 | -52.92 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| TAOUSDT | 1h | short | atr | 1.7581 | 0.6779 | 21 | -56.43 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| INJUSDT | 12h | short | fixed_pct | 1.7203 | 0.5965 | 19 | -20.77 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| INJUSDT | 12h | short | fixed_signal | 1.7203 | 0.5965 | 19 | -20.77 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| ENAUSDT | 15m | long | fixed_pct | 1.5881 | 0.9664 | 103 | -51.41 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| ENAUSDT | 15m | long | fixed_signal | 1.5881 | 0.9664 | 103 | -51.41 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| AXSUSDT | 15m | short | embedded | 1.4393 | 0.2691 | 1 | -65.29 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| OPUSDT | 12h | short | atr | 1.4124 | 0.2199 | 1 | -77.84 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| FETUSDT | 15m | long | embedded | 1.4027 | 1.256 | 1 | -62.41 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| FETUSDT | 15m | long | atr | 1.4027 | 1.2578 | 1 | -74.06 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| AAVEUSDT | 12h | long | atr | 1.3966 | 1.8787 | 7 | -25.69 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| GMXUSDT | 1h | long | atr | 1.3596 | 0.9783 | 37 | -57.15 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| TAOUSDT | 15m | short | atr | 1.3416 | 0.9205 | 43 | -71.73 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| DYDXUSDT | 15m | short | fixed_pct | 1.2849 | 1.1415 | 289 | -51.32 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| DYDXUSDT | 15m | short | fixed_signal | 1.2849 | 1.1415 | 289 | -51.32 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| MANAUSDT | 12h | short | fixed_pct | 1.2783 | 0.9261 | 25 | -39.49 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| MANAUSDT | 12h | short | fixed_signal | 1.2783 | 0.9261 | 25 | -39.49 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| ATOMUSDT | 15m | short | fixed_pct | 1.2561 | 1.4746 | 274 | -46.33 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| ATOMUSDT | 15m | short | fixed_signal | 1.2561 | 1.4746 | 274 | -46.33 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| OPUSDT | 1h | short | atr | 1.204 | 0.7221 | 1 | -67.75 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| FETUSDT | 12h | long | embedded | 1.1848 | 0.0957 | 18 | -76.02 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| SEIUSDT | 15m | long | embedded | 1.1643 | 1.3686 | 1 | -61.07 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| UNIUSDT | 1h | long | atr | 1.1532 | 0.685 | 40 | -63.08 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| SUIUSDT | 1h | long | atr | 1.1198 | 1.5803 | 84 | -36.95 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| SEIUSDT | 12h | both | embedded | 1.1131 | 0.7206 | 17 | -77.12 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| ETCUSDT | 12h | long | fixed_pct | 1.0914 | 1.6146 | 12 | -16.47 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| ETCUSDT | 12h | long | fixed_signal | 1.0914 | 1.6146 | 12 | -16.47 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| UNIUSDT | 1h | both | fixed_pct | 1.0807 | 0.9383 | 307 | -36.69 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| UNIUSDT | 1h | both | fixed_signal | 1.0807 | 0.9383 | 307 | -36.69 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| BNBUSDT | 12h | both | embedded | 1.0631 | 1.5453 | 19 | -34.33 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| OPUSDT | 12h | short | fixed_pct | 1.0421 | 1.5487 | 24 | -30.03 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| OPUSDT | 12h | short | fixed_signal | 1.0421 | 1.5487 | 24 | -30.03 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| AAVEUSDT | 12h | long | embedded | 1.0328 | 1.5251 | 6 | -51.01 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| DASHUSDT | 15m | short | fixed_pct | 1.0231 | 0.8311 | 329 | -51.25 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| DASHUSDT | 15m | short | fixed_signal | 1.0231 | 0.8311 | 329 | -51.25 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| TAOUSDT | 1h | short | embedded | 1.0164 | 0.4483 | 16 | -50.83 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| UNIUSDT | 12h | long | fixed_pct | 1.0108 | 2.2267 | 31 | -19.56 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| UNIUSDT | 12h | long | fixed_signal | 1.0108 | 2.2267 | 31 | -19.56 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| BNBUSDT | 12h | both | atr | 0.9929 | 1.7814 | 19 | -38.42 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| GMXUSDT | 1h | long | embedded | 0.9773 | -0.0229 | 63 | -75.2 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| FETUSDT | 12h | long | atr | 0.9644 | 1.0771 | 20 | -63.09 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| SEIUSDT | 15m | long | atr | 0.915 | 1.4218 | 135 | -62.58 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| INJUSDT | 1h | short | embedded | 0.9048 | -0.5193 | 1 | -95.1 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| INJUSDT | 1h | short | atr | 0.9048 | -0.4644 | 1 | -78.98 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| INJUSDT | 12h | short | embedded | 0.9019 | 0.0492 | 1 | -68.51 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| INJUSDT | 12h | short | atr | 0.9019 | 0.0492 | 1 | -68.51 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| DASHUSDT | 15m | long | embedded | 0.8879 | 0.1123 | 1 | -42.39 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| DASHUSDT | 15m | long | atr | 0.8879 | 0.1123 | 1 | -42.39 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| OPUSDT | 15m | short | fixed_pct | 0.8869 | 0.3619 | 219 | -74.85 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| OPUSDT | 15m | short | fixed_signal | 0.8869 | 0.3619 | 219 | -74.85 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| BTCUSDT | 12h | long | embedded | 0.8394 | 1.0653 | 11 | -32.13 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| UNIUSDT | 12h | long | atr | 0.8324 | 2.2491 | 18 | -27.53 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| NEARUSDT | 1h | long | embedded | 0.8019 | 0.6489 | 178 | -60.73 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| NEARUSDT | 1h | long | atr | 0.8019 | 0.6489 | 178 | -60.73 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 10,...` |
| MANAUSDT | 15m | short | fixed_pct | 0.7913 | 1.2894 | 184 | -47.55 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| MANAUSDT | 15m | short | fixed_signal | 0.7913 | 1.2894 | 184 | -47.55 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| AXSUSDT | 12h | short | embedded | 0.7395 | 0.0616 | 1 | -58.63 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| AXSUSDT | 12h | short | atr | 0.7395 | 0.2591 | 1 | -56.8 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| DASHUSDT | 1h | short | fixed_pct | 0.7377 | 1.9118 | 157 | -29.81 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| DASHUSDT | 1h | short | fixed_signal | 0.7377 | 1.9118 | 157 | -29.81 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| SUIUSDT | 15m | long | embedded | 0.6576 | -0.0274 | 296 | -70.56 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| SUIUSDT | 15m | long | atr | 0.6576 | -0.0274 | 296 | -70.56 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| SEIUSDT | 12h | both | atr | 0.6319 | 0.8489 | 18 | -59.28 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| DASHUSDT | 12h | long | atr | 0.6099 | 0.5432 | 12 | -37.59 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| ETHUSDT | 12h | long | fixed_pct | 0.5872 | 2.1248 | 14 | -11.38 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| ETHUSDT | 12h | long | fixed_signal | 0.5872 | 2.1248 | 14 | -11.38 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| SEIUSDT | 1h | long | embedded | 0.5657 | 1.3611 | 45 | -52.38 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| AAVEUSDT | 1h | long | embedded | 0.5462 | 0.4677 | 96 | -43.56 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| SEIUSDT | 1h | long | atr | 0.509 | 1.8663 | 21 | -62.41 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| AAVEUSDT | 15m | long | atr | 0.5071 | 0.1115 | 248 | -77.1 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| DOTUSDT | 15m | short | fixed_pct | 0.4153 | 1.0521 | 270 | -52.0 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| DOTUSDT | 15m | short | fixed_signal | 0.4153 | 1.0521 | 270 | -52.0 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| UNIUSDT | 1h | long | embedded | 0.4034 | 0.6108 | 179 | -44.14 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| UNIUSDT | 15m | long | embedded | 0.369 | 0.5034 | 239 | -64.02 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 7, "rsi_period": 14,...` |
| BCHUSDT | 12h | long | fixed_pct | 0.3682 | 2.1606 | 9 | -24.7 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| BCHUSDT | 12h | long | fixed_signal | 0.3682 | 2.1606 | 9 | -24.7 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| DASHUSDT | 1h | long | atr | 0.3086 | 0.1223 | 22 | -65.45 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| UNIUSDT | 1h | both | atr | 0.2737 | 1.1498 | 219 | -57.89 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| ETHUSDT | 1h | long | atr | 0.2399 | 0.6286 | 34 | -69.0 | `{"macd_fast": 12, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 14,...` |
| ATOMUSDT | 1h | short | fixed_pct | 0.2306 | 1.5012 | 189 | -48.68 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| ATOMUSDT | 1h | short | fixed_signal | 0.2306 | 1.5012 | 189 | -48.68 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| UNIUSDT | 12h | long | embedded | 0.2277 | 0.9353 | 12 | -64.89 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 10,...` |
| ADAUSDT | 1h | long | atr | 0.1402 | 0.12 | 111 | -45.97 | `{"macd_fast": 12, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 14,...` |
| DYDXUSDT | 1h | short | fixed_pct | 0.1147 | 1.3768 | 151 | -42.54 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| DYDXUSDT | 1h | short | fixed_signal | 0.1147 | 1.3768 | 151 | -42.54 | `{"macd_fast": 10, "macd_slow": 24, "macd_signal_period": 9, "rsi_period": 10,...` |
| INJUSDT | 15m | short | fixed_pct | 0.0942 | -0.4415 | 322 | -84.76 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| INJUSDT | 15m | short | fixed_signal | 0.0942 | -0.4415 | 322 | -84.76 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| AAVEUSDT | 15m | long | embedded | 0.0569 | 0.0409 | 382 | -63.33 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 9, "rsi_period": 10,...` |
| ETHUSDT | 1h | long | fixed_pct | 0.0235 | 1.007 | 85 | -43.35 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |
| ETHUSDT | 1h | long | fixed_signal | 0.0235 | 1.007 | 85 | -43.35 | `{"macd_fast": 10, "macd_slow": 26, "macd_signal_period": 7, "rsi_period": 14,...` |

**Stage 2 pass rate: 101 / 204**
