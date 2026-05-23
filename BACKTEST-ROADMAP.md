# Backtesting Implementation Roadmap

> Structured plan for implementing all 19 strategies in BacktestingMCP. Designed to be picked up by any AI coding assistant (Claude Code, Cursor, Copilot Workspace, etc.) with clear per-task context.

---

## Status Legend

| Badge | Meaning |
|---|---|
| ✅ Done | Python strategy class exists in BacktestingMCP, registered in `STRATEGY_REGISTRY` |
| 🟡 In Progress | Spec file exists, implementation started |
| ⬜ Todo | Spec exists, not yet implemented in Python |
| 🔲 Spec Missing | No spec file yet — needs backtest description first |

---

## Current State (as of 2026-05-23)

| # | Strategy | Spec | Python Impl. | Engine Complexity | Est. Effort |
|---|---|-|-|-|-|
| 1 | **SWING1** — EMA Wave + Volume | ✅ | ✅ Done | Single-TF, standard indicators | — |
| 2 | **SWING2** — BB Squeeze Breakout | ✅ | ✅ Done | Single-TF, BB + KC bands | — |
| 3 | **SWING3** — Supertrend + ADX | ✅ | ✅ Done | Single-TF, Supertrend indicator | — |
| 4 | **SWING4** — MACD Divergence | ✅ | ✅ Done | Single-TF, divergence detection logic | — |
| 5 | **SWING5** — Keltner Breakout | ✅ | ✅ Done | Single-TF, KC bands | — |
| 6 | **SWING6** — MTF EMA Stack | ✅ | ✅ Done | Dual-TF (30m entry, 4H bias, scaled EMA) | — |
| 7 | **EMA_REJ_V1** — EMA200 Rejection | ✅ | ✅ Done | Single-TF, bounce detection | — |
| 8 | **EMA_REJ_V2** — EMA200 Rejection v2 | ✅ | ✅ Done | Single-TF, 3-phase rejection + RSI threshold | — |
| 9 | **AGGR_PB** — Aggressive Pullback | ✅ | ✅ Done | Single-TF, engulfing + EMA | — |
| 10 | **RR1** — Range Mean Reversion | ✅ | ✅ Done | Single-TF, RSI+BB+Stoch | — |
| 11 | **DC1** — Donchian Channel + ATR | ✅ | ✅ Done | Single-TF, trailing stop logic | — |
| 12 | **VR1** — VWAP Mean Reversion | ✅ | ✅ Done | Single-TF, daily-reset VWAP + bands | — |
| 13 | **VP1** — Volume Profile Breakout | ✅ | ✅ Done | Single-TF, price-bin volume profile | — |
| 14 | **A01** — Screener Signal Composite | ✅ | ✅ Done | Single-TF, screener mock CSV (altFINS proxy) | — |
| 15 | **MO1** — Cross-Asset Momentum Rotation | ✅ | ✅ Done | Relative RSI vs BTC benchmark from DB | — |
| 16 | **PT1** — BTC/ETH Pair Trading | ✅ | ✅ Done | Z-score on ratio, ETH close from DB, single-leg proxy | — |
| 17 | **AR1** — Adaptive Regime Switcher | ✅ | ✅ Done | Meta-strategy, routes to SWING3+RR1 | — |
| 18 | **EC1** — Event Catalyst Alpha | ✅ | ✅ Done | Event calendar mock CSV, pre/post-event logic | — |
| 19 | **SFP1** — Swing Failure Pattern | ✅ | ✅ Done | Dual-TF via 5m feed + synthesized 1H resampling | — |

**Summary:** 19 of 19 implemented · 19 have specs · 🎉 ALL STRATEGIES COMPLETE

---

## Phased Implementation Plan

### Phase 1 — Quick Wins ✅ COMPLETE

> All 8 single-TF strategies implemented and registered.

