# MO1 — Stage 2 Summary (home TF: 4H, 39 symbols)

**Date:** 2026-06-02
**Off-TFs tested:** 15m, 1h, 12h
**Pass filter:** train_trades ≥ 30 AND OOS Sharpe > 0
**Note:** `Trades` column shows OOS trade count (train count guaranteed ≥ 30)
**Combos completed:** 639 / 1404  (39 symbols × 3 dir × 4 SL × 3 TFs max)
**Pass rate:** 335 / 639

---

## Pass/Fail Table — 15M

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ❌ | ✅ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ |
| ETHUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ❌ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ❌ | ⬜ | ❌ | ❌ | ❌ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ❌ |
| LINKUSDT | ❌ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| ATOMUSDT | ✅ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ❌ | ✅ | ❌ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ❌ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⬜ | ❌ | ⬜ |
| NEARUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| TRXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| ALGOUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ |
| SANDUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| RUNEUSDT | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ❌ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ |
| ICPUSDT | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ✅ | ❌ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ |
| FETUSDT | ❌ | ❌ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ❌ | ❌ | ✅ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ❌ | ⬜ | ⬜ | ❌ | ✅ | ❌ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 1H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ✅ | ❌ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ |
| ETHUSDT | ⬜ | ✅ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ✅ | ⬜ | ❌ | ❌ | ✅ | ❌ | ❌ | ⬜ | ❌ | ✅ | ❌ | ❌ |
| LINKUSDT | ❌ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| ATOMUSDT | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ❌ | ❌ | ❌ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ❌ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ⬜ | ✅ | ⬜ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| TRXUSDT | ✅ | ✅ | ✅ | ❌ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ✅ |
| ALGOUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ✅ |
| SANDUSDT | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| RUNEUSDT | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ✅ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ❌ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ✅ |
| ICPUSDT | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ❌ | ❌ |
| FETUSDT | ✅ | ✅ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ❌ | ✅ | ✅ | ❌ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ❌ | ❌ |
| GMXUSDT | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |

## Pass/Fail Table — 12H

| Symbol | both/emb | both/fpct | both/fsig | both/atr | long/emb | long/fpct | long/fsig | long/atr | short/emb | short/fpct | short/fsig | short/atr |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ✅ | ✅ | ✅ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ✅ |
| ETHUSDT | ⬜ | ❌ | ❌ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ✅ | ⬜ | ✅ | ✅ | ❌ | ✅ | ✅ | ⬜ | ❌ | ✅ | ✅ | ✅ |
| LINKUSDT | ✅ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| BCHUSDT | ⬜ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ❌ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ⬜ | ❌ | ❌ | ⬜ |
| ATOMUSDT | ✅ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ✅ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ | ⬜ | ✅ | ⬜ |
| NEARUSDT | ✅ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| TRXUSDT | ✅ | ✅ | ✅ | ✅ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ❌ |
| ALGOUSDT | ✅ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ✅ | ⬜ | ✅ | ❌ | ❌ |
| SANDUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ❌ | ❌ | ⬜ |
| RUNEUSDT | ❌ | ⬜ | ⬜ | ⬜ | ✅ | ⬜ | ❌ | ✅ | ❌ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ✅ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| DASHUSDT | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |
| CHZUSDT | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SHIBUSDT | ⬜ | ✅ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| ICPUSDT | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ | ✅ | ⬜ | ⬜ | ✅ | ✅ |
| FETUSDT | ✅ | ✅ | ✅ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ✅ | ❌ | ❌ | ✅ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ✅ | ✅ |
| GMXUSDT | ⬜ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ✅ | ⬜ | ⬜ | ⬜ | ❌ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ✅ | ✅ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ❌ | ⬜ | ⬜ | ✅ | ❌ | ✅ | ⬜ | ✅ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ❌ | ⬜ | ❌ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ✅ | ✅ | ⬜ | ⬜ | ⬜ | ❌ | ❌ | ⬜ | ⬜ | ⬜ | ⬜ |

---

## Passing Combos (proceed to Stage 3)

