# VP1 — Stage 2 Summary (home TF: 1H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 4h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 729 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 397 / 729

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ❌ | ⬜ | ⬜ |
| ETHUSDT | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| SOLUSDT | ⬜ | ✅ | ⬜ | ✅ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ❌ | ❌ | ⬜ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ⬜ |
| ADAUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ✅ | ❌ | ⬜ | ❌ | ⬜ | ⬜ |
| DOGEUSDT | ❌ | ✅ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ❌ | ❌ | ✅ | ❌ | ⬜ |
| DOTUSDT | ❌ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ❌ |
| LINKUSDT | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ✅ |
| FILUSDT | ❌ | ✅ | ❌ | ✅ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ | ❌ | ⬜ |
| INJUSDT | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| AVAXUSDT | ⬜ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⬜ | ⬜ |
| NEARUSDT | ❌ | ❌ | ❌ | ✅ | ⬜ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ❌ |
| TRXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ⬜ |
| ALGOUSDT | ❌ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ❌ | ✅ |
| SANDUSDT | ✅ | ❌ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ❌ |
| MANAUSDT | ❌ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ | ❌ |
| RUNEUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ❌ |
| CHZUSDT | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ | ✅ |
| SHIBUSDT | ✅ | ⬜ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ❌ | ⬜ |
| ICPUSDT | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| FLOWUSDT | ⬜ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ⬜ |
| FETUSDT | ❌ | ❌ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| GMXUSDT | ✅ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ❌ | ❌ |
| SUIUSDT | ❌ | ✅ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ❌ | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ✅ | ❌ | ❌ | ❌ | ✅ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ |

## Pass/Fail Table — 4H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ |
| ETHUSDT | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ✅ | ✅ |
| SOLUSDT | ⬜ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ❌ | ⬜ | ❌ | ✅ | ⬜ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ⬜ |
| ADAUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ |
| DOGEUSDT | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ |
| DOTUSDT | ❌ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ✅ |
| LINKUSDT | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| FILUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ |
| INJUSDT | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ✅ | ❌ |
| AVAXUSDT | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ |
| NEARUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| TRXUSDT | ❌ | ❌ | ✅ | ❌ | ⬜ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ⬜ |
| ALGOUSDT | ✅ | ❌ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ❌ | ❌ |
| SANDUSDT | ✅ | ❌ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ✅ |
| MANAUSDT | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ |
| RUNEUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| CHZUSDT | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SHIBUSDT | ✅ | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ |
| ICPUSDT | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| FLOWUSDT | ⬜ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ⬜ |
| FETUSDT | ✅ | ✅ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ❌ | ✅ |
| GMXUSDT | ❌ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ✅ | ✅ | ❌ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ |
| SUIUSDT | ✅ | ✅ | ⬜ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ✅ | ✅ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ✅ | ❌ | ❌ | ✅ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ❌ | ⬜ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ⬜ |
| ETHUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| SOLUSDT | ⬜ | ✅ | ⬜ | ❌ | ❌ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ✅ | ⬜ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⬜ |
| ADAUSDT | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ | ⬜ | ✅ | ⬜ | ⬜ |
| DOGEUSDT | ✅ | ✅ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ❌ | ❌ | ✅ | ✅ | ⬜ |
| DOTUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ❌ |
| LINKUSDT | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ✅ | ❌ | ⬜ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| FILUSDT | ✅ | ❌ | ❌ | ✅ | ⬜ | ✅ | ⬜ | ❌ | ✅ | ❌ | ❌ | ⬜ |
| INJUSDT | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ✅ | ❌ |
| AVAXUSDT | ⬜ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ |
| NEARUSDT | ✅ | ✅ | ❌ | ✅ | ⬜ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| TRXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ⬜ | ✅ | ❌ | ⬜ | ✅ | ⬜ |
| ALGOUSDT | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ |
| SANDUSDT | ✅ | ✅ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ |
| MANAUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ✅ | ❌ |
| RUNEUSDT | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ❌ |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| CHZUSDT | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ✅ |
| SHIBUSDT | ✅ | ⬜ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ⬜ |
| ICPUSDT | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| FLOWUSDT | ⬜ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ⬜ |
| FETUSDT | ✅ | ✅ | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ✅ | ❌ |
| GMXUSDT | ❌ | ❌ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ✅ | ❌ |
| SUIUSDT | ✅ | ✅ | ⬜ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ❌ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| TRXUSDT | 15m | both | fixed_pct | 4.2051 | 0.2175 | 161 | -41.53 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 15m | both | fixed_signal | 3.4256 | 0.219 | 249 | -48.48 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 4h | both | atr | 3.1519 | 2.2411 | 20 | -41.67 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 15m | long | atr | 2.8464 | 0.284 | 90 | -38.19 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 15m | both | embedded | 2.7781 | -0.3692 | 318 | -59.14 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 15m | long | fixed_pct | 2.7596 | 1.0347 | 52 | -41.0 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| DOGEUSDT | 12h | long | fixed_pct | 2.6548 | 0.6774 | 18 | -17.33 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 4h | both | fixed_pct | 2.5887 | 1.9821 | 45 | -34.46 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ALGOUSDT | 12h | both | atr | 2.574 | 1.6856 | 15 | -51.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 4h | both | fixed_pct | 2.5607 | 1.153 | 74 | -30.83 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SUIUSDT | 4h | both | embedded | 2.3907 | 1.1405 | 16 | -31.16 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| DOGEUSDT | 4h | both | atr | 2.3821 | 1.0713 | 40 | -47.93 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 12h | both | fixed_pct | 2.3634 | 1.021 | 18 | -18.51 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SEIUSDT | 12h | both | fixed_pct | 2.3014 | 1.8205 | 16 | -16.82 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| CHZUSDT | 12h | short | fixed_pct | 2.2978 | 0.9595 | 5 | -20.65 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 12h | short | fixed_signal | 2.2978 | 1.008 | 5 | -20.65 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 4h | long | fixed_signal | 2.2682 | 2.0532 | 18 | -7.33 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 4h | short | atr | 2.2403 | 1.9835 | 34 | -27.61 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SANDUSDT | 12h | both | fixed_signal | 2.1344 | 0.8394 | 12 | -28.04 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| SANDUSDT | 12h | short | fixed_pct | 2.1312 | 1.1671 | 8 | -36.55 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| SEIUSDT | 4h | short | fixed_signal | 2.1225 | 2.2423 | 11 | -16.42 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SANDUSDT | 12h | both | fixed_pct | 2.1005 | 0.9214 | 12 | -28.04 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| NEARUSDT | 4h | both | fixed_signal | 2.0897 | 2.3 | 47 | -32.78 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 12h | short | fixed_pct | 2.0887 | 0.8954 | 20 | -24.48 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 12h | both | embedded | 2.0725 | 1.2348 | 25 | -44.67 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 4h | long | fixed_pct | 2.0715 | 2.0025 | 24 | -14.34 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| FETUSDT | 12h | both | fixed_pct | 2.0622 | 1.4025 | 19 | -25.25 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 4h | short | fixed_pct | 2.0541 | 2.5703 | 40 | -30.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 12h | short | fixed_pct | 2.0467 | 1.5674 | 13 | -23.35 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| ARBUSDT | 12h | short | fixed_signal | 2.0208 | 1.7723 | 13 | -16.89 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 4h | long | embedded | 2.0031 | 0.6534 | 24 | -39.14 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 15m | both | atr | 1.9999 | -0.3403 | 186 | -67.84 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| OPUSDT | 4h | short | embedded | 1.983 | 0.4332 | 26 | -64.53 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ARBUSDT | 4h | short | fixed_signal | 1.9813 | 1.7296 | 17 | -20.29 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SUIUSDT | 4h | long | atr | 1.9227 | -0.4428 | 23 | -30.95 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| MANAUSDT | 12h | both | atr | 1.9153 | 1.0107 | 13 | -36.64 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ETHUSDT | 12h | long | fixed_pct | 1.9106 | 1.299 | 15 | -22.75 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 4h | both | fixed_pct | 1.9013 | 1.5813 | 47 | -35.44 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 4h | long | embedded | 1.8843 | -0.0129 | 20 | -37.63 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 12h | both | fixed_signal | 1.8681 | 1.5027 | 17 | -18.26 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| BNBUSDT | 4h | long | fixed_pct | 1.8598 | 1.3495 | 24 | -14.75 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 12h | both | atr | 1.8584 | 1.4504 | 8 | -37.62 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| BTCUSDT | 12h | long | fixed_pct | 1.8325 | 1.3397 | 18 | -12.44 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 12h | both | atr | 1.8315 | 0.6707 | 14 | -39.92 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 12h | both | fixed_signal | 1.8278 | 1.4858 | 29 | -24.68 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| BTCUSDT | 4h | both | atr | 1.8248 | 1.1678 | 85 | -32.38 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| GMXUSDT | 4h | long | atr | 1.813 | 0.8367 | 17 | -31.32 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| UNIUSDT | 4h | long | atr | 1.8115 | 0.8252 | 18 | -29.62 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SOLUSDT | 4h | long | fixed_pct | 1.8022 | 1.9202 | 11 | -13.03 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 12h | short | fixed_signal | 1.7948 | 0.8164 | 18 | -19.54 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | short | atr | 1.7708 | 1.7074 | 39 | -30.85 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 15m | long | fixed_pct | 1.7541 | 0.4524 | 88 | -34.56 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| GMXUSDT | 15m | long | atr | 1.75 | 1.3751 | 146 | -34.52 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ALGOUSDT | 12h | both | fixed_pct | 1.7488 | 1.5461 | 40 | -35.07 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | short | fixed_signal | 1.7434 | 1.4233 | 24 | -25.68 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| AXSUSDT | 12h | short | fixed_pct | 1.7289 | 1.8265 | 9 | -20.83 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ATOMUSDT | 12h | both | embedded | 1.7195 | 0.1889 | 13 | -52.62 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BTCUSDT | 12h | long | fixed_signal | 1.6892 | 1.4795 | 18 | -11.02 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| SOLUSDT | 4h | long | embedded | 1.6879 | 2.149 | 24 | -31.5 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FETUSDT | 4h | long | atr | 1.6669 | 1.6512 | 19 | -41.37 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| MANAUSDT | 12h | both | fixed_pct | 1.6531 | 1.5106 | 12 | -22.8 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| MANAUSDT | 12h | both | fixed_signal | 1.6531 | 1.5276 | 12 | -22.8 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| SANDUSDT | 4h | short | atr | 1.6398 | 2.2661 | 26 | -36.25 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 4h | long | atr | 1.636 | 1.1128 | 32 | -26.76 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ATOMUSDT | 4h | both | embedded | 1.6355 | 0.4593 | 40 | -60.41 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FILUSDT | 4h | both | fixed_pct | 1.6283 | 1.9742 | 84 | -31.04 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 4h | long | fixed_pct | 1.6206 | 1.2459 | 25 | -23.9 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ALGOUSDT | 4h | both | embedded | 1.6106 | 1.329 | 39 | -30.64 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 12h | both | embedded | 1.6099 | 0.4696 | 22 | -31.02 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 12h | both | embedded | 1.603 | 1.0795 | 14 | -33.41 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| ARBUSDT | 4h | short | fixed_pct | 1.599 | 2.4833 | 16 | -13.55 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 12h | long | atr | 1.5872 | 0.859 | 16 | -15.21 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SOLUSDT | 12h | long | atr | 1.5797 | 1.8543 | 16 | -23.65 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 4h | both | fixed_pct | 1.5609 | 1.2306 | 29 | -28.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| GMXUSDT | 15m | long | fixed_signal | 1.5487 | 0.7319 | 198 | -34.39 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SHIBUSDT | 12h | short | fixed_signal | 1.5475 | 1.6077 | 12 | -17.64 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 4h | both | embedded | 1.545 | 1.4154 | 32 | -38.71 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ETHUSDT | 12h | long | fixed_signal | 1.5446 | 1.309 | 21 | -11.04 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FLOWUSDT | 12h | both | fixed_pct | 1.5444 | 2.0988 | 24 | -25.24 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 12h | both | fixed_pct | 1.5418 | 0.6805 | 17 | -21.8 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 12h | short | fixed_pct | 1.5289 | 0.5125 | 9 | -22.08 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 15m | long | fixed_pct | 1.5164 | 0.7408 | 117 | -46.84 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 12h | both | fixed_signal | 1.5083 | 0.9865 | 22 | -18.2 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| BNBUSDT | 15m | long | fixed_signal | 1.5028 | 0.1317 | 130 | -27.75 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| NEARUSDT | 4h | both | embedded | 1.4979 | 1.943 | 38 | -40.07 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| AVAXUSDT | 15m | long | fixed_pct | 1.4746 | 1.0659 | 103 | -32.65 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 12h | both | embedded | 1.4576 | 0.3244 | 18 | -46.98 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 4h | both | embedded | 1.4503 | 2.1521 | 32 | -32.17 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| AVAXUSDT | 12h | both | fixed_signal | 1.4493 | 2.2146 | 38 | -32.04 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| FETUSDT | 4h | long | embedded | 1.4478 | 1.9469 | 15 | -23.46 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| ETHUSDT | 12h | long | embedded | 1.447 | -0.0693 | 14 | -26.28 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 4h | both | atr | 1.4438 | 1.9266 | 27 | -26.75 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 12h | both | embedded | 1.4436 | 0.5319 | 17 | -37.7 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SANDUSDT | 12h | both | embedded | 1.4359 | 0.953 | 27 | -53.68 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SANDUSDT | 12h | short | fixed_signal | 1.4336 | 1.1827 | 16 | -22.3 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 12h | both | embedded | 1.4018 | 1.0418 | 12 | -39.78 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 12h | both | embedded | 1.3997 | 1.4227 | 22 | -30.53 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 12h | both | atr | 1.3952 | 1.5627 | 19 | -37.88 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 15m | both | atr | 1.3777 | 0.0096 | 243 | -80.38 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 4h | short | fixed_pct | 1.3754 | 1.7689 | 16 | -21.12 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 12h | both | embedded | 1.3627 | 1.1423 | 19 | -35.29 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 12h | both | fixed_signal | 1.3596 | 1.4803 | 36 | -31.78 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 12h | both | embedded | 1.3548 | 1.4869 | 23 | -35.85 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| BTCUSDT | 15m | long | fixed_pct | 1.3406 | 0.4283 | 75 | -38.21 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ALGOUSDT | 4h | long | atr | 1.335 | 1.0727 | 24 | -21.9 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 4h | long | embedded | 1.3099 | 1.9035 | 16 | -16.79 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| DYDXUSDT | 4h | short | fixed_pct | 1.3045 | 0.661 | 15 | -35.87 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| AAVEUSDT | 15m | long | atr | 1.2978 | 1.3351 | 106 | -33.57 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| GMXUSDT | 4h | short | embedded | 1.2896 | 1.8935 | 16 | -17.61 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 4h | long | fixed_pct | 1.2841 | 0.8616 | 29 | -27.77 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 4h | long | fixed_pct | 1.2801 | 1.2919 | 26 | -19.11 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | long | fixed_signal | 1.2736 | 1.0613 | 22 | -29.33 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| AAVEUSDT | 4h | long | embedded | 1.2726 | 0.391 | 25 | -29.92 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| AAVEUSDT | 12h | long | atr | 1.2644 | 0.1572 | 21 | -41.48 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 4h | both | atr | 1.2566 | 2.1782 | 35 | -30.15 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 4h | both | fixed_signal | 1.2495 | 2.0663 | 80 | -24.24 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 4h | short | embedded | 1.2434 | 1.4172 | 18 | -32.92 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 4h | both | fixed_signal | 1.2431 | 1.2585 | 42 | -27.53 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| NEARUSDT | 4h | both | atr | 1.2416 | 2.4664 | 24 | -37.69 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| FILUSDT | 15m | both | atr | 1.2313 | 1.068 | 249 | -65.67 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | short | embedded | 1.2267 | 0.7232 | 20 | -52.71 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FETUSDT | 12h | both | atr | 1.2201 | 1.8501 | 16 | -39.19 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SOLUSDT | 4h | long | atr | 1.2137 | 2.0936 | 12 | -12.99 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 15m | long | embedded | 1.2132 | -0.47 | 161 | -40.83 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ATOMUSDT | 12h | both | fixed_pct | 1.212 | 1.3371 | 31 | -31.84 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 15m | long | atr | 1.2118 | 0.1814 | 140 | -62.0 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SHIBUSDT | 15m | long | embedded | 1.2103 | -0.3348 | 218 | -57.33 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 12h | short | embedded | 1.2055 | -0.2746 | 12 | -56.52 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 4h | long | atr | 1.2031 | 1.5909 | 42 | -32.38 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 12h | both | embedded | 1.1983 | 1.1144 | 10 | -41.19 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| AVAXUSDT | 4h | long | fixed_signal | 1.1938 | 1.9906 | 35 | -21.92 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 4h | both | fixed_pct | 1.1938 | 1.9437 | 30 | -17.56 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ARBUSDT | 15m | short | fixed_pct | 1.1888 | 1.6633 | 89 | -62.73 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 15m | short | fixed_signal | 1.188 | 0.2236 | 124 | -33.67 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ARBUSDT | 4h | both | embedded | 1.1793 | 1.2153 | 32 | -23.11 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | short | fixed_pct | 1.172 | 1.4071 | 8 | -25.21 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | short | fixed_signal | 1.172 | 1.1461 | 8 | -25.21 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ADAUSDT | 15m | long | fixed_signal | 1.1641 | 0.1225 | 139 | -52.37 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| DYDXUSDT | 12h | short | fixed_pct | 1.1575 | 0.903 | 17 | -23.06 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 4h | short | fixed_signal | 1.1479 | 1.2596 | 28 | -20.16 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| SEIUSDT | 4h | long | fixed_pct | 1.138 | 1.7007 | 29 | -26.48 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 12h | long | fixed_pct | 1.1331 | 1.1 | 19 | -15.91 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| DASHUSDT | 4h | both | atr | 1.1301 | 0.92 | 26 | -37.93 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| INJUSDT | 4h | short | embedded | 1.1273 | 1.1552 | 16 | -27.57 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| DOGEUSDT | 15m | both | fixed_pct | 1.1203 | 0.0965 | 350 | -65.8 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DOTUSDT | 12h | both | fixed_signal | 1.1055 | 0.7512 | 28 | -40.95 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| LINKUSDT | 12h | both | fixed_pct | 1.0984 | 0.9621 | 19 | -24.72 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ETCUSDT | 4h | both | atr | 1.0913 | 1.5727 | 29 | -39.72 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 4h | short | embedded | 1.0876 | 1.5368 | 17 | -24.04 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| SANDUSDT | 15m | short | fixed_pct | 1.0773 | 1.8029 | 150 | -33.37 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| BNBUSDT | 12h | short | fixed_pct | 1.0754 | 1.3135 | 5 | -17.39 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| BNBUSDT | 12h | short | fixed_signal | 1.0754 | 1.0718 | 5 | -18.83 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| AAVEUSDT | 4h | long | atr | 1.0738 | 1.3513 | 33 | -34.97 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 15m | long | atr | 1.0707 | 1.1147 | 164 | -35.32 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 12h | both | fixed_pct | 1.0685 | 0.7498 | 29 | -36.15 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 12h | short | fixed_pct | 1.068 | 1.7615 | 12 | -15.9 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 12h | both | atr | 1.0666 | 1.1741 | 25 | -38.06 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 4h | both | fixed_signal | 1.0563 | 2.4379 | 62 | -28.75 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 4h | long | atr | 1.0542 | 1.9965 | 19 | -25.38 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| CHZUSDT | 15m | long | atr | 1.0464 | 0.1872 | 107 | -74.61 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 15m | short | embedded | 1.0459 | -0.072 | 237 | -39.53 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 15m | long | atr | 1.0445 | 0.8688 | 153 | -54.83 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 4h | long | fixed_pct | 1.0415 | 1.6305 | 46 | -26.42 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 12h | both | atr | 1.0302 | 1.3241 | 20 | -34.26 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 12h | both | fixed_signal | 1.0149 | 0.9159 | 24 | -16.46 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 15m | long | fixed_signal | 1.0096 | 1.2909 | 152 | -21.87 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| OPUSDT | 12h | short | fixed_pct | 1.0085 | 1.2603 | 26 | -16.72 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| OPUSDT | 12h | short | fixed_signal | 1.0085 | 1.281 | 26 | -16.72 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 4h | short | embedded | 1.0065 | 1.4876 | 13 | -19.06 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| BTCUSDT | 12h | long | embedded | 0.9977 | 0.6107 | 17 | -21.72 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 15m | long | fixed_pct | 0.9844 | 0.5421 | 64 | -42.81 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 12h | short | fixed_signal | 0.9831 | -0.5825 | 10 | -32.87 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 12h | both | atr | 0.9784 | 1.5459 | 17 | -32.2 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| DOTUSDT | 4h | short | atr | 0.9686 | 1.816 | 13 | -31.26 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 4h | both | embedded | 0.9588 | 0.2105 | 39 | -49.17 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 4h | both | fixed_pct | 0.9502 | 1.4967 | 49 | -22.43 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| DYDXUSDT | 12h | both | atr | 0.9466 | 0.9267 | 13 | -59.77 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 12h | short | atr | 0.9361 | 1.0409 | 17 | -32.96 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 12h | short | atr | 0.933 | 1.0083 | 7 | -40.62 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DYDXUSDT | 4h | both | atr | 0.9248 | 1.2724 | 25 | -50.78 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 15m | long | fixed_signal | 0.9234 | 0.0349 | 167 | -45.29 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FLOWUSDT | 4h | both | atr | 0.9206 | 1.8934 | 29 | -36.34 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 12h | short | atr | 0.9201 | 0.7727 | 11 | -33.42 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 15m | long | embedded | 0.913 | -0.671 | 148 | -66.96 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ADAUSDT | 4h | long | embedded | 0.9035 | 0.9534 | 25 | -37.01 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | short | fixed_pct | 0.8953 | 1.6168 | 24 | -18.27 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| GMXUSDT | 4h | both | fixed_pct | 0.8933 | 0.9594 | 77 | -29.75 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BTCUSDT | 4h | short | fixed_pct | 0.8877 | 1.5693 | 20 | -13.17 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| OPUSDT | 4h | short | atr | 0.8822 | 0.8958 | 18 | -25.75 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ETHUSDT | 4h | short | atr | 0.8817 | 1.4773 | 18 | -26.48 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ARBUSDT | 4h | short | embedded | 0.8792 | 1.3618 | 15 | -11.4 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ETCUSDT | 12h | both | atr | 0.8768 | 1.1597 | 25 | -28.31 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 12h | long | fixed_pct | 0.865 | 1.4136 | 18 | -18.85 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 12h | long | fixed_signal | 0.865 | 1.4136 | 18 | -18.85 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 4h | long | fixed_pct | 0.8615 | 1.8612 | 34 | -24.09 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 4h | long | embedded | 0.8575 | 1.0564 | 27 | -19.29 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 15m | short | fixed_pct | 0.8562 | 1.3564 | 177 | -48.89 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 15m | long | embedded | 0.8488 | 3.1633 | 218 | -17.07 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 15m | long | fixed_signal | 0.8462 | 0.7835 | 146 | -21.98 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 12h | long | fixed_pct | 0.8344 | 1.4266 | 13 | -14.11 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ENAUSDT | 4h | long | fixed_pct | 0.8342 | -0.1409 | 33 | -19.13 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETCUSDT | 12h | both | fixed_pct | 0.8281 | 1.5608 | 36 | -17.34 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| FETUSDT | 4h | both | embedded | 0.8276 | 1.1197 | 30 | -42.3 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 4h | both | embedded | 0.8239 | 1.0911 | 24 | -39.5 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ALGOUSDT | 15m | both | fixed_pct | 0.8169 | 1.2339 | 243 | -33.49 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SANDUSDT | 4h | short | embedded | 0.8092 | 1.8967 | 26 | -34.22 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SEIUSDT | 4h | both | embedded | 0.8045 | 1.8419 | 18 | -33.87 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 4h | both | embedded | 0.8033 | 1.3766 | 44 | -29.43 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 15m | long | atr | 0.7859 | 0.4384 | 178 | -26.57 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| DOTUSDT | 15m | both | fixed_pct | 0.7807 | 0.6972 | 289 | -52.72 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ETHUSDT | 12h | both | fixed_signal | 0.7734 | 1.3344 | 24 | -24.3 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 4h | both | fixed_pct | 0.757 | 2.4103 | 61 | -28.0 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 12h | short | fixed_signal | 0.7561 | 0.2946 | 12 | -25.14 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ADAUSDT | 15m | long | embedded | 0.7481 | -0.1877 | 229 | -61.08 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| BNBUSDT | 12h | long | atr | 0.7368 | -0.6384 | 25 | -33.69 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 12h | both | fixed_pct | 0.7358 | 2.0485 | 23 | -19.27 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| SANDUSDT | 12h | short | embedded | 0.7327 | 1.0936 | 12 | -39.77 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 12h | both | fixed_signal | 0.7315 | 1.3967 | 16 | -17.94 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ALGOUSDT | 12h | short | fixed_signal | 0.7311 | 1.4153 | 23 | -33.39 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 12h | both | atr | 0.7275 | 1.2994 | 23 | -32.59 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | both | fixed_pct | 0.7183 | 1.4998 | 66 | -28.32 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ETHUSDT | 4h | long | embedded | 0.7153 | 1.3082 | 17 | -13.92 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| FLOWUSDT | 4h | short | embedded | 0.7075 | 1.808 | 19 | -37.76 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 12h | both | fixed_pct | 0.7051 | 1.457 | 16 | -17.94 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| BTCUSDT | 4h | long | atr | 0.7017 | 1.3314 | 55 | -10.99 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | both | embedded | 0.7013 | 1.3636 | 24 | -27.98 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SEIUSDT | 15m | long | fixed_pct | 0.6985 | 1.5505 | 83 | -45.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| LTCUSDT | 12h | long | fixed_pct | 0.6983 | -0.4509 | 18 | -34.11 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| DYDXUSDT | 4h | short | fixed_signal | 0.6965 | 0.7663 | 25 | -34.1 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 15m | both | embedded | 0.6917 | 2.323 | 471 | -39.57 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| AXSUSDT | 4h | short | embedded | 0.6901 | 1.2606 | 27 | -23.22 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| ETCUSDT | 4h | short | atr | 0.6741 | 1.6322 | 18 | -27.03 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 15m | long | fixed_pct | 0.6732 | 0.3309 | 125 | -59.66 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| TRXUSDT | 12h | both | atr | 0.6729 | 0.4761 | 12 | -40.58 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 12h | both | atr | 0.6636 | 1.5953 | 18 | -38.1 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| LINKUSDT | 12h | short | fixed_pct | 0.6588 | 0.2982 | 20 | -35.69 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 4h | long | atr | 0.6549 | 0.7988 | 46 | -30.66 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 12h | long | fixed_pct | 0.6478 | 1.0073 | 23 | -12.92 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 12h | both | fixed_pct | 0.6456 | 1.2588 | 23 | -26.87 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 4h | long | fixed_pct | 0.6445 | 1.227 | 16 | -20.53 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| LINKUSDT | 4h | both | embedded | 0.6379 | 0.7594 | 41 | -50.49 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| AAVEUSDT | 12h | both | atr | 0.6289 | 1.2145 | 19 | -46.84 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| MANAUSDT | 4h | both | embedded | 0.6282 | 1.335 | 37 | -31.91 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 4h | both | fixed_pct | 0.6182 | 2.6788 | 65 | -28.01 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FLOWUSDT | 12h | short | embedded | 0.6161 | 1.894 | 9 | -31.84 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 4h | long | embedded | 0.6086 | 0.3875 | 26 | -44.33 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 4h | short | fixed_pct | 0.603 | 1.0694 | 30 | -20.69 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 4h | both | fixed_pct | 0.6026 | 1.8048 | 71 | -36.73 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ARBUSDT | 15m | short | embedded | 0.6004 | 0.2711 | 227 | -36.55 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| TAOUSDT | 4h | both | atr | 0.5986 | 3.4745 | 19 | -25.38 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 12h | long | fixed_pct | 0.5945 | -0.1103 | 33 | -23.39 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 12h | long | fixed_signal | 0.5945 | -0.1103 | 33 | -23.39 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 4h | short | fixed_signal | 0.5901 | 0.9999 | 19 | -9.4 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 12h | long | atr | 0.5786 | 1.2541 | 21 | -13.86 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 15m | both | fixed_pct | 0.5767 | 1.104 | 309 | -61.95 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| AXSUSDT | 15m | short | fixed_pct | 0.5766 | 1.5992 | 161 | -31.62 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| INJUSDT | 4h | both | fixed_signal | 0.5686 | 1.9842 | 51 | -30.63 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| FILUSDT | 4h | both | atr | 0.5671 | 1.9031 | 47 | -29.42 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 12h | short | embedded | 0.5645 | 0.2877 | 13 | -55.89 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 4h | long | fixed_signal | 0.5635 | 1.2526 | 29 | -16.02 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| APTUSDT | 4h | short | embedded | 0.5575 | 1.5944 | 17 | -22.09 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SOLUSDT | 12h | long | fixed_pct | 0.5569 | 2.1025 | 26 | -13.8 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SOLUSDT | 12h | both | fixed_pct | 0.555 | 2.6827 | 25 | -21.47 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 4h | short | embedded | 0.5533 | 0.4199 | 11 | -30.48 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 15m | long | fixed_signal | 0.5475 | 0.9331 | 179 | -24.19 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ICPUSDT | 4h | long | fixed_pct | 0.5469 | 1.421 | 11 | -15.57 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| SANDUSDT | 12h | short | atr | 0.5464 | 1.5271 | 14 | -26.38 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ADAUSDT | 12h | long | fixed_signal | 0.545 | 0.7885 | 17 | -31.5 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 4h | short | embedded | 0.5425 | 1.6529 | 23 | -21.29 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| TRXUSDT | 4h | both | fixed_signal | 0.5423 | 0.6733 | 55 | -25.61 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SHIBUSDT | 15m | both | embedded | 0.5411 | -0.484 | 397 | -86.91 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| LINKUSDT | 12h | both | embedded | 0.5402 | 0.3558 | 20 | -50.54 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 12h | long | fixed_pct | 0.5268 | 2.0345 | 15 | -14.32 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FLOWUSDT | 12h | both | atr | 0.5234 | 1.3022 | 19 | -69.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 4h | both | atr | 0.5233 | 1.5911 | 33 | -30.58 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| MANAUSDT | 15m | long | atr | 0.5106 | 0.5982 | 151 | -34.99 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 15m | short | fixed_pct | 0.5067 | 1.0026 | 125 | -59.98 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| GMXUSDT | 12h | long | fixed_signal | 0.5054 | 1.0819 | 22 | -16.08 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ADAUSDT | 12h | both | embedded | 0.5042 | 1.1309 | 13 | -37.13 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 4h | both | atr | 0.5006 | 2.3536 | 34 | -47.99 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 12h | both | embedded | 0.4999 | 1.847 | 26 | -46.33 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SEIUSDT | 15m | long | atr | 0.4963 | 1.6211 | 180 | -40.77 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETCUSDT | 4h | short | fixed_pct | 0.4958 | 1.91 | 32 | -21.63 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FILUSDT | 12h | short | embedded | 0.4947 | 1.0762 | 10 | -39.09 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| ETCUSDT | 4h | short | fixed_signal | 0.4922 | 1.7396 | 42 | -23.36 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| LTCUSDT | 12h | both | fixed_pct | 0.4872 | 1.1635 | 17 | -16.05 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| DOGEUSDT | 12h | short | fixed_pct | 0.4871 | 0.4085 | 11 | -40.93 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 4h | long | embedded | 0.4806 | 1.3904 | 23 | -23.78 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| BNBUSDT | 12h | both | embedded | 0.4791 | 1.0865 | 19 | -21.46 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ATOMUSDT | 15m | short | fixed_pct | 0.4692 | 1.2991 | 122 | -42.49 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SANDUSDT | 4h | both | embedded | 0.463 | 1.2314 | 51 | -43.44 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| MANAUSDT | 4h | both | atr | 0.4612 | 1.4281 | 36 | -44.13 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 15m | both | atr | 0.4574 | 1.0045 | 295 | -59.06 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 4h | both | fixed_signal | 0.4535 | 1.29 | 45 | -25.98 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| BTCUSDT | 15m | long | embedded | 0.4421 | 0.3419 | 157 | -22.63 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ARBUSDT | 4h | short | atr | 0.4376 | 2.096 | 16 | -16.46 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| DASHUSDT | 12h | both | atr | 0.4355 | 1.3113 | 31 | -31.94 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 4h | short | fixed_signal | 0.4339 | 2.2653 | 45 | -27.22 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 15m | long | fixed_signal | 0.4328 | 3.3564 | 278 | -15.94 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ATOMUSDT | 15m | short | fixed_signal | 0.4204 | 0.4718 | 242 | -41.97 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| DYDXUSDT | 12h | short | fixed_signal | 0.4162 | 0.751 | 20 | -26.75 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETCUSDT | 4h | short | embedded | 0.4097 | 1.4431 | 20 | -28.15 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 15m | long | fixed_pct | 0.4077 | 2.6928 | 252 | -30.58 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| GMXUSDT | 15m | both | fixed_pct | 0.4018 | 2.9877 | 481 | -30.08 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ARBUSDT | 12h | both | fixed_signal | 0.4007 | 1.8781 | 25 | -27.4 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| INJUSDT | 4h | short | fixed_signal | 0.3994 | 1.4226 | 32 | -24.67 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 15m | long | atr | 0.3964 | 0.813 | 156 | -39.37 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| LTCUSDT | 4h | short | atr | 0.3909 | 0.9684 | 10 | -28.22 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 15m | long | fixed_pct | 0.3887 | 0.3339 | 180 | -39.04 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 15m | short | atr | 0.3882 | 0.7035 | 207 | -48.99 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| DOTUSDT | 15m | short | fixed_pct | 0.3854 | 1.5763 | 194 | -33.19 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ATOMUSDT | 15m | both | fixed_pct | 0.3843 | 0.5738 | 222 | -50.16 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| INJUSDT | 4h | long | atr | 0.376 | 1.9167 | 15 | -31.31 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 12h | both | fixed_signal | 0.3599 | 1.9811 | 30 | -29.53 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 4h | both | atr | 0.3453 | 2.2269 | 39 | -41.59 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOGEUSDT | 15m | short | fixed_pct | 0.3431 | 0.0905 | 117 | -62.11 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 15m | long | embedded | 0.3422 | 0.6969 | 233 | -31.6 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ETCUSDT | 4h | both | fixed_pct | 0.339 | 1.9653 | 91 | -20.6 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| TAOUSDT | 15m | short | fixed_pct | 0.3316 | 4.2057 | 40 | -17.9 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 12h | long | fixed_signal | 0.3285 | 1.0546 | 32 | -12.92 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SUIUSDT | 15m | both | fixed_pct | 0.3281 | 0.569 | 141 | -63.9 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| BNBUSDT | 4h | long | atr | 0.3263 | 1.1274 | 21 | -17.9 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 4h | short | embedded | 0.3213 | 0.7673 | 15 | -19.99 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SANDUSDT | 15m | both | embedded | 0.319 | 0.0439 | 706 | -65.74 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| RUNEUSDT | 15m | both | fixed_pct | 0.3076 | 2.2034 | 357 | -51.75 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 4h | short | fixed_pct | 0.3041 | 2.079 | 29 | -23.61 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| MANAUSDT | 4h | short | atr | 0.3011 | 1.9527 | 14 | -35.17 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| SEIUSDT | 15m | short | atr | 0.2984 | 1.0151 | 96 | -53.82 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| FILUSDT | 4h | both | fixed_signal | 0.2957 | 2.0364 | 39 | -18.97 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| AXSUSDT | 4h | short | fixed_pct | 0.2911 | 1.6257 | 28 | -26.44 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| AAVEUSDT | 4h | both | atr | 0.2906 | 1.7532 | 55 | -48.74 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| TRXUSDT | 4h | long | atr | 0.2885 | 0.7095 | 21 | -40.08 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DYDXUSDT | 15m | both | atr | 0.2858 | 0.826 | 330 | -61.94 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| AXSUSDT | 4h | both | embedded | 0.2827 | 1.0834 | 64 | -40.37 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| OPUSDT | 12h | both | fixed_signal | 0.2754 | 1.6469 | 34 | -25.44 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 15m | both | fixed_signal | 0.2611 | 2.5027 | 557 | -33.01 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| DYDXUSDT | 15m | short | fixed_pct | 0.2515 | 0.9096 | 112 | -53.61 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| SUIUSDT | 12h | both | fixed_pct | 0.2471 | 1.6506 | 19 | -16.62 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| ADAUSDT | 12h | short | fixed_pct | 0.2415 | 1.9186 | 10 | -12.37 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| DOTUSDT | 12h | short | fixed_signal | 0.2372 | 0.5293 | 13 | -20.25 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| INJUSDT | 4h | both | embedded | 0.2357 | 1.6162 | 44 | -50.04 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | both | fixed_pct | 0.2313 | 1.2877 | 29 | -24.75 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| GMXUSDT | 15m | both | embedded | 0.2275 | 1.0905 | 800 | -41.67 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| SANDUSDT | 4h | long | embedded | 0.2263 | 0.0192 | 24 | -40.11 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| SANDUSDT | 15m | long | embedded | 0.2208 | -0.5842 | 328 | -57.54 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| NEARUSDT | 4h | short | fixed_signal | 0.2157 | 2.5045 | 27 | -12.5 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| FILUSDT | 4h | short | embedded | 0.2147 | 1.3498 | 33 | -28.11 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ALGOUSDT | 15m | long | atr | 0.2079 | 0.4243 | 169 | -35.59 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 15m | both | atr | 0.2054 | 2.5311 | 336 | -58.78 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| SEIUSDT | 4h | both | fixed_pct | 0.1959 | 2.0808 | 24 | -18.8 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 12h | long | atr | 0.1925 | 0.517 | 17 | -47.43 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| CHZUSDT | 4h | long | atr | 0.1817 | 1.1137 | 28 | -33.5 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| DOGEUSDT | 4h | short | fixed_signal | 0.179 | 0.4393 | 40 | -23.27 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 12h | long | fixed_signal | 0.1772 | 2.0345 | 16 | -14.32 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| LINKUSDT | 4h | both | fixed_pct | 0.1633 | 1.6091 | 29 | -31.86 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| AVAXUSDT | 15m | both | fixed_pct | 0.1589 | 1.8156 | 320 | -41.33 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| MANAUSDT | 15m | both | fixed_pct | 0.1534 | 0.9304 | 269 | -50.07 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| CHZUSDT | 15m | short | embedded | 0.1459 | 0.2836 | 479 | -51.04 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| SOLUSDT | 4h | both | atr | 0.1457 | 2.4659 | 39 | -38.51 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ICPUSDT | 4h | both | fixed_pct | 0.1432 | 2.0665 | 67 | -37.8 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AVAXUSDT | 12h | both | atr | 0.1391 | 2.4381 | 26 | -21.3 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 4h | short | fixed_pct | 0.1333 | 2.2709 | 21 | -30.34 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| FETUSDT | 4h | both | fixed_pct | 0.1298 | 1.3755 | 107 | -30.46 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| INJUSDT | 12h | short | fixed_signal | 0.126 | 0.2619 | 23 | -20.48 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SEIUSDT | 4h | long | atr | 0.1212 | 1.4171 | 23 | -39.44 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| SHIBUSDT | 15m | short | fixed_pct | 0.1182 | 0.5271 | 123 | -54.17 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ETHUSDT | 4h | both | embedded | 0.1152 | 1.3226 | 31 | -24.42 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 2.0, "ad...` |
| ENAUSDT | 15m | long | embedded | 0.1073 | 1.5514 | 99 | -25.5 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| ALGOUSDT | 15m | short | atr | 0.1072 | 1.5456 | 137 | -48.59 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FETUSDT | 12h | both | embedded | 0.1027 | 1.4588 | 21 | -59.96 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| NEARUSDT | 4h | short | fixed_pct | 0.0944 | 2.3753 | 26 | -13.17 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| LTCUSDT | 12h | long | fixed_signal | 0.0898 | -0.2964 | 24 | -30.8 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| LTCUSDT | 4h | long | embedded | 0.088 | 0.3516 | 18 | -25.11 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.2, "ad...` |
| RUNEUSDT | 12h | long | atr | 0.0806 | 1.5144 | 14 | -20.25 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ATOMUSDT | 15m | short | atr | 0.0804 | 0.9203 | 172 | -46.74 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.5, "ad...` |
| NEARUSDT | 4h | short | embedded | 0.0738 | 1.9057 | 8 | -23.36 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| SOLUSDT | 15m | both | atr | 0.0722 | 1.4767 | 240 | -50.32 | `{"profile_lookback": 200, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| AVAXUSDT | 15m | both | atr | 0.072 | 1.418 | 466 | -37.55 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 2.0, "ad...` |
| FLOWUSDT | 4h | short | fixed_signal | 0.0701 | 2.0273 | 42 | -28.11 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FILUSDT | 4h | short | fixed_signal | 0.0527 | 1.9224 | 18 | -17.58 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| SOLUSDT | 15m | both | fixed_pct | 0.052 | 1.4729 | 309 | -43.65 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| BTCUSDT | 4h | long | fixed_signal | 0.0505 | 1.181 | 20 | -14.46 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| FILUSDT | 4h | long | atr | 0.0476 | 0.9709 | 25 | -22.63 | `{"profile_lookback": 100, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| ETCUSDT | 15m | short | fixed_signal | 0.0447 | 0.5986 | 262 | -38.42 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| MANAUSDT | 12h | short | fixed_signal | 0.0424 | 0.9522 | 10 | -18.75 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| FETUSDT | 15m | long | embedded | 0.0346 | -0.6682 | 213 | -88.28 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| RUNEUSDT | 12h | both | fixed_pct | 0.0312 | 1.8846 | 30 | -26.71 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| FILUSDT | 4h | short | fixed_pct | 0.0227 | 1.9725 | 18 | -16.97 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| MANAUSDT | 4h | short | fixed_signal | 0.0221 | 1.844 | 18 | -24.82 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |
| FLOWUSDT | 12h | short | fixed_signal | 0.0165 | 1.8414 | 18 | -34.71 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| AXSUSDT | 12h | short | embedded | 0.0143 | 0.2401 | 8 | -40.65 | `{"profile_lookback": 100, "value_area_pct": 70, "volume_spike_mult": 1.2, "ad...` |
| MANAUSDT | 12h | short | embedded | 0.0139 | 0.9981 | 9 | -38.48 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| ETHUSDT | 15m | both | fixed_pct | 0.0101 | 1.0004 | 289 | -52.93 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| GMXUSDT | 15m | short | embedded | 0.0083 | 1.4409 | 309 | -46.24 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 1.2, "ad...` |
| BNBUSDT | 4h | both | atr | 0.0053 | 1.0062 | 48 | -26.17 | `{"profile_lookback": 100, "value_area_pct": 60, "volume_spike_mult": 1.5, "ad...` |
| ETHUSDT | 15m | long | embedded | 0.0043 | 0.8826 | 154 | -26.33 | `{"profile_lookback": 200, "value_area_pct": 60, "volume_spike_mult": 2.0, "ad...` |
| LINKUSDT | 15m | short | fixed_pct | 0.002 | 1.2304 | 160 | -40.18 | `{"profile_lookback": 200, "value_area_pct": 80, "volume_spike_mult": 1.5, "ad...` |

**Stage 2 pass rate: 397 / 729**