| Strategy | Registry Key | Notes |
|---|---|---|
| SWING1 | `swing1_ema_wave_volume` | Reference implementation |
| SWING2 | `swing2_bb_squeeze` | BB squeeze + MACD |
| SWING3 | `swing3_supertrend_adx` | Custom Supertrend helper |
| SWING5 | `swing5_keltner_breakout` | KC breakout + CCI |
| EMA_REJ_V1 | `ema_rejection_v1` | EMA200 rejection with HTF bias |
| AGGR_PB | `aggr_pullback` | 5-condition engulfing |
| RR1 | `rr1_range_mean_reversion` | Partial TP, ADX exit, Stoch |
| DC1 | `dc1_donchian_channel` | Turtle trailing stop, 10-bar exit channel |

---

### Phase 2 — Medium Complexity ✅ COMPLETE

> **Target:** 3 strategies · SWING4 + SWING6 + VR1 all done

| Order | Strategy | Status | Complexity Driver | Key Implementation Notes |
|---|---|---|---|---|
| 7 | **SWING4** — MACD Divergence | ✅ Done | Divergence detection | Swing high/low detection, MACD histogram comparison |
| 8 | **SWING6** — MTF EMA Stack | ✅ Done | Dual-TF bias | HTF bias via scaled EMA period (no resampling needed) |
| 9 | **VR1** — VWAP Mean Reversion | ✅ Done | Daily-reset VWAP + bands | `_vwap_all()` returns (5,N) array, vol exhaustion filter, reversal trigger |

---

### Phase 3 — High Complexity / Engine Extensions ✅ COMPLETE

> **Target:** 6 strategies · All implemented

| Order | Strategy | Engine Change Required | Key Implementation Notes |
|---|---|---|---|
| 10 | **VP1** — Volume Profile | ✅ Done | `_build_volume_profile()` called per-bar in `next()`, NumPy slice binning, POC/VAH/VAL |
| 11 | **MO1** — Cross-Asset Rotation | ✅ Done | BTC benchmark RSI loaded from DB in `init()`, aligned to primary feed index. Relative RSI ranking. |
| 12 | **PT1** — BTC/ETH Pair Trading | ✅ Done | ETH close loaded from DB, Z-score on ratio computed each bar. Single-leg proxy with notional sizing. |
| 13 | **A01** — Screener Composite | ✅ Done | Mock CSV auto-generated on first run (seeded random). Signal lookup per bar via pandas mask. |
| 14 | **EC1** — Event Catalyst | ✅ Done | 20-row events_mock.csv. Pre-event profit protection + post-event directional entry with wider ATR stop. |
| 15 | **SFP1** — Swing Failure Pattern | ✅ Done | 5m primary feed, synthesized 1H via `resample('1h')` forward-filled. Swing detection → SFP flag → FVG entry. Session filter (NY/London/Asian/Any). |
| 16 | **AR1** — Adaptive Regime Switcher | ✅ Done | Meta-strategy inlining SWING3+RR1 signal logic, ADX+EMA regime classifier, churn protection |

**Implementation approach for Phase 3:**

| Challenge | Solution Used |
|---|---|
| Multi-asset data | Secondary symbols loaded from DB in `init()`, aligned to primary feed index |
| Two-leg pair trade | Single-leg proxy (long side only); notional sizing approximates pair P&L |
| External API (A01/EC1) | Mock CSV files auto-generated or bundled; timestamp-aligned lookup per bar |
| Dual-TF (SFP1) | 5m primary feed; 1H synthesized via `resample('1h')` + forward-fill via `self.I()` |
| Volume profile | Per-bar O(n) NumPy slice binning in `next()` (not via `self.I()`) |

---

### Phase 4 — Meta-Strategy & Dependencies ✅ COMPLETE

| Order | Strategy | Status | Notes |
|---|---|---|---|
| 16 | **AR1** — Adaptive Regime Switcher | ✅ Done | SWING3 + RR1 inlined. Regime classifier (ADX thresholds) activates one sub-strategy. |
| 17 | **EMA_REJ_V2** — EMA200 Rejection v2 | ✅ Done | Pine Script BUG-003 fixed. Persistent bar counters for 3-phase rejection + RSI threshold filter |

---

### Phase 5 — Optimization Runs

Once a strategy is implemented, run parameter optimization:

```
Per strategy workflow:
1. Unit smoke test → single symbol, 2024 data, default params → verify entries exist
2. Baseline backtest → BTCUSDT 2023-2025, log Sharpe / max DD / net return
3. Parameter grid search → use strategy's spec file "Parameter Grid" section
4. Cross-symbol validation → test top 5 symbols, check consistency
5. Store results → results/{strategy_id}/best_params.json + equity.csv
```