| Symbol | Off-TF | Direction | SL Type | OOS Sharpe | Train Sharpe | OOS Trades | Max DD% | Best Params |
|---|---|---|---|---|---|---|---|---|
| SUIUSDT | 15m | long | embedded | 3.8952 | 0.6042 | 179 | -56.41 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| SUIUSDT | 1h | long | embedded | 3.0644 | 0.5752 | 35 | -59.65 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 15m | both | embedded | 2.9756 | -0.7881 | 626 | -87.61 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| TRXUSDT | 15m | long | fixed_signal | 2.6862 | 1.5376 | 172 | -27.85 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| AVAXUSDT | 12h | both | fixed_pct | 2.5722 | 1.9842 | 50 | -30.35 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AVAXUSDT | 12h | both | fixed_signal | 2.5722 | 1.9842 | 50 | -30.35 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| SUIUSDT | 1h | long | fixed_pct | 2.5394 | 1.0909 | 83 | -29.96 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 15m | both | fixed_signal | 2.3381 | -0.112 | 623 | -82.84 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AAVEUSDT | 1h | long | embedded | 2.3224 | 0.5297 | 101 | -56.59 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BNBUSDT | 12h | long | embedded | 2.318 | 0.2612 | 10 | -42.2 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| TRXUSDT | 15m | both | fixed_pct | 2.2776 | 0.0249 | 607 | -80.93 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| TRXUSDT | 1h | long | atr | 2.2766 | 0.9733 | 77 | -38.84 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| TRXUSDT | 15m | long | fixed_pct | 2.2708 | 1.6108 | 174 | -25.13 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| DOGEUSDT | 12h | long | embedded | 2.2024 | 0.3648 | 10 | -47.59 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 12h | long | fixed_pct | 2.161 | 1.6612 | 26 | -19.45 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AVAXUSDT | 12h | long | fixed_signal | 2.161 | 1.6612 | 26 | -19.45 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| BCHUSDT | 12h | both | atr | 2.1291 | 0.8232 | 28 | -47.13 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 1h | long | fixed_signal | 2.1157 | 1.4467 | 87 | -24.38 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ALGOUSDT | 12h | long | embedded | 2.1113 | -0.5804 | 14 | -74.47 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ICPUSDT | 12h | both | fixed_pct | 2.0668 | 1.2458 | 47 | -30.75 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| ICPUSDT | 12h | both | fixed_signal | 2.0668 | 1.2458 | 47 | -30.75 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| DOGEUSDT | 15m | long | atr | 2.0293 | 0.0398 | 217 | -61.56 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AAVEUSDT | 15m | long | embedded | 1.9873 | 0.8703 | 148 | -54.82 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| FLOWUSDT | 12h | long | fixed_signal | 1.9508 | 0.7183 | 15 | -22.9 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| FLOWUSDT | 12h | both | fixed_signal | 1.932 | 1.5434 | 52 | -29.02 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| SUIUSDT | 12h | long | atr | 1.8885 | 0.1007 | 15 | -41.96 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 1h | both | fixed_signal | 1.8876 | 0.3673 | 147 | -39.47 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| SEIUSDT | 15m | long | embedded | 1.862 | 1.0347 | 82 | -64.94 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 1h | both | embedded | 1.8548 | -0.6793 | 293 | -72.81 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| FLOWUSDT | 12h | both | fixed_pct | 1.8521 | 1.5336 | 43 | -25.44 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BTCUSDT | 15m | long | atr | 1.8428 | 0.5688 | 252 | -40.35 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AXSUSDT | 12h | long | fixed_pct | 1.8393 | 1.1438 | 22 | -15.89 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AXSUSDT | 12h | long | fixed_signal | 1.8393 | 1.1438 | 22 | -15.89 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| DOTUSDT | 12h | both | embedded | 1.8389 | 1.0418 | 17 | -40.97 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BTCUSDT | 12h | long | atr | 1.8342 | 0.2592 | 19 | -33.28 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| SUIUSDT | 12h | long | fixed_pct | 1.7772 | 0.7898 | 15 | -20.48 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| AXSUSDT | 12h | both | atr | 1.7703 | 0.9923 | 35 | -46.92 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| ALGOUSDT | 15m | long | embedded | 1.7695 | -0.1823 | 221 | -77.81 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| NEARUSDT | 15m | long | atr | 1.766 | -0.067 | 133 | -87.27 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| FETUSDT | 12h | long | embedded | 1.743 | 0.8692 | 12 | -80.23 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| ETHUSDT | 1h | long | fixed_pct | 1.7366 | 0.8319 | 128 | -32.52 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| AAVEUSDT | 12h | long | embedded | 1.7335 | 0.4151 | 14 | -57.58 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 12h | short | fixed_signal | 1.7078 | 2.3657 | 31 | -19.2 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| LINKUSDT | 12h | both | fixed_pct | 1.7053 | 1.7903 | 45 | -35.79 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| FETUSDT | 12h | both | embedded | 1.6867 | 1.4176 | 21 | -63.24 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| BCHUSDT | 15m | long | embedded | 1.6734 | 0.1995 | 96 | -66.84 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ENAUSDT | 1h | long | fixed_signal | 1.6689 | 2.1781 | 64 | -23.94 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| BCHUSDT | 15m | long | atr | 1.6579 | -0.1042 | 96 | -71.7 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| NEARUSDT | 1h | long | atr | 1.63 | 0.5695 | 61 | -57.97 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| FETUSDT | 1h | long | embedded | 1.6244 | 0.8899 | 34 | -84.06 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| ARBUSDT | 15m | long | embedded | 1.6182 | 0.2078 | 74 | -53.59 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| DOGEUSDT | 1h | long | embedded | 1.6175 | 0.4709 | 37 | -54.48 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| FILUSDT | 12h | both | fixed_pct | 1.6099 | 1.8698 | 39 | -24.03 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| FILUSDT | 12h | both | fixed_signal | 1.6099 | 1.8698 | 39 | -24.03 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| AVAXUSDT | 15m | both | atr | 1.5772 | 1.369 | 391 | -59.71 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ALGOUSDT | 15m | long | atr | 1.5754 | -0.4905 | 234 | -76.22 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| SOLUSDT | 1h | long | atr | 1.5598 | 0.745 | 77 | -70.84 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| UNIUSDT | 12h | long | embedded | 1.5237 | -0.0678 | 10 | -46.62 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| MANAUSDT | 12h | long | fixed_signal | 1.5229 | 0.8843 | 18 | -22.16 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| BTCUSDT | 12h | both | fixed_pct | 1.4871 | 0.6989 | 45 | -27.55 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| ALGOUSDT | 1h | long | embedded | 1.4859 | 0.0433 | 83 | -66.06 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| SANDUSDT | 12h | long | fixed_pct | 1.463 | 0.8775 | 29 | -21.6 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| SANDUSDT | 15m | long | embedded | 1.4579 | -0.3172 | 200 | -86.15 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| FETUSDT | 15m | long | embedded | 1.4446 | 0.2799 | 123 | -88.14 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| CHZUSDT | 12h | long | embedded | 1.3921 | 0.4921 | 8 | -53.02 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BTCUSDT | 15m | long | fixed_signal | 1.372 | 0.6019 | 99 | -46.8 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| DOTUSDT | 12h | short | atr | 1.3612 | 1.5862 | 19 | -22.47 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| SANDUSDT | 12h | both | embedded | 1.3552 | 1.369 | 17 | -46.24 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 1h | both | fixed_pct | 1.3297 | -0.0627 | 283 | -63.29 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| SHIBUSDT | 12h | short | atr | 1.3287 | 1.4098 | 11 | -42.13 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| APTUSDT | 12h | short | fixed_pct | 1.2894 | 1.4874 | 17 | -25.95 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| APTUSDT | 12h | short | fixed_signal | 1.2894 | 1.4874 | 17 | -25.95 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FILUSDT | 12h | short | atr | 1.2784 | 1.2569 | 16 | -43.24 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| NEARUSDT | 12h | long | atr | 1.2763 | 0.7787 | 18 | -32.16 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| LINKUSDT | 15m | long | embedded | 1.2753 | 0.6254 | 125 | -66.94 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ETHUSDT | 15m | long | embedded | 1.2733 | 0.5826 | 135 | -58.76 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| NEARUSDT | 1h | both | embedded | 1.2718 | 0.7531 | 117 | -51.12 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| MANAUSDT | 12h | both | embedded | 1.2615 | 1.2454 | 20 | -35.32 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| ADAUSDT | 1h | long | embedded | 1.2594 | 0.763 | 69 | -34.08 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| NEARUSDT | 12h | long | embedded | 1.2587 | 0.308 | 11 | -77.87 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| LTCUSDT | 15m | long | atr | 1.2496 | 0.2668 | 66 | -49.92 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| TAOUSDT | 12h | both | fixed_pct | 1.239 | 2.6595 | 15 | -10.68 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| TAOUSDT | 12h | both | fixed_signal | 1.239 | 2.6595 | 15 | -10.68 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AAVEUSDT | 15m | long | atr | 1.2389 | 0.7777 | 209 | -60.18 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| CHZUSDT | 15m | long | embedded | 1.2296 | 0.3255 | 163 | -69.49 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| BTCUSDT | 12h | long | fixed_pct | 1.2061 | 0.7343 | 16 | -18.97 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| BTCUSDT | 12h | long | fixed_signal | 1.2061 | 0.7343 | 16 | -18.97 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| BTCUSDT | 12h | both | fixed_signal | 1.2033 | 0.6989 | 46 | -27.55 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| BNBUSDT | 1h | long | atr | 1.2032 | 0.6187 | 100 | -32.15 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| OPUSDT | 1h | short | embedded | 1.1988 | -0.1387 | 47 | -79.91 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| SEIUSDT | 1h | long | embedded | 1.1907 | 1.7067 | 14 | -59.17 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| SANDUSDT | 12h | both | atr | 1.1905 | 1.6759 | 24 | -41.6 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| GMXUSDT | 1h | both | fixed_signal | 1.1884 | 2.1905 | 227 | -38.78 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| SUIUSDT | 12h | both | atr | 1.1818 | 2.0926 | 18 | -32.81 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| AVAXUSDT | 1h | both | embedded | 1.1772 | 0.6962 | 153 | -59.14 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ADAUSDT | 1h | long | atr | 1.1735 | 0.0698 | 27 | -80.79 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| DOTUSDT | 12h | both | fixed_signal | 1.1658 | 1.4775 | 30 | -21.41 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| SANDUSDT | 12h | long | embedded | 1.159 | -0.2583 | 13 | -68.32 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| RUNEUSDT | 15m | long | embedded | 1.146 | 2.2994 | 250 | -41.37 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| BTCUSDT | 15m | long | fixed_pct | 1.1417 | 0.6262 | 71 | -53.38 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| GMXUSDT | 12h | long | atr | 1.128 | 1.1727 | 22 | -20.27 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| FETUSDT | 1h | both | embedded | 1.1267 | -0.5953 | 180 | -96.57 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| ENAUSDT | 1h | long | fixed_pct | 1.1191 | 2.039 | 63 | -29.28 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| ATOMUSDT | 12h | both | embedded | 1.1148 | 0.4589 | 17 | -48.03 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| BNBUSDT | 15m | long | embedded | 1.1129 | 0.3918 | 172 | -44.23 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| NEARUSDT | 12h | both | embedded | 1.106 | 1.5371 | 18 | -52.65 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ETHUSDT | 1h | long | fixed_signal | 1.1053 | 1.1461 | 141 | -19.87 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| AVAXUSDT | 1h | both | fixed_pct | 1.0972 | 1.8538 | 234 | -45.05 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| FLOWUSDT | 12h | short | fixed_signal | 1.0815 | 2.0926 | 29 | -26.59 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 12h | long | fixed_pct | 1.0732 | 2.1545 | 17 | -18.18 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| TRXUSDT | 12h | long | fixed_signal | 1.0732 | 2.1089 | 17 | -18.18 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| DOGEUSDT | 15m | long | embedded | 1.0691 | 0.1164 | 260 | -57.72 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 1h | long | fixed_pct | 1.0682 | 1.3133 | 41 | -36.38 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| BTCUSDT | 1h | long | atr | 1.068 | 0.6382 | 33 | -52.2 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| TAOUSDT | 1h | both | fixed_signal | 1.0645 | 5.0648 | 75 | -20.01 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ATOMUSDT | 1h | short | fixed_pct | 1.06 | 1.2251 | 109 | -31.8 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| SHIBUSDT | 12h | short | fixed_pct | 1.0537 | 1.9329 | 13 | -14.03 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| SHIBUSDT | 12h | both | fixed_pct | 1.0456 | 1.679 | 32 | -22.77 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| DOGEUSDT | 12h | long | atr | 1.0438 | 0.971 | 14 | -30.48 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| BNBUSDT | 12h | long | fixed_signal | 1.0379 | 0.5973 | 12 | -18.22 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| FILUSDT | 12h | long | fixed_pct | 1.036 | 1.891 | 20 | -11.27 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| FILUSDT | 12h | long | fixed_signal | 1.036 | 1.891 | 20 | -11.27 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 15m | long | atr | 1.0348 | 1.0292 | 392 | -27.04 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| SUIUSDT | 1h | both | embedded | 1.0245 | 0.2718 | 76 | -62.21 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AVAXUSDT | 1h | short | fixed_signal | 1.0242 | 1.9273 | 106 | -33.17 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| BTCUSDT | 1h | long | fixed_pct | 1.0203 | 0.5172 | 63 | -49.19 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| FLOWUSDT | 12h | long | atr | 1.0172 | 0.5565 | 21 | -35.11 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| ALGOUSDT | 12h | both | embedded | 1.0126 | 1.0884 | 21 | -42.1 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| BCHUSDT | 12h | long | atr | 1.001 | 0.3565 | 21 | -45.07 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| SHIBUSDT | 1h | long | embedded | 0.9991 | 0.2234 | 37 | -65.51 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ATOMUSDT | 1h | both | embedded | 0.9984 | 0.0658 | 152 | -80.41 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| AVAXUSDT | 1h | both | fixed_signal | 0.9919 | 1.8827 | 235 | -47.13 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ATOMUSDT | 15m | both | fixed_signal | 0.9886 | -0.249 | 429 | -79.27 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ATOMUSDT | 15m | long | embedded | 0.9835 | 0.3582 | 148 | -70.21 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DOTUSDT | 1h | long | embedded | 0.9749 | 0.2071 | 92 | -56.93 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| AAVEUSDT | 15m | long | fixed_signal | 0.9646 | 1.0272 | 213 | -54.22 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| LTCUSDT | 1h | long | atr | 0.953 | 0.7144 | 27 | -56.55 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ARBUSDT | 1h | long | fixed_signal | 0.9416 | 0.3496 | 124 | -46.14 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 15m | long | embedded | 0.9356 | 0.5019 | 268 | -56.1 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| UNIUSDT | 15m | long | embedded | 0.9351 | 0.4124 | 230 | -65.99 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| FETUSDT | 15m | both | atr | 0.9316 | -1.3123 | 580 | -99.55 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AXSUSDT | 12h | both | embedded | 0.9313 | 0.6693 | 16 | -52.44 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| SHIBUSDT | 15m | long | embedded | 0.9253 | -0.1574 | 143 | -81.15 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| AVAXUSDT | 12h | both | embedded | 0.9152 | 1.6721 | 24 | -46.5 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| AAVEUSDT | 1h | both | atr | 0.9148 | 1.3492 | 234 | -46.77 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| AAVEUSDT | 1h | long | atr | 0.8944 | 0.5267 | 96 | -59.53 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BCHUSDT | 12h | both | fixed_pct | 0.8927 | 0.8054 | 39 | -39.62 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| UNIUSDT | 1h | long | atr | 0.8831 | 0.5225 | 119 | -60.85 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| TAOUSDT | 1h | both | fixed_pct | 0.8746 | 4.9218 | 75 | -20.01 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| CHZUSDT | 12h | long | fixed_pct | 0.869 | 1.7118 | 30 | -27.17 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| CHZUSDT | 12h | long | fixed_signal | 0.869 | 1.7118 | 30 | -27.17 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| ETHUSDT | 15m | long | fixed_signal | 0.8679 | 0.6021 | 123 | -53.74 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ALGOUSDT | 12h | both | fixed_pct | 0.8651 | 2.0428 | 38 | -19.28 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ALGOUSDT | 12h | both | fixed_signal | 0.8651 | 2.0428 | 38 | -19.28 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| TRXUSDT | 15m | both | atr | 0.8587 | -0.7235 | 668 | -82.6 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| BCHUSDT | 1h | long | embedded | 0.8575 | 0.7816 | 64 | -50.14 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| MANAUSDT | 1h | long | embedded | 0.8448 | 0.3858 | 100 | -55.68 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AVAXUSDT | 15m | long | fixed_pct | 0.8435 | 0.7347 | 198 | -55.03 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| FLOWUSDT | 12h | short | atr | 0.8395 | 1.9314 | 16 | -33.69 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| SANDUSDT | 1h | long | embedded | 0.8275 | 0.3935 | 70 | -64.11 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| MANAUSDT | 12h | both | fixed_pct | 0.823 | 1.6484 | 41 | -26.46 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| MANAUSDT | 12h | both | fixed_signal | 0.823 | 1.6484 | 41 | -26.46 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DASHUSDT | 12h | both | embedded | 0.8157 | 0.7061 | 22 | -45.59 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| MANAUSDT | 12h | long | embedded | 0.8155 | 0.019 | 14 | -65.53 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| ETHUSDT | 1h | both | fixed_pct | 0.8109 | 0.5011 | 379 | -50.55 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BCHUSDT | 12h | long | embedded | 0.7963 | 0.3902 | 15 | -57.11 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ARBUSDT | 1h | long | embedded | 0.7907 | 0.7801 | 69 | -47.14 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 12h | both | embedded | 0.7665 | 0.4283 | 28 | -37.56 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| LTCUSDT | 12h | long | atr | 0.7645 | 1.0261 | 22 | -30.92 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| CHZUSDT | 12h | both | embedded | 0.7636 | 1.3792 | 20 | -53.94 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| LINKUSDT | 1h | short | fixed_pct | 0.7549 | 0.602 | 137 | -39.21 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| ETHUSDT | 1h | long | embedded | 0.7543 | 1.1796 | 171 | -35.57 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BCHUSDT | 12h | both | fixed_signal | 0.7536 | 0.8589 | 39 | -31.94 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| FETUSDT | 1h | both | atr | 0.7473 | -0.3398 | 230 | -91.96 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| AAVEUSDT | 12h | long | atr | 0.7452 | 0.4038 | 25 | -41.11 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| CHZUSDT | 1h | long | fixed_signal | 0.7392 | 0.6462 | 90 | -44.98 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| CHZUSDT | 1h | long | atr | 0.7296 | 1.0578 | 71 | -64.16 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ALGOUSDT | 12h | long | atr | 0.7267 | -0.2819 | 15 | -42.07 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| BNBUSDT | 15m | long | atr | 0.7246 | 0.1055 | 212 | -39.6 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| UNIUSDT | 12h | long | atr | 0.7183 | 0.703 | 11 | -26.95 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| AVAXUSDT | 1h | long | embedded | 0.7144 | 0.6278 | 68 | -54.52 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| CHZUSDT | 15m | long | fixed_pct | 0.7067 | 0.313 | 257 | -77.98 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| ATOMUSDT | 15m | short | fixed_pct | 0.7063 | 0.4955 | 210 | -82.22 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| TRXUSDT | 12h | long | atr | 0.6912 | 1.3007 | 20 | -35.02 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| GMXUSDT | 1h | long | fixed_signal | 0.683 | 1.7354 | 113 | -28.75 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| AVAXUSDT | 15m | long | fixed_signal | 0.6698 | 0.6811 | 212 | -53.32 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AVAXUSDT | 12h | long | atr | 0.6688 | 1.0025 | 18 | -36.8 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| CHZUSDT | 15m | long | fixed_signal | 0.6615 | 0.1271 | 281 | -75.84 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| SOLUSDT | 15m | long | atr | 0.6592 | 0.2966 | 96 | -84.67 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| SEIUSDT | 1h | long | fixed_pct | 0.6588 | 2.0224 | 62 | -19.8 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| FLOWUSDT | 12h | long | fixed_pct | 0.6437 | 0.6853 | 16 | -17.75 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ATOMUSDT | 1h | long | embedded | 0.6371 | 0.2506 | 33 | -64.67 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| SANDUSDT | 1h | both | embedded | 0.6326 | 0.585 | 190 | -57.92 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| LINKUSDT | 1h | short | fixed_signal | 0.6315 | 0.5075 | 81 | -38.4 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| CHZUSDT | 1h | long | fixed_pct | 0.6297 | 0.7953 | 88 | -42.09 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| DOTUSDT | 12h | long | fixed_signal | 0.6281 | 0.8387 | 15 | -23.4 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BCHUSDT | 1h | long | atr | 0.6223 | 0.2674 | 44 | -59.81 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| BTCUSDT | 12h | both | embedded | 0.6171 | 0.5263 | 43 | -36.15 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 1h | long | atr | 0.6112 | 1.0758 | 63 | -51.31 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AAVEUSDT | 15m | long | fixed_pct | 0.611 | 0.727 | 196 | -49.35 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| DOTUSDT | 15m | short | fixed_pct | 0.6038 | 0.6568 | 254 | -45.95 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BNBUSDT | 12h | long | atr | 0.6002 | 0.1267 | 11 | -24.79 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| AAVEUSDT | 1h | both | embedded | 0.594 | 1.2993 | 226 | -42.93 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| ADAUSDT | 15m | long | embedded | 0.5886 | 0.395 | 140 | -69.05 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DOTUSDT | 12h | long | fixed_pct | 0.5886 | 0.7576 | 15 | -24.57 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| ADAUSDT | 12h | long | embedded | 0.5753 | 0.2363 | 12 | -68.62 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| DYDXUSDT | 15m | long | fixed_signal | 0.5668 | 0.2309 | 340 | -71.87 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| DOGEUSDT | 1h | long | atr | 0.562 | 0.7116 | 162 | -40.51 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| DOTUSDT | 1h | short | fixed_pct | 0.5616 | 0.5692 | 146 | -50.03 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| FLOWUSDT | 15m | long | fixed_signal | 0.5604 | -0.2201 | 258 | -76.18 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| CHZUSDT | 12h | long | atr | 0.5512 | 1.4019 | 13 | -36.25 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| ETCUSDT | 1h | long | embedded | 0.5476 | 1.392 | 65 | -47.59 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| BTCUSDT | 15m | both | fixed_pct | 0.5406 | -0.2834 | 422 | -48.4 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| DOTUSDT | 15m | short | fixed_signal | 0.5106 | 0.425 | 286 | -51.15 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| SHIBUSDT | 1h | short | atr | 0.5092 | 0.5724 | 5 | -62.03 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| AVAXUSDT | 15m | both | embedded | 0.493 | 1.1376 | 387 | -58.81 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| BCHUSDT | 12h | long | fixed_pct | 0.4903 | 0.876 | 30 | -25.73 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| BCHUSDT | 12h | long | fixed_signal | 0.4903 | 0.876 | 30 | -25.73 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| FILUSDT | 12h | both | atr | 0.4867 | 1.6777 | 22 | -49.06 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| GMXUSDT | 15m | both | fixed_signal | 0.4838 | 2.3234 | 550 | -43.46 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| RUNEUSDT | 12h | long | atr | 0.4796 | 0.3723 | 15 | -69.3 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| SEIUSDT | 1h | long | fixed_signal | 0.4757 | 2.0224 | 62 | -19.8 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 12h | both | fixed_pct | 0.4755 | 1.117 | 22 | -19.5 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| TRXUSDT | 12h | both | fixed_signal | 0.4755 | 1.0472 | 22 | -19.5 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| APTUSDT | 15m | long | embedded | 0.4645 | 0.9468 | 217 | -58.53 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BCHUSDT | 12h | short | fixed_pct | 0.4634 | 0.6796 | 22 | -29.2 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| BCHUSDT | 12h | short | fixed_signal | 0.4634 | 0.7507 | 22 | -29.2 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AXSUSDT | 12h | long | embedded | 0.4567 | -0.6731 | 14 | -76.19 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| MANAUSDT | 15m | long | embedded | 0.4517 | -0.0533 | 304 | -70.85 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FETUSDT | 12h | both | fixed_pct | 0.4325 | 0.5208 | 30 | -32.61 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| FETUSDT | 12h | both | fixed_signal | 0.4325 | 0.5208 | 30 | -32.61 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ATOMUSDT | 1h | both | fixed_signal | 0.4223 | 0.2091 | 183 | -70.11 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| LINKUSDT | 12h | long | embedded | 0.4201 | 0.3239 | 12 | -76.36 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| MANAUSDT | 1h | both | atr | 0.4162 | 1.0919 | 288 | -63.51 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| DYDXUSDT | 1h | short | fixed_pct | 0.4046 | 0.2512 | 82 | -50.48 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| UNIUSDT | 15m | long | atr | 0.393 | -0.0422 | 339 | -59.61 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| LINKUSDT | 12h | both | embedded | 0.3883 | 1.0345 | 25 | -58.82 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| FETUSDT | 1h | both | fixed_pct | 0.3745 | -0.2882 | 316 | -89.45 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| AXSUSDT | 15m | both | atr | 0.3707 | -0.621 | 534 | -93.91 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ETHUSDT | 12h | long | fixed_pct | 0.3699 | 0.7147 | 19 | -18.1 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ETHUSDT | 12h | long | fixed_signal | 0.3699 | 0.7147 | 19 | -18.1 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| DYDXUSDT | 12h | both | fixed_pct | 0.3676 | 0.5684 | 54 | -46.75 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| DYDXUSDT | 12h | both | fixed_signal | 0.3676 | 0.5684 | 54 | -46.75 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| ETCUSDT | 1h | long | fixed_pct | 0.3664 | 0.1891 | 98 | -54.33 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ETCUSDT | 12h | long | embedded | 0.3563 | 0.4083 | 13 | -58.26 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| MANAUSDT | 12h | long | fixed_pct | 0.3417 | 0.7044 | 28 | -16.39 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| MANAUSDT | 1h | long | fixed_pct | 0.3409 | 0.5655 | 130 | -49.27 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| ICPUSDT | 12h | both | embedded | 0.3337 | 1.0585 | 29 | -54.62 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| FLOWUSDT | 15m | both | fixed_pct | 0.3199 | -0.3596 | 582 | -90.67 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| SANDUSDT | 12h | both | fixed_pct | 0.3194 | 1.4386 | 40 | -17.63 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| SANDUSDT | 12h | both | fixed_signal | 0.3194 | 1.4386 | 40 | -17.63 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BCHUSDT | 15m | long | fixed_pct | 0.3159 | -0.1456 | 234 | -55.91 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DOTUSDT | 1h | both | embedded | 0.3127 | -0.042 | 189 | -79.43 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| ADAUSDT | 12h | long | atr | 0.3124 | 0.7361 | 17 | -37.2 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| ETHUSDT | 12h | long | embedded | 0.312 | 0.0234 | 13 | -51.67 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| SUIUSDT | 1h | both | atr | 0.3106 | 0.9259 | 127 | -51.37 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| OPUSDT | 12h | short | atr | 0.3087 | -0.4298 | 17 | -98.95 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ICPUSDT | 15m | long | embedded | 0.3078 | 0.4085 | 157 | -87.35 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| LINKUSDT | 1h | long | embedded | 0.3022 | 0.9884 | 103 | -49.15 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 12h | both | atr | 0.2934 | 0.959 | 34 | -34.11 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| ATOMUSDT | 1h | both | atr | 0.2863 | 0.4773 | 169 | -74.72 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| LINKUSDT | 12h | short | fixed_pct | 0.2822 | 1.3687 | 21 | -24.31 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| LINKUSDT | 12h | short | fixed_signal | 0.2822 | 1.3847 | 21 | -23.47 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| ICPUSDT | 15m | both | atr | 0.2821 | -0.2762 | 416 | -96.15 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ETCUSDT | 12h | long | fixed_pct | 0.2754 | 0.7275 | 18 | -48.29 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AXSUSDT | 1h | long | embedded | 0.2732 | 0.0287 | 94 | -64.31 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| SHIBUSDT | 15m | short | atr | 0.2653 | 0.8126 | 90 | -52.32 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ALGOUSDT | 12h | short | fixed_pct | 0.2617 | 1.7427 | 36 | -22.96 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| ETCUSDT | 1h | long | atr | 0.2599 | 0.5563 | 30 | -58.31 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| MANAUSDT | 1h | both | embedded | 0.259 | 0.9397 | 272 | -66.56 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 1h | short | embedded | 0.2552 | 1.0409 | 97 | -47.64 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| DOTUSDT | 12h | short | fixed_pct | 0.2497 | 1.3994 | 27 | -20.35 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| DOTUSDT | 12h | short | fixed_signal | 0.2497 | 1.3994 | 27 | -20.35 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ATOMUSDT | 15m | both | embedded | 0.2472 | -0.5677 | 412 | -88.49 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| SHIBUSDT | 12h | short | fixed_signal | 0.2439 | 2.0446 | 19 | -15.29 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| ICPUSDT | 1h | long | embedded | 0.2371 | 0.7183 | 34 | -76.84 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ICPUSDT | 12h | long | fixed_pct | 0.2341 | 1.4556 | 25 | -11.28 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| ICPUSDT | 12h | long | fixed_signal | 0.2341 | 1.4556 | 25 | -11.28 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| UNIUSDT | 1h | long | fixed_pct | 0.2325 | 0.0246 | 108 | -63.45 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| RUNEUSDT | 1h | short | embedded | 0.2323 | 0.9159 | 64 | -67.93 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| MANAUSDT | 12h | both | atr | 0.2257 | 1.2219 | 24 | -39.88 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DOTUSDT | 12h | both | atr | 0.2224 | 1.631 | 27 | -35.87 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FILUSDT | 1h | short | fixed_pct | 0.2122 | 1.282 | 168 | -51.18 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FILUSDT | 1h | short | fixed_signal | 0.2122 | 1.2191 | 168 | -51.18 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 15m | both | fixed_pct | 0.2097 | 1.2656 | 692 | -65.26 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| ARBUSDT | 15m | long | fixed_signal | 0.2065 | 0.04 | 132 | -40.55 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ATOMUSDT | 12h | both | fixed_signal | 0.1976 | 1.6016 | 31 | -26.56 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| UNIUSDT | 12h | both | atr | 0.1943 | 0.9335 | 17 | -52.27 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FLOWUSDT | 1h | long | atr | 0.1904 | 0.1991 | 111 | -36.26 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| APTUSDT | 1h | long | embedded | 0.1846 | 0.77 | 29 | -74.17 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BCHUSDT | 1h | long | fixed_pct | 0.181 | 0.0764 | 97 | -57.61 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| BNBUSDT | 15m | long | fixed_pct | 0.1628 | 0.3392 | 208 | -46.6 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| ATOMUSDT | 12h | long | embedded | 0.1613 | 0.3119 | 13 | -60.71 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| RUNEUSDT | 12h | long | embedded | 0.159 | 1.2073 | 14 | -68.32 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| CHZUSDT | 15m | long | atr | 0.142 | 0.5896 | 163 | -74.04 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| DYDXUSDT | 15m | short | atr | 0.1313 | -0.0228 | 132 | -92.14 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| FILUSDT | 1h | long | fixed_pct | 0.119 | 0.4688 | 152 | -47.71 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| CHZUSDT | 12h | both | fixed_pct | 0.1163 | 2.0434 | 44 | -32.97 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| CHZUSDT | 12h | both | fixed_signal | 0.1163 | 2.0434 | 44 | -32.97 | `{"rsi_period": 10, "momentum_threshold": 10.0, "adx_trend_confirm": 20, "adx_...` |
| FILUSDT | 15m | both | fixed_signal | 0.1151 | -0.6477 | 522 | -92.14 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ETCUSDT | 15m | long | embedded | 0.1115 | 0.8191 | 189 | -57.22 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| DYDXUSDT | 12h | short | atr | 0.1091 | 0.7568 | 21 | -43.89 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| ICPUSDT | 1h | both | atr | 0.1089 | 0.2463 | 234 | -76.15 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| ATOMUSDT | 12h | short | fixed_pct | 0.1002 | 1.6441 | 20 | -12.71 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| ATOMUSDT | 12h | both | atr | 0.0977 | 1.0392 | 24 | -47.02 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| SOLUSDT | 12h | both | atr | 0.0929 | 1.3698 | 26 | -42.1 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| FILUSDT | 1h | long | fixed_signal | 0.0929 | 0.4054 | 95 | -50.57 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| OPUSDT | 12h | short | fixed_pct | 0.0902 | 1.894 | 25 | -11.05 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| OPUSDT | 12h | short | fixed_signal | 0.0902 | 1.894 | 25 | -11.05 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 15, "adx_...` |
| BTCUSDT | 12h | short | atr | 0.0899 | 0.5327 | 13 | -21.04 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| BTCUSDT | 1h | long | fixed_signal | 0.0884 | 0.5778 | 80 | -35.33 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| DYDXUSDT | 12h | short | embedded | 0.0859 | -0.1946 | 10 | -81.9 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| GMXUSDT | 1h | long | atr | 0.0811 | 1.7063 | 117 | -27.76 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| GMXUSDT | 12h | both | fixed_signal | 0.0798 | 2.2971 | 22 | -20.38 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| BNBUSDT | 1h | long | embedded | 0.0783 | 0.9968 | 85 | -37.71 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| DOTUSDT | 15m | short | embedded | 0.0759 | 0.1897 | 155 | -70.24 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| SHIBUSDT | 15m | short | fixed_signal | 0.0758 | 0.6501 | 257 | -60.98 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| AXSUSDT | 1h | long | fixed_pct | 0.07 | 0.0244 | 148 | -63.8 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| AAVEUSDT | 1h | both | fixed_pct | 0.0699 | 0.7358 | 271 | -50.37 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| BTCUSDT | 1h | both | embedded | 0.0657 | 0.4605 | 141 | -33.75 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 25, "adx_e...` |
| DYDXUSDT | 1h | short | fixed_signal | 0.0636 | 0.2876 | 125 | -53.79 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 15, "adx_e...` |
| ALGOUSDT | 1h | short | atr | 0.0508 | 1.2719 | 112 | -59.9 | `{"rsi_period": 10, "momentum_threshold": 8.0, "adx_trend_confirm": 15, "adx_e...` |
| AAVEUSDT | 1h | both | fixed_signal | 0.0443 | 0.6271 | 271 | -50.03 | `{"rsi_period": 10, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| TRXUSDT | 1h | short | atr | 0.0421 | -0.1398 | 111 | -45.23 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 25, "adx_e...` |
| AXSUSDT | 1h | both | embedded | 0.0399 | 0.5385 | 209 | -87.76 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 20, "adx_e...` |
| RUNEUSDT | 15m | both | embedded | 0.0369 | 2.2644 | 838 | -40.83 | `{"rsi_period": 14, "momentum_threshold": 8.0, "adx_trend_confirm": 20, "adx_e...` |
| BNBUSDT | 1h | long | fixed_pct | 0.0344 | 0.2165 | 87 | -26.9 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| ICPUSDT | 1h | both | fixed_signal | 0.0272 | 0.1226 | 424 | -58.95 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| ICPUSDT | 1h | both | fixed_pct | 0.0234 | 0.0804 | 423 | -60.3 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 15, "adx_e...` |
| ETCUSDT | 12h | long | fixed_signal | 0.0224 | 0.7574 | 20 | -36.93 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| AVAXUSDT | 12h | long | embedded | 0.0205 | 0.423 | 17 | -76.79 | `{"rsi_period": 10, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |
| SUIUSDT | 15m | long | atr | 0.0187 | 0.2069 | 192 | -46.23 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| FLOWUSDT | 15m | long | atr | 0.0145 | -0.0364 | 214 | -78.07 | `{"rsi_period": 14, "momentum_threshold": 5.0, "adx_trend_confirm": 25, "adx_e...` |
| GMXUSDT | 15m | long | atr | 0.011 | 1.325 | 218 | -33.67 | `{"rsi_period": 14, "momentum_threshold": 10.0, "adx_trend_confirm": 25, "adx_...` |
| FLOWUSDT | 15m | long | fixed_pct | 0.0051 | -0.3477 | 197 | -90.35 | `{"rsi_period": 14, "momentum_threshold": 3.0, "adx_trend_confirm": 20, "adx_e...` |

**Stage 2 pass rate: 335 / 639**
