# DC1 — Stage 2 Summary (home TF: 4H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 1h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 540 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 332 / 540

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ❌ | ✅ | ✅ | ⬜ | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ❌ | ❌ |
| AAVEUSDT | ❌ | ❌ | ❌ | ⬜ | ❌ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| INJUSDT | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |
| AVAXUSDT | ❌ | ✅ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ⬜ |
| NEARUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ❌ | ❌ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ❌ | ✅ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ |
| ETCUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ✅ | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| SHIBUSDT | ⬜ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ⬜ |
| ICPUSDT | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ⬜ | ✅ | ✅ | ❌ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ✅ |
| APTUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| ARBUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ❌ | ✅ | ⬜ | ❌ | ✅ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 1H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ❌ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ❌ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ✅ | ✅ | ✅ |
| AAVEUSDT | ✅ | ✅ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ✅ |
| INJUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ |
| AVAXUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ | ⬜ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ✅ | ✅ | ❌ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ |
| ETCUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ✅ |
| SHIBUSDT | ⬜ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ |
| ICPUSDT | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ⬜ | ✅ | ✅ | ✅ | ❌ | ❌ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ✅ |
| APTUSDT | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| ARBUSDT | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ✅ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ❌ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ✅ | ✅ | ✅ | ⬜ | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ❌ |
| AAVEUSDT | ❌ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| INJUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |
| AVAXUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ✅ | ⬜ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ❌ | ✅ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ✅ | ✅ | ⬜ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ⬜ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ |
| ETCUSDT | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| SHIBUSDT | ⬜ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ⬜ |
| ICPUSDT | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ⬜ | ✅ | ✅ | ✅ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ❌ |
| APTUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ |
| ARBUSDT | ❌ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| SUIUSDT | 1h | long | atr | 4.0649 | 1.0832 | 16 | -53.04 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SUIUSDT | 1h | long | embedded | 3.7023 | 0.7482 | 50 | -49.35 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SUIUSDT | 1h | both | atr | 3.1586 | 1.2497 | 29 | -57.05 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| RUNEUSDT | 12h | both | fixed_pct | 2.7196 | 2.1737 | 20 | -23.87 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| DASHUSDT | 15m | long | fixed_signal | 2.7002 | 0.6025 | 56 | -20.43 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| UNIUSDT | 1h | short | fixed_signal | 2.6848 | 1.057 | 30 | -17.08 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 20, "atr_period": 21...` |
| TRXUSDT | 15m | long | atr | 2.5946 | 1.1792 | 173 | -43.92 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 1h | short | fixed_pct | 2.5156 | 1.3151 | 30 | -15.47 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| FETUSDT | 1h | long | embedded | 2.4651 | 1.5526 | 24 | -41.72 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| SUIUSDT | 1h | both | embedded | 2.4165 | 0.9389 | 45 | -35.97 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| SEIUSDT | 1h | long | embedded | 2.4153 | 2.0265 | 36 | -43.0 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 1h | both | atr | 2.4102 | 2.0669 | 39 | -44.68 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 15m | long | fixed_signal | 2.266 | 1.4474 | 90 | -22.36 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 15m | long | embedded | 2.2338 | 1.19 | 91 | -24.35 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| SUIUSDT | 1h | long | fixed_pct | 2.1986 | 0.4727 | 58 | -24.63 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| SUIUSDT | 1h | long | fixed_signal | 2.1986 | 0.6361 | 58 | -23.05 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 20, "atr_period": 14...` |
| GMXUSDT | 15m | long | fixed_pct | 2.1851 | 1.5128 | 153 | -22.8 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 15m | long | fixed_pct | 2.172 | 2.0514 | 109 | -16.65 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| SEIUSDT | 15m | long | atr | 2.1324 | 1.4333 | 70 | -65.43 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SUIUSDT | 15m | long | fixed_signal | 2.1152 | 0.3795 | 115 | -35.48 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 1h | long | embedded | 2.1039 | 1.3944 | 79 | -24.01 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 15m | short | fixed_signal | 2.0994 | 2.5359 | 208 | -30.11 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 1h | short | fixed_signal | 2.0976 | 1.3022 | 41 | -21.35 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 14...` |
| GMXUSDT | 15m | both | fixed_signal | 2.07 | 2.5005 | 478 | -40.19 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 1h | both | fixed_pct | 2.0489 | 0.564 | 54 | -23.41 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| CHZUSDT | 1h | both | atr | 2.0153 | 0.8438 | 60 | -54.2 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 12h | both | embedded | 1.9937 | 0.6323 | 19 | -45.91 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 15m | long | atr | 1.9481 | 0.8458 | 54 | -17.87 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| RUNEUSDT | 15m | long | atr | 1.9475 | 2.6049 | 227 | -27.85 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| DASHUSDT | 15m | long | fixed_pct | 1.9465 | 0.3575 | 42 | -48.08 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| TRXUSDT | 15m | long | fixed_signal | 1.9375 | 1.5483 | 129 | -18.99 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| SUIUSDT | 15m | long | embedded | 1.9319 | 0.7046 | 91 | -27.23 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 1h | long | embedded | 1.9012 | 1.3143 | 56 | -35.13 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| SEIUSDT | 15m | long | fixed_pct | 1.82 | 1.1951 | 83 | -30.79 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SANDUSDT | 12h | both | fixed_pct | 1.8013 | 1.4967 | 29 | -16.21 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SANDUSDT | 12h | long | fixed_pct | 1.8 | 0.6185 | 16 | -17.57 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SANDUSDT | 12h | long | fixed_signal | 1.8 | 0.6185 | 16 | -17.57 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ADAUSDT | 12h | long | fixed_pct | 1.7794 | 1.4167 | 17 | -9.93 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| ADAUSDT | 12h | long | fixed_signal | 1.7794 | 1.4167 | 17 | -9.93 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| ALGOUSDT | 12h | long | embedded | 1.7655 | -0.4157 | 12 | -65.81 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| UNIUSDT | 12h | long | fixed_pct | 1.7591 | 0.5691 | 18 | -16.03 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| SEIUSDT | 15m | long | embedded | 1.7582 | 1.1586 | 45 | -27.55 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| BCHUSDT | 1h | long | embedded | 1.7368 | 1.3474 | 30 | -23.51 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 21...` |
| TRXUSDT | 1h | long | fixed_signal | 1.7262 | 1.1489 | 55 | -25.67 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 12h | short | fixed_pct | 1.7182 | 0.2876 | 5 | -26.51 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| GMXUSDT | 12h | short | fixed_signal | 1.7182 | 0.2876 | 5 | -26.51 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| SHIBUSDT | 1h | long | embedded | 1.6846 | 0.6558 | 54 | -38.03 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| GMXUSDT | 15m | short | fixed_pct | 1.6842 | 2.6036 | 213 | -38.16 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| BNBUSDT | 12h | both | fixed_pct | 1.6442 | 1.1298 | 15 | -27.84 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| SHIBUSDT | 15m | long | embedded | 1.6436 | 0.1136 | 84 | -56.06 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| GMXUSDT | 12h | both | fixed_signal | 1.6401 | 0.8047 | 19 | -35.95 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 14...` |
| GMXUSDT | 12h | both | fixed_pct | 1.6345 | 0.7969 | 20 | -27.68 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 15m | long | fixed_pct | 1.6284 | 0.7803 | 82 | -20.34 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SHIBUSDT | 12h | long | fixed_pct | 1.6217 | 0.3609 | 23 | -28.03 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 12h | long | fixed_signal | 1.6217 | 0.3609 | 23 | -28.03 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FETUSDT | 12h | both | atr | 1.6201 | 1.5423 | 23 | -36.45 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOGEUSDT | 1h | long | atr | 1.6178 | 1.1469 | 27 | -56.96 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AXSUSDT | 1h | short | embedded | 1.6069 | 1.7824 | 17 | -18.47 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| TRXUSDT | 15m | long | embedded | 1.6059 | 0.8951 | 197 | -18.72 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| SANDUSDT | 1h | both | fixed_pct | 1.6051 | 0.8027 | 40 | -25.9 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 1h | both | fixed_signal | 1.602 | 0.2902 | 55 | -31.78 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 21...` |
| ETHUSDT | 12h | long | embedded | 1.5918 | 0.0464 | 13 | -28.45 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| SANDUSDT | 1h | short | fixed_pct | 1.5915 | 1.6648 | 86 | -26.9 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 1h | short | fixed_pct | 1.5585 | 0.9593 | 37 | -30.61 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 12h | long | fixed_pct | 1.5561 | 0.7382 | 23 | -39.18 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOGEUSDT | 12h | long | fixed_signal | 1.5561 | 0.7382 | 23 | -39.18 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 1h | both | fixed_signal | 1.5243 | 1.8459 | 73 | -25.61 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 1h | long | atr | 1.4936 | 0.847 | 36 | -37.4 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 12h | short | fixed_signal | 1.4771 | 0.9926 | 14 | -21.79 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| INJUSDT | 12h | both | fixed_pct | 1.463 | 1.2209 | 32 | -29.71 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 15m | long | embedded | 1.4582 | 2.0454 | 153 | -25.22 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 15m | both | fixed_pct | 1.4491 | 1.8334 | 228 | -33.84 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ARBUSDT | 12h | both | atr | 1.4479 | 1.4242 | 19 | -30.5 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 12h | both | atr | 1.4449 | 1.5741 | 9 | -26.98 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| RUNEUSDT | 12h | long | atr | 1.4393 | 1.2849 | 14 | -33.09 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| MANAUSDT | 15m | long | fixed_signal | 1.4378 | 0.8564 | 63 | -39.91 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| FETUSDT | 1h | long | fixed_pct | 1.4263 | 1.0679 | 41 | -26.2 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 1h | both | embedded | 1.4228 | 0.785 | 100 | -51.07 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| LTCUSDT | 12h | long | fixed_pct | 1.4222 | 0.0963 | 13 | -35.63 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SANDUSDT | 15m | long | fixed_signal | 1.4191 | 0.2558 | 118 | -42.34 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 14...` |
| CHZUSDT | 1h | short | atr | 1.4164 | 0.7866 | 57 | -53.5 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 12h | long | embedded | 1.4132 | -0.513 | 15 | -56.63 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| TRXUSDT | 12h | both | fixed_signal | 1.4126 | 1.1162 | 24 | -18.9 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 1h | both | fixed_pct | 1.411 | 0.5407 | 55 | -13.7 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| RUNEUSDT | 15m | both | fixed_pct | 1.4072 | 2.3333 | 608 | -40.46 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FILUSDT | 15m | long | embedded | 1.4049 | 0.7428 | 50 | -29.05 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| TRXUSDT | 12h | both | fixed_pct | 1.4018 | 1.3105 | 23 | -19.65 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| TRXUSDT | 1h | both | fixed_signal | 1.3928 | 0.3601 | 56 | -14.5 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| AAVEUSDT | 1h | long | embedded | 1.3815 | 1.5505 | 47 | -33.9 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 21...` |
| NEARUSDT | 1h | long | atr | 1.3746 | 1.3268 | 23 | -48.72 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| NEARUSDT | 12h | both | embedded | 1.3739 | 1.7429 | 20 | -39.93 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 1h | both | embedded | 1.3639 | 0.908 | 100 | -33.99 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| MANAUSDT | 12h | both | fixed_pct | 1.3601 | 0.8434 | 29 | -55.64 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| MANAUSDT | 12h | both | fixed_signal | 1.3601 | 0.8434 | 29 | -55.64 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SANDUSDT | 15m | both | atr | 1.3534 | 0.3743 | 209 | -76.26 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| FLOWUSDT | 1h | short | fixed_signal | 1.3533 | 1.0904 | 64 | -35.59 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| GMXUSDT | 1h | both | fixed_pct | 1.3167 | 1.7628 | 73 | -28.62 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| TRXUSDT | 15m | both | embedded | 1.3158 | 1.1301 | 332 | -20.72 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AVAXUSDT | 1h | both | fixed_pct | 1.3122 | 1.1101 | 114 | -38.97 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 12h | long | atr | 1.312 | -0.0664 | 12 | -38.85 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 15m | both | embedded | 1.2962 | 0.3518 | 166 | -38.88 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| AVAXUSDT | 1h | long | embedded | 1.281 | 1.6229 | 37 | -15.9 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 25, "atr_period": 14...` |
| AAVEUSDT | 12h | long | fixed_pct | 1.2731 | -0.1494 | 18 | -40.45 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 12h | long | fixed_signal | 1.2731 | -0.1494 | 18 | -40.45 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| UNIUSDT | 12h | long | fixed_signal | 1.2627 | 0.6243 | 18 | -16.03 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 14...` |
| CHZUSDT | 1h | short | embedded | 1.2569 | 0.9129 | 38 | -34.15 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| SUIUSDT | 15m | long | atr | 1.2547 | 0.9907 | 161 | -40.86 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| DOTUSDT | 1h | short | fixed_pct | 1.2476 | 1.4374 | 34 | -15.87 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SANDUSDT | 12h | both | atr | 1.2243 | 2.298 | 21 | -28.45 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 1h | long | atr | 1.2217 | 1.4547 | 29 | -35.71 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| TRXUSDT | 1h | long | fixed_pct | 1.2109 | 1.5776 | 51 | -11.26 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| TRXUSDT | 12h | long | atr | 1.2055 | 0.5496 | 19 | -25.95 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| ETHUSDT | 15m | short | fixed_pct | 1.2053 | 1.2194 | 80 | -30.1 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| FETUSDT | 1h | long | fixed_signal | 1.1762 | 1.0679 | 41 | -26.2 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| MANAUSDT | 15m | long | fixed_pct | 1.1677 | 0.7089 | 72 | -58.43 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| FLOWUSDT | 1h | both | fixed_pct | 1.1675 | 0.7755 | 140 | -35.52 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 15m | long | atr | 1.1489 | 0.6744 | 52 | -40.02 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 12h | long | atr | 1.1339 | 0.3276 | 17 | -35.79 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| INJUSDT | 1h | both | fixed_pct | 1.1213 | 0.6629 | 200 | -57.45 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| INJUSDT | 1h | short | fixed_pct | 1.1081 | 0.8746 | 109 | -47.04 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| BNBUSDT | 12h | long | embedded | 1.1069 | 1.2546 | 15 | -21.48 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| AXSUSDT | 1h | short | fixed_signal | 1.1022 | 1.7499 | 30 | -11.01 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| AXSUSDT | 1h | short | fixed_pct | 1.0992 | 1.3912 | 27 | -14.55 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 15m | both | fixed_signal | 1.0961 | 0.4584 | 119 | -40.81 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| TRXUSDT | 1h | short | embedded | 1.0961 | 0.6293 | 44 | -20.63 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| DASHUSDT | 12h | long | fixed_pct | 1.0939 | 0.6426 | 14 | -21.35 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DASHUSDT | 12h | long | fixed_signal | 1.0939 | 0.6426 | 14 | -21.35 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SEIUSDT | 15m | long | fixed_signal | 1.0923 | 1.6552 | 128 | -24.94 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 20, "atr_period": 14...` |
| SEIUSDT | 1h | long | fixed_signal | 1.0848 | 0.5634 | 67 | -28.59 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| CHZUSDT | 1h | both | fixed_pct | 1.0837 | 0.6252 | 84 | -45.92 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| AVAXUSDT | 1h | both | fixed_signal | 1.0782 | 1.2723 | 119 | -37.99 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 14...` |
| GMXUSDT | 1h | short | atr | 1.0765 | 1.814 | 37 | -28.59 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| BNBUSDT | 12h | both | atr | 1.0635 | 1.1003 | 18 | -25.38 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 1h | short | fixed_signal | 1.0628 | 1.0925 | 34 | -17.33 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 14...` |
| DOTUSDT | 1h | long | atr | 1.0471 | 0.7315 | 17 | -45.77 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| AAVEUSDT | 15m | long | fixed_pct | 1.0352 | 1.2283 | 128 | -32.9 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| ETHUSDT | 12h | long | fixed_pct | 1.0266 | 1.5673 | 15 | -12.77 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 12h | long | fixed_signal | 1.0266 | 1.5673 | 15 | -12.77 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 12h | both | fixed_pct | 1.019 | 1.6841 | 25 | -16.5 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 12h | both | fixed_signal | 1.019 | 1.6841 | 25 | -16.5 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| AVAXUSDT | 1h | both | embedded | 1.0136 | 1.7978 | 94 | -43.23 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 20, "atr_period": 14...` |
| TRXUSDT | 12h | both | embedded | 1.0055 | 0.498 | 20 | -33.89 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| DOGEUSDT | 12h | both | fixed_pct | 1.0019 | 0.81 | 26 | -20.1 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 12h | both | fixed_signal | 1.0019 | 0.81 | 26 | -20.1 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| SHIBUSDT | 1h | both | atr | 1.0004 | 0.7556 | 58 | -62.07 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| FLOWUSDT | 12h | both | fixed_pct | 0.9913 | 2.1484 | 31 | -21.81 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FLOWUSDT | 12h | both | fixed_signal | 0.9913 | 2.1484 | 31 | -21.81 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FLOWUSDT | 15m | both | embedded | 0.9711 | 0.7768 | 101 | -44.74 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| TRXUSDT | 12h | long | fixed_pct | 0.9652 | 0.7724 | 21 | -12.27 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| GMXUSDT | 15m | long | atr | 0.9563 | 2.0392 | 149 | -24.92 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FETUSDT | 12h | long | atr | 0.9557 | 1.2194 | 17 | -31.13 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 12h | both | fixed_pct | 0.935 | 0.9195 | 30 | -37.39 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 12h | both | fixed_signal | 0.935 | 0.9195 | 30 | -37.39 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 1h | both | atr | 0.9338 | 0.8895 | 44 | -48.64 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 1h | short | atr | 0.931 | 0.8167 | 24 | -25.99 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| BTCUSDT | 1h | long | embedded | 0.9169 | 1.1531 | 97 | -21.18 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 20, "atr_period": 10...` |
| FLOWUSDT | 1h | both | fixed_signal | 0.9048 | 1.0242 | 98 | -43.32 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| AVAXUSDT | 15m | long | embedded | 0.8954 | 0.8151 | 214 | -41.59 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 12h | long | atr | 0.8827 | 0.6342 | 17 | -23.33 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 1h | short | fixed_signal | 0.8801 | 1.348 | 45 | -20.44 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 21...` |
| SUIUSDT | 15m | both | fixed_pct | 0.88 | 0.6289 | 102 | -42.7 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| SHIBUSDT | 1h | both | fixed_signal | 0.8716 | 0.4723 | 133 | -45.03 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| BCHUSDT | 15m | long | embedded | 0.8699 | 1.9228 | 86 | -26.57 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| MANAUSDT | 15m | long | embedded | 0.8559 | 0.7167 | 56 | -42.61 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| BTCUSDT | 1h | both | embedded | 0.8523 | 2.1241 | 41 | -27.2 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 12h | both | atr | 0.8392 | 1.1405 | 18 | -44.83 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DYDXUSDT | 1h | short | embedded | 0.8175 | 1.0152 | 65 | -33.48 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 20, "atr_period": 14...` |
| NEARUSDT | 12h | long | embedded | 0.8147 | -0.0338 | 13 | -49.65 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| UNIUSDT | 12h | both | embedded | 0.8126 | 0.7675 | 15 | -42.06 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| BTCUSDT | 12h | long | embedded | 0.8065 | 0.0752 | 15 | -37.09 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| CHZUSDT | 12h | long | atr | 0.8057 | 1.0641 | 18 | -35.72 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 15m | long | atr | 0.804 | 0.9829 | 89 | -39.37 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| BNBUSDT | 15m | both | fixed_pct | 0.7965 | 0.6882 | 190 | -45.24 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| BTCUSDT | 15m | long | embedded | 0.7939 | 1.5146 | 91 | -14.89 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 20, "atr_period": 21...` |
| UNIUSDT | 12h | short | fixed_pct | 0.7887 | 0.9426 | 12 | -23.41 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AVAXUSDT | 15m | both | atr | 0.7784 | 1.3274 | 314 | -53.32 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 15m | both | atr | 0.7749 | 1.2619 | 97 | -29.6 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SANDUSDT | 15m | short | fixed_pct | 0.7652 | 1.0481 | 156 | -54.33 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| ADAUSDT | 15m | long | embedded | 0.7597 | 0.8068 | 281 | -36.76 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 20, "atr_period": 14...` |
| ETHUSDT | 1h | long | atr | 0.7547 | 1.5248 | 94 | -24.21 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| BCHUSDT | 1h | both | fixed_pct | 0.7473 | 1.1336 | 34 | -18.24 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SHIBUSDT | 1h | both | fixed_pct | 0.7434 | 0.4853 | 109 | -43.98 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 15m | long | atr | 0.7401 | 0.957 | 47 | -34.98 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| FILUSDT | 1h | short | atr | 0.7307 | 1.7673 | 43 | -39.87 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 1h | long | fixed_signal | 0.7267 | 1.3204 | 51 | -33.74 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 14...` |
| ALGOUSDT | 15m | long | atr | 0.7236 | 0.8009 | 82 | -26.06 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 1h | long | atr | 0.7231 | 0.6041 | 30 | -38.8 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| ARBUSDT | 1h | short | embedded | 0.7214 | 0.5917 | 37 | -35.18 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 10...` |
| TRXUSDT | 15m | both | fixed_signal | 0.7213 | 1.7397 | 279 | -26.0 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ADAUSDT | 15m | long | atr | 0.7207 | 0.7791 | 247 | -45.93 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| DYDXUSDT | 15m | long | atr | 0.7184 | 0.7486 | 34 | -47.17 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| BNBUSDT | 12h | both | embedded | 0.7163 | 1.3255 | 22 | -25.95 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| SANDUSDT | 12h | short | fixed_pct | 0.7023 | 2.0103 | 17 | -16.85 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| ETCUSDT | 12h | long | atr | 0.6984 | 0.5948 | 17 | -56.41 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOGEUSDT | 1h | long | fixed_signal | 0.6949 | 0.8816 | 102 | -35.83 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| SEIUSDT | 1h | long | fixed_pct | 0.6949 | 0.664 | 63 | -30.99 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| APTUSDT | 15m | long | embedded | 0.6941 | 1.0247 | 44 | -27.33 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| AVAXUSDT | 12h | short | fixed_pct | 0.688 | 1.9358 | 16 | -15.22 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AVAXUSDT | 12h | short | fixed_signal | 0.688 | 1.9358 | 16 | -15.22 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FLOWUSDT | 12h | both | embedded | 0.6825 | 1.4112 | 22 | -39.82 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| ETHUSDT | 15m | short | fixed_signal | 0.6816 | 1.5493 | 52 | -26.53 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 15m | both | embedded | 0.6792 | 0.4173 | 99 | -40.47 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| TRXUSDT | 1h | long | atr | 0.6789 | 0.9775 | 43 | -31.85 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| TRXUSDT | 12h | long | embedded | 0.6728 | 0.6994 | 18 | -22.73 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| INJUSDT | 1h | both | atr | 0.6701 | 0.8349 | 54 | -86.58 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 15m | both | atr | 0.6539 | 0.3538 | 102 | -48.66 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| FETUSDT | 12h | long | fixed_pct | 0.6537 | -0.0128 | 20 | -27.75 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FETUSDT | 12h | long | fixed_signal | 0.6537 | -0.0128 | 20 | -27.75 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FETUSDT | 15m | long | atr | 0.6494 | 0.826 | 169 | -57.51 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 15m | long | fixed_pct | 0.6443 | 1.728 | 72 | -26.67 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| TRXUSDT | 12h | long | fixed_signal | 0.6426 | 0.9456 | 21 | -11.73 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| NEARUSDT | 15m | long | atr | 0.6381 | 1.1946 | 51 | -24.45 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SOLUSDT | 12h | long | fixed_pct | 0.6361 | 1.3929 | 18 | -23.53 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SOLUSDT | 12h | long | fixed_signal | 0.6361 | 1.3929 | 18 | -23.53 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SOLUSDT | 1h | both | atr | 0.6349 | 1.3546 | 102 | -56.08 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| CHZUSDT | 1h | both | fixed_signal | 0.6123 | 0.5718 | 85 | -46.09 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| NEARUSDT | 12h | long | atr | 0.6065 | 0.3839 | 14 | -31.95 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| SANDUSDT | 12h | both | fixed_signal | 0.5958 | 1.6433 | 27 | -14.79 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| ADAUSDT | 1h | long | fixed_signal | 0.594 | 1.6639 | 61 | -25.36 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 10...` |
| FETUSDT | 15m | long | embedded | 0.5864 | 0.3116 | 172 | -74.38 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| FLOWUSDT | 12h | short | atr | 0.5813 | 1.4998 | 15 | -39.07 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 1h | long | embedded | 0.5775 | 0.3533 | 66 | -42.95 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 25, "atr_period": 14...` |
| CHZUSDT | 1h | both | embedded | 0.5773 | 0.6737 | 65 | -44.23 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 20, "atr_period": 14...` |
| APTUSDT | 1h | long | atr | 0.5765 | 0.9461 | 37 | -60.69 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| AVAXUSDT | 1h | both | atr | 0.5713 | 1.8405 | 72 | -40.73 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| APTUSDT | 1h | long | embedded | 0.5651 | 0.9678 | 31 | -30.13 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 20, "atr_period": 14...` |
| LTCUSDT | 12h | long | atr | 0.5615 | -0.0355 | 12 | -46.43 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| NEARUSDT | 15m | long | embedded | 0.5489 | 1.7663 | 112 | -45.22 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 14...` |
| APTUSDT | 1h | both | embedded | 0.5489 | 1.0767 | 57 | -49.17 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SANDUSDT | 1h | long | fixed_signal | 0.5473 | 0.3345 | 114 | -51.06 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ARBUSDT | 1h | both | embedded | 0.5456 | 0.6895 | 82 | -35.66 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ICPUSDT | 1h | long | fixed_pct | 0.5432 | 0.9747 | 23 | -15.2 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ICPUSDT | 1h | long | fixed_signal | 0.5432 | 0.9747 | 23 | -15.2 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ICPUSDT | 12h | both | atr | 0.5349 | 1.4065 | 17 | -47.16 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 1h | both | embedded | 0.5303 | 1.5173 | 77 | -47.58 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 21...` |
| ADAUSDT | 12h | both | embedded | 0.53 | 1.1935 | 16 | -39.93 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| ETHUSDT | 12h | short | fixed_pct | 0.5284 | 1.0464 | 17 | -17.81 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| NEARUSDT | 1h | both | embedded | 0.5269 | 1.2285 | 70 | -33.57 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 21...` |
| MANAUSDT | 12h | long | fixed_signal | 0.5219 | 0.8281 | 18 | -32.51 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| LTCUSDT | 15m | long | atr | 0.5207 | 0.812 | 80 | -40.66 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| LINKUSDT | 15m | long | embedded | 0.5196 | 0.8639 | 63 | -18.55 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| BCHUSDT | 15m | long | fixed_pct | 0.4994 | 2.127 | 80 | -12.61 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SANDUSDT | 1h | both | fixed_signal | 0.4992 | 0.875 | 98 | -42.21 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 15m | long | embedded | 0.493 | 0.8523 | 65 | -26.24 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| SOLUSDT | 12h | both | atr | 0.4881 | 1.7969 | 15 | -36.52 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 12h | long | atr | 0.4863 | -0.3457 | 13 | -53.15 | `{"donchian_length": 15, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| RUNEUSDT | 1h | both | fixed_pct | 0.4821 | 2.612 | 153 | -30.33 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AAVEUSDT | 12h | long | embedded | 0.4813 | -0.0207 | 12 | -64.77 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| SANDUSDT | 15m | long | fixed_pct | 0.4687 | -0.0461 | 112 | -47.24 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| SANDUSDT | 1h | long | fixed_pct | 0.4683 | 0.0005 | 29 | -30.27 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 12h | short | fixed_signal | 0.4673 | 0.9977 | 12 | -23.41 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| SHIBUSDT | 12h | both | atr | 0.4662 | 1.6548 | 24 | -36.89 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AVAXUSDT | 1h | long | atr | 0.4556 | 1.2223 | 41 | -46.09 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| SANDUSDT | 1h | short | embedded | 0.447 | 1.6898 | 50 | -30.12 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 1h | long | atr | 0.4431 | 2.0094 | 23 | -34.81 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| BCHUSDT | 1h | both | fixed_signal | 0.4223 | 1.035 | 34 | -18.24 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| ADAUSDT | 1h | long | embedded | 0.419 | 1.781 | 71 | -22.23 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 1h | both | embedded | 0.3966 | 0.5948 | 48 | -38.26 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 25, "atr_period": 21...` |
| BNBUSDT | 1h | both | atr | 0.3865 | 0.8583 | 68 | -39.77 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 15m | short | fixed_pct | 0.3865 | 1.0331 | 187 | -35.66 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| DOGEUSDT | 12h | long | atr | 0.3812 | 0.3969 | 22 | -40.21 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| MANAUSDT | 12h | long | fixed_pct | 0.3774 | 0.8281 | 18 | -32.51 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 1h | short | fixed_pct | 0.3704 | 1.7341 | 28 | -28.45 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| GMXUSDT | 1h | short | fixed_signal | 0.3704 | 1.7341 | 28 | -28.45 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| SHIBUSDT | 15m | long | fixed_signal | 0.3678 | 0.3468 | 89 | -48.31 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| FLOWUSDT | 15m | short | fixed_signal | 0.3678 | 1.1702 | 57 | -27.52 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| MANAUSDT | 1h | long | embedded | 0.363 | 0.5119 | 53 | -33.77 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 20, "atr_period": 10...` |
| NEARUSDT | 1h | both | atr | 0.3623 | 1.4162 | 59 | -52.61 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| CHZUSDT | 12h | long | embedded | 0.3614 | -0.2316 | 16 | -58.52 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| CHZUSDT | 15m | both | fixed_signal | 0.3604 | -0.627 | 326 | -90.86 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| FLOWUSDT | 12h | short | fixed_signal | 0.3437 | 2.0963 | 14 | -25.32 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ICPUSDT | 1h | both | embedded | 0.3389 | 1.1231 | 29 | -30.22 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 25, "atr_period": 21...` |
| BCHUSDT | 12h | long | fixed_pct | 0.335 | 1.3756 | 20 | -10.59 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| BCHUSDT | 12h | long | fixed_signal | 0.335 | 1.3756 | 20 | -10.59 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 12h | long | atr | 0.3324 | -0.3274 | 13 | -36.74 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 15m | long | fixed_signal | 0.3301 | 1.0029 | 78 | -32.55 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 20, "atr_period": 21...` |
| AXSUSDT | 15m | short | fixed_signal | 0.3266 | 1.2129 | 207 | -45.4 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| RUNEUSDT | 12h | both | atr | 0.3172 | 1.9279 | 14 | -38.56 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 12h | short | fixed_pct | 0.3162 | 1.6075 | 19 | -14.84 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 12h | short | fixed_signal | 0.3162 | 1.6075 | 19 | -14.84 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 12h | long | fixed_signal | 0.3156 | 0.9251 | 22 | -14.71 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 12h | both | embedded | 0.3123 | 2.0915 | 18 | -30.99 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| ICPUSDT | 12h | both | embedded | 0.2989 | 1.7626 | 18 | -34.12 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| AXSUSDT | 12h | short | fixed_pct | 0.2862 | 1.3845 | 18 | -17.16 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AXSUSDT | 12h | short | fixed_signal | 0.2862 | 1.333 | 18 | -17.16 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| AVAXUSDT | 15m | short | fixed_pct | 0.2848 | 1.5085 | 190 | -50.58 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| FETUSDT | 15m | both | atr | 0.2842 | -0.1508 | 216 | -91.25 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 12h | both | atr | 0.2802 | 1.8805 | 17 | -34.09 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| DASHUSDT | 1h | long | fixed_signal | 0.2789 | 1.137 | 78 | -25.38 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| BCHUSDT | 15m | both | atr | 0.2702 | 1.5269 | 142 | -35.63 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| FLOWUSDT | 1h | both | embedded | 0.2663 | 1.3117 | 122 | -36.55 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| NEARUSDT | 12h | both | atr | 0.2619 | 1.8013 | 26 | -34.89 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| DOTUSDT | 15m | short | fixed_signal | 0.2567 | 0.814 | 70 | -25.05 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AAVEUSDT | 1h | long | fixed_pct | 0.2549 | 1.1674 | 59 | -19.58 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| CHZUSDT | 15m | both | atr | 0.2459 | -0.4816 | 213 | -89.81 | `{"donchian_length": 55, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| ETHUSDT | 1h | long | fixed_signal | 0.2301 | 0.9932 | 113 | -20.73 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 25, "atr_period": 10...` |
| DASHUSDT | 1h | long | fixed_pct | 0.2294 | 0.8567 | 78 | -33.72 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| BCHUSDT | 12h | both | fixed_pct | 0.2284 | 1.222 | 27 | -27.59 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| BCHUSDT | 12h | both | fixed_signal | 0.2284 | 1.222 | 27 | -27.59 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| ADAUSDT | 1h | long | fixed_pct | 0.2225 | 1.3708 | 60 | -25.59 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| BCHUSDT | 1h | long | fixed_signal | 0.2225 | 1.0641 | 66 | -16.83 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 25, "atr_period": 10...` |
| BNBUSDT | 1h | both | embedded | 0.2139 | 0.6095 | 118 | -35.14 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 20, "atr_period": 10...` |
| SHIBUSDT | 1h | long | atr | 0.2108 | 0.6752 | 41 | -47.61 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| SHIBUSDT | 15m | long | fixed_pct | 0.1939 | 0.5192 | 121 | -50.89 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| DOGEUSDT | 15m | long | fixed_signal | 0.185 | 0.8624 | 137 | -26.28 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| FLOWUSDT | 15m | both | fixed_signal | 0.177 | 0.3309 | 101 | -31.8 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| RUNEUSDT | 1h | both | atr | 0.1684 | 2.4182 | 169 | -27.21 | `{"donchian_length": 55, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| FETUSDT | 1h | long | atr | 0.1684 | 1.8045 | 25 | -33.05 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AVAXUSDT | 12h | long | atr | 0.1626 | 0.9999 | 15 | -40.74 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ALGOUSDT | 1h | long | fixed_signal | 0.1615 | 0.9866 | 71 | -27.16 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |
| INJUSDT | 1h | short | atr | 0.1546 | 0.6042 | 121 | -47.34 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| GMXUSDT | 15m | both | fixed_pct | 0.1515 | 2.4947 | 208 | -31.26 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 15m | both | fixed_pct | 0.1464 | 0.435 | 162 | -45.6 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| ARBUSDT | 1h | both | atr | 0.1448 | 0.8903 | 41 | -41.28 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| DOGEUSDT | 15m | both | fixed_signal | 0.142 | 0.1791 | 222 | -47.26 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 14...` |
| INJUSDT | 12h | both | atr | 0.1261 | 2.1363 | 13 | -47.31 | `{"donchian_length": 20, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| RUNEUSDT | 15m | both | atr | 0.1233 | 2.7426 | 581 | -27.56 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 14...` |
| AVAXUSDT | 15m | both | fixed_pct | 0.1085 | 1.1385 | 115 | -42.2 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| GMXUSDT | 15m | short | atr | 0.0787 | 1.7435 | 104 | -44.83 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 21...` |
| ADAUSDT | 15m | long | fixed_pct | 0.0783 | 0.9777 | 82 | -28.92 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| RUNEUSDT | 1h | long | atr | 0.0763 | 2.5302 | 151 | -33.1 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 10...` |
| ICPUSDT | 15m | both | atr | 0.0756 | 0.0165 | 128 | -79.24 | `{"donchian_length": 25, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| DOGEUSDT | 1h | long | fixed_pct | 0.0734 | 0.7851 | 100 | -45.03 | `{"donchian_length": 25, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| UNIUSDT | 15m | short | fixed_pct | 0.073 | 0.5362 | 51 | -33.55 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AAVEUSDT | 1h | both | fixed_pct | 0.0715 | 1.508 | 37 | -22.31 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| CHZUSDT | 15m | both | embedded | 0.063 | -0.8744 | 141 | -84.05 | `{"donchian_length": 15, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| CHZUSDT | 1h | long | embedded | 0.0612 | 0.6142 | 63 | -52.39 | `{"donchian_length": 20, "adx_threshold": 25, "adx_exit": 15, "atr_period": 10...` |
| CHZUSDT | 15m | long | atr | 0.0605 | 0.6743 | 144 | -58.47 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 14...` |
| UNIUSDT | 15m | both | fixed_pct | 0.0274 | 0.4716 | 131 | -47.07 | `{"donchian_length": 55, "adx_threshold": 30, "adx_exit": 15, "atr_period": 21...` |
| AVAXUSDT | 15m | short | fixed_signal | 0.0254 | 1.0802 | 201 | -55.98 | `{"donchian_length": 15, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| UNIUSDT | 1h | long | embedded | 0.0244 | 0.5872 | 51 | -35.08 | `{"donchian_length": 25, "adx_threshold": 20, "adx_exit": 15, "atr_period": 21...` |
| ALGOUSDT | 1h | both | atr | 0.0065 | 1.1425 | 88 | -59.7 | `{"donchian_length": 20, "adx_threshold": 30, "adx_exit": 15, "atr_period": 10...` |

**Stage 2 pass rate: 332 / 540**