---

## Task Files for External AI Assistants

Each task below is a self-contained prompt that any AI coding tool can pick up. Place these in individual `.md` files if you want to give them to different Claude/Cursor sessions.

### Task 1: Implement SWING2, RR1, AGGR_PB, EMA_REJ_V1, DC1

**Context files needed:**
- `C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\src\strategies\swing1_ema_wave_volume.py` (mirror this structure)
- `C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\src\core\backtesting_engine.py` (read BaseStrategy)
- `C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\src\strategies\templates.py` (add to STRATEGY_REGISTRY)
- 5 spec files in `backtest-descriptions/` (SWING2, RR1, AGGR_PB, EMA_REJ_V1, DC1)

**Deliverables:**
- 5 Python files in `BacktestingMCP/src/strategies/`
- 5 new entries in `STRATEGY_REGISTRY`
- Each strategy must pass a smoke test: `backtest -s BTCUSDT -t 4H -d 365 --strategy {id}` → produces output with ≥1 trade

---

### Task 2: Implement SWING3 (Supertrend) + SWING4 (MACD Divergence)

**Additional context:**
- SWING3 needs a `_calculate_supertrend()` helper (ATR-based directional bands, flip on crossover)
- SWING4 needs a `_detect_divergence(prices, macd_hist, lookback=20)` helper (find swing points, compare direction)

**Deliverables:**
- 2 Python strategy files
- 2 helper functions (can go in a shared `src/indicators/helpers.py` if useful)
- Register both in `STRATEGY_REGISTRY`

---

### Task 3: Add Dual-TF Support to Engine + Implement SWING6

**Scope:**
1. Add `load_secondary_timeframe()` to `BacktestingEngine`
2. Expose `self.data_secondary` in `BaseStrategy` (nullable)
3. Implement SWING6 using 30m primary + 4H bias filter

**Deliverables:**
- Engine changes in `backtesting_engine.py`
- 1 strategy file
- Register SWING6

---

### Task 4: Implement VP1 (Volume Profile) + VR1 (VWAP)

**Scope:**
1. `_build_volume_profile()` — bin price levels, find POC/VAH/VAL
2. `_calculate_vwap_daily_reset()` — VWAP with UTC-midnight session reset, ±bands

**Deliverables:**
- 2 strategy files
- 2 helper functions
- Register both

---

### Task 5: Multi-Asset Support + Implement MO1 + PT1

**This is the largest engine change. Split into two sub-tasks if needed.**

**5a: MO1 — Cross-Asset Momentum**
- Engine must accept a `symbols: List[str]` parameter
- Load OHLCV for all symbols in batch
- Strategy ranks by relative RSI vs BTC, selects top/bottom asset
- Single position at a time (rotate between assets)

**5b: PT1 — Pair Trading**
- Strategy manages 2 concurrent positions (long leg + short leg)
- Z-score on price ratio BTC/ETH
- Equal notional sizing per leg
- Combined P&L tracking for exit

**Deliverables:**
- Multi-asset data loading in engine
- 2 strategy files
- Registration for both

---

### Task 6: External Data Mock Layer + Implement A01 + EC1

**Scope:**
1. Create `src/data/external_mock.py` — loads screener/calendar CSV as pandas DataFrames
2. A01: query mock screener → filter by SHORT_TERM_TREND signal + VOLUME_RELATIVE
3. EC1: query mock calendar → event timestamp alignment → pre/post-event logic

**Deliverables:**
- Mock data loader
- 2 strategy files
- Registration for both
- Sample CSV files for backtesting period

---

### Task 7: Implement SFP1 (Most Complex Dual-TF)

**Scope:**
1. 1H swing point detection (N-bar lookback, high/low extremes)
2. SFP flag when LTF sweeps swing point and closes back inside
3. Drop to 5m timeframe → wait for FVG formation
4. Enter on FVG entry + session filter (4 modes)
5. SL beyond FVG candle-2, TP at 2R

**Deliverables:**
- 1 strategy file (heaviest in the set)
- May need to reuse dual-TF infrastructure from Task 3

---

### Task 8: Implement AR1 (Meta-Strategy)

**Depends on:** SWING3 + RR1 both working

**Scope:**
1. Import SWING3 and RR1 strategy classes
2. ADX regime classifier runs every 50 bars
3. Active sub-strategy's `next()` is called — others are dormant
4. Regime-change exit logic (close if profitable, hold if not)

**Deliverables:**
- 1 strategy file
- Registration

---

## GPU Budget Considerations

| Phase | Strategies | Grid Search Budget (each) | Est. GPU Time (RTX 4090 24GB) |
|---|---|-|--|
| Phase 1 | 6 single-TF | 50–200 parameter combos | ~30–60 min per strategy |
| Phase 2 | 3 (1 dual-TF) | same + SWING6 needs 2x data load | ~1 hour for SWING6 |
| Phase 3 | 6 (complex) | VP1/MO1/PT1 may need larger grids | ~2–4 hours each |
| **Total optimization** | | | **~20–40 hours GPU** |

> Run optimization asynchronously via `backtest optimize`. Consider running Phase 1+2 optimizations while Phase 3 is being coded to overlap GPU and CPU time.

---

## Results Tracking

Store outputs in: `C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\`

Per strategy subfolder structure:
```
results/
├── SWING1/
│   ├── baseline_report.json      # Default params run
│   ├── best_params.json          # Optimization winner
│   ├── equity_curve.csv          # Bar-by-bar equity
│   └── trades.csv               # All closed trades
├── SWING2/
└── ...
```

---

## Quick-Start Commands

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP

# Smoke test a strategy
python -m backtesting.main backtest -s BTCUSDT -t 4H -d 365 --strategy SWING1

# Run parameter optimization
python -m backtesting.main optimize -s BTCUSDT -t 4H -d 730 --strategy SWING2 --grid-file grid_swings2.json

# List registered strategies
python -m backtesting.main list-strategies
```

---

## Wave 1 — Expanded Multi-Symbol Optimization

> Started: 2026-05-23 · Scope: 7 strategies × 39 symbols × 4 TFs × 3 directions × 3 SL types · Funnel approach (4 stages)
> Data audit completed 2026-05-23 — 5 of 44 symbols excluded (no data in 2022-2024 test window): HYPEUSDT, ONDOUSDT, TONUSDT, POLUSDT, RENDERUSDT · ENA + TAO limited (~9 months) — included with caution, 15m excluded · See `results/data_audit.md`

### Progress Legend

| Badge | Meaning |
|---|---|
| ⬜ | Not started |
| 🔄 | In progress |
| ✅ | Complete — at least 1 passing symbol |
| ❌ | Complete — 0 symbols passed filter |

---

### Stage Tracker

| Strategy | Home TF | Stage 1 | S1 Pass | Stage 2 | S2 Pass | Stage 3 | Stage 4 | Best Combos |
|---|---|---|---|---|---|---|---|---|
| SWING2 | 4H | 🔄 | — | ⬜ | — | ⬜ | ⬜ | — |
| SWING3 | 1H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |
| SWING4 | 4H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |
| SWING5 | 1H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |
| EMA_REJ_V1 | 1H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |
| DC1 | 4H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |
| RR1 | 4H | ⬜ | — | ⬜ | — | ⬜ | ⬜ | — |

---

### Symbol Universe — Confirmed 39 active (data audit 2026-05-23)

Binance USDT-M perpetuals · ranked by 24h futures volume as of 2026-05-23 · stables/wrapped/synthetics excluded

**Active for all 4 TFs (37 symbols)**
`BTCUSDT` `ETHUSDT` `SOLUSDT` `SHIBUSDT` `NEARUSDT` `DOGEUSDT` `BNBUSDT` `SUIUSDT` `ADAUSDT` `LINKUSDT` `BCHUSDT` `FILUSDT` `INJUSDT` `AVAXUSDT` `UNIUSDT` `AAVEUSDT` `DOTUSDT` `ATOMUSDT` `LTCUSDT` `DASHUSDT` `TRXUSDT` `FETUSDT` `ICPUSDT` `CHZUSDT` `ARBUSDT` `APTUSDT` `ETCUSDT` `OPUSDT` `ALGOUSDT` `SANDUSDT` `MANAUSDT` `FLOWUSDT` `AXSUSDT` `GMXUSDT` `DYDXUSDT` `RUNEUSDT` `SEIUSDT`

**Active for 1H/4H/12H only — 15m excluded (2 symbols)**
`ENAUSDT` *(~9 months in window, Apr–Dec 2024)* · `TAOUSDT` *(~8.5 months in window, Apr–Dec 2024)*

**Excluded — no data in 2022-2024 test window (5 symbols)**
~~`HYPEUSDT`~~ *(starts 2025-05-30)* · ~~`ONDOUSDT`~~ *(starts 2025-04-11)* · ~~`TONUSDT`~~ *(only ~5 months)* · ~~`POLUSDT`~~ *(only ~3.5 months)* · ~~`RENDERUSDT`~~ *(only ~5 months)*

---

### Optimization Parameters

| Dimension | Values |
|---|---|
| Timeframes | 15m · 1H · 4H · 12H |
| Directions | Long only · Short only · Both |
| Stop-loss | Fixed % · ATR + multiplier · Embedded dynamic SL |
| Test window | 2022-01-01 → 2024-12-31 (3 years) |
| Walk-forward | 70% train / 30% OOS |
| Pass filter (S1/S2) | ≥30 trades AND OOS Sharpe > 0 |
| DOW masks (S3) | ALL · MON-FRI · SAT-SUN · MON · TUE · WED · THU · FRI |
| DOW pass rule | Best mask must beat ALL by >5% Sharpe with ≥20 trades |

---

### Stage 1 Detail — SWING2 (4H)

> Status: 🔄 In progress · 39 active symbols (5 excluded — see symbol universe above)

| Symbol | Long/Fixed% | Long/ATR | Long/Embedded | Short/Fixed% | Short/ATR | Short/Embedded | Both/Fixed% | Both/ATR | Both/Embedded |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SOLUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| HYPEUSDT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| SHIBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| NEARUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOGEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ONDOUSDT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| BNBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SUIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ADAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TAOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LINKUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TONUSDT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| BCHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FILUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| INJUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AVAXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ENAUSDT | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ | ⬜⚠️ |
| UNIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AAVEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DOTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ATOMUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| LTCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| POLUSDT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| DASHUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| TRXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FETUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ICPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RENDERUSDT | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| CHZUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ARBUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| APTUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ETCUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| OPUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| ALGOUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SANDUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| MANAUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| FLOWUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| AXSUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| GMXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| DYDXUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| RUNEUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |
| SEIUSDT | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ |

---

### Stage 1 Detail — SWING3 (1H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

### Stage 1 Detail — SWING4 (4H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

### Stage 1 Detail — SWING5 (1H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

### Stage 1 Detail — EMA_REJ_V1 (1H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

### Stage 1 Detail — DC1 (4H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

### Stage 1 Detail — RR1 (4H)

> Status: ⬜ Not started · 39 active symbols (5 excluded — see symbol universe above)

---

## Wave 2 — Placeholder

> To be started after Wave 1 Stage 4 is complete for all 7 strategies.

Strategies queued for Wave 2 (12 total):

| # | Strategy | Notes |
|---|---|---|
| 1 | SWING1 | Re-optimize with constrained RR — overfit at rr=4.0 |
| 2 | SWING6 | Dual-TF 30m/4H — not yet backtested |
| 3 | EMA_REJ_V2 | BUG-003 fixed — ready to run |
| 4 | AGGR_PB | Only 21 trades on ETH — needs multi-symbol to find fit |
| 5 | VP1 | Volume profile breakout — uncorrelated alpha |
| 6 | VR1 | VWAP mean reversion — 1H, daily reset |
| 7 | A01 | Screener composite — mock altFINS CSV |
| 8 | MO1 | Cross-asset momentum rotation |
| 9 | PT1 | BTC/ETH pair trading |
| 10 | AR1 | Adaptive regime switcher (meta-strategy) |
| 11 | EC1 | Event catalyst alpha |
| 12 | SFP1 | Swing failure pattern — dual-TF 1H+5m, most complex |

Wave 2 symbol universe and shortlisting will be revisited based on Wave 1 findings.
