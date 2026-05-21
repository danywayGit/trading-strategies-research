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

## Current State (as of 2025-07-17)

| # | Strategy | Spec | Python Impl. | Engine Complexity | Est. Effort |
|---|---|-|-|-|-|
| 1 | **SWING1** — EMA Wave + Volume | ✅ | ✅ Done | Single-TF, standard indicators | — |
| 2 | **SWING2** — BB Squeeze Breakout | ✅ | ⬜ Todo | Single-TF, BB + KC bands | Low |
| 3 | **SWING3** — Supertrend + ADX | ✅ | ⬜ Todo | Single-TF, needs Supertrend indicator | Low |
| 4 | **SWING4** — MACD Divergence | ✅ | ⬜ Todo | Single-TF, divergence detection logic | Medium |
| 5 | **SWING5** — Keltner Breakout | ✅ | ⬜ Todo | Single-TF, KC bands | Low |
| 6 | **SWING6** — MTF EMA Stack | ✅ | ⬜ Todo | **Dual-TF** (30m entry, 4H bias) | Medium |
| 7 | **EMA_REJ_V1** — EMA200 Rejection | ✅ | ⬜ Todo | Single-TF, bounce detection | Low |
| 8 | **EMA_REJ_V2** — EMA200 Rejection v2 | 🔲 | 🔲 | Needs corrected Pine Script first | — |
| 9 | **AGGR_PB** — Aggressive Pullback | ✅ | ⬜ Todo | Single-TF, engulfing + EMA | Low |
| 10 | **RR1** — Range Mean Reversion | ✅ | ⬜ Todo | Single-TF, RSI+BB+Stoch | Low |
| 11 | **VP1** — Volume Profile Breakout | ✅ | ⬜ Todo | Single-TF, needs price-bin volume profile | **High** |
| 12 | **VR1** — VWAP Mean Reversion | ✅ | ⬜ Todo | Single-TF, daily-reset VWAP + bands | Medium |
| 13 | **A01** — Screener Signal Composite | ✅ | ⬜ Todo | Single-TF, **external API** (altFINS) | **High** |
| 14 | **MO1** — Cross-Asset Momentum Rotation | ✅ | ⬜ Todo | Multi-asset ranking, trailing stop | **High** |
| 15 | **DC1** — Donchian Channel + ATR | ✅ | ⬜ Todo | Single-TF, trailing stop logic | Low |
| 16 | **PT1** — BTC/ETH Pair Trading | ✅ | ⬜ Todo | **Dual-asset**, Z-score, 2-leg position | **High** |
| 17 | **AR1** — Adaptive Regime Switcher | ✅ | ⬜ Todo | **Meta-strategy**, needs SWING3+RR1 first | **High** |
| 18 | **EC1** — Event Catalyst Alpha | ✅ | ⬜ Todo | **External API** (altFINS calendar+news) | **High** |
| 19 | **SFP1** — Swing Failure Pattern | ✅ | ⬜ Todo | **Dual-TF** (1H swing + 5m FVG entry) | **High** |

**Summary:** 1 of 19 implemented · 17 have specs · 1 needs spec correction first

---

## Phased Implementation Plan

### Phase 1 — Quick Wins (Low complexity, single-TF, no external deps)

> **Target:** 6 strategies · ~4–6 hours total · Validates pipeline, no new engine features needed

| Order | Strategy | Why First | Key Implementation Notes |
|---|---|---|---|
| 1 | **SWING2** — BB Squeeze | BB + KC = simple indicators, straightforward breakout | BB squeeze = BB width < threshold; entries on close outside KC |
| 2 | **RR1** — Range Mean Reversion | RSI + BB + Stoch all in `ta`/`talib`, mean reversion is complementary alpha | Entry at lower BB + oversold RSI + Stoch cross; exit at VWAP/mid |
| 3 | **AGGR_PB** — Aggressive Pullback | Engulfing detection is candlestick pattern (simple) + EMA alignment | Need helper `is_engulfing()` or use `ta.trend.engulfing` |
| 4 | **EMA_REJ_V1** — EMA200 Rejection | Single-TF, bounces off EMA200 with reversal candle | Close bounces EMA200 + RSI divergence confirmation |
| 5 | **DC1** — Donchian Channel | Highest/lowest over N bars — trivial to compute | Trailing stop logic needs careful testing (`trail_atr_mult`) |
| 6 | **SWING3** — Supertrend + ADX | Supertrend only indicator not in `ta` yet, easy to code | Implement `_calculate_supertrend()` helper: ATR-based bands |

**Engine changes needed:** None — all fit current `BaseStrategy` + `BacktestingEngine`.

**Claude/Cursor prompt template** (copy-paste ready):
```
Implement strategy {ID} in BacktestingMCP.
Spec file: C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\backtest-descriptions\{spec_filename}.md
Existing example to mirror: C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\src\strategies\swing1_ema_wave_volume.py
Register in: C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP\src\strategies\templates.py → STRATEGY_REGISTRY
Rules: inherit BaseStrategy, use self.I() in init(), bar-by-bar in next(), risk-based sizing, absolute SL/TP prices.
```

---

### Phase 2 — Medium Complexity (Single-TF but non-trivial logic)

> **Target:** 3 strategies · ~4–8 hours · May need 1–2 engine helper additions

| Order | Strategy | Complexity Driver | Key Implementation Notes |
|---|---|---|---|
| 7 | **SWING4** — MACD Divergence | Divergence detection (price ↔ indicator mismatch) | Track recent swing highs/lows, compare price extremum vs MACD extremum sign mismatch |
| 8 | **VR1** — VWAP Mean Reversion | Daily-reset VWAP + band calculation | Need `_calculate_vwap()` with session reset (UTC midnight), `band_mult × stddev` for bands |
| 9 | **SWING6** — MTF EMA Stack | **Dual-TF**: load both 30m and 4H data | **Requires engine update:** `BacktestingEngine` must support loading a second timeframe. Bias filter on 4H, entries on 30m |

**Engine changes for SWING6 (Dual-TF):**
```python
# Current BacktestingEngine load_data() accepts one TimeFrame.
# Need: load_data_pair(primary_tf, secondary_tf) → returns (df_primary, df_secondary)
# or: add self.data_4h alongside self.data_30m in BaseStrategy
# Implementation approach: resample 1m→30m and 1m→4H from same base data
```

---

### Phase 3 — High Complexity / Engine Extensions

> **Target:** 6 strategies · ~12–20 hours · Each needs distinct engine work

| Order | Strategy | Engine Change Required | Key Implementation Notes |
|---|---|---|---|
| 10 | **VP1** — Volume Profile | Price-bin volume histogram (not a standard indicator) | Implement `_build_volume_profile(highs, lows, closes, volumes, bin_size)` → returns POC, VAH, VAL. Bin size = ATR/4 |
| 11 | **MO1** — Cross-Asset Rotation | Multi-asset data loading + ranking | **Requires:** Engine must load OHLCV for 5 assets simultaneously. Track per-asset position + trailing stop. Relative RSI vs BTC benchmark |
| 12 | **PT1** — BTC/ETH Pair Trading | **Two independent positions** (market-neutral) | **Major change:** `enter_long_position()` manages one asset. PT1 needs a `PairTradeManager` or override `PositionTracker` to track 2 legs. Z-score on price ratio. Equal notional sizing |
| 13 | **A01** — Screener Composite | **External API integration** (altFINS) | Mock the screener data for backtesting. Add `screener_data` attribute to engine or cache it as a CSV. Signal asset selection logic (scan top 20) |
| 14 | **EC1** — Event Catalyst | **External API** (altFINS calendar) + event timestamp alignment | Similar to A01: mock calendar events as timestamped CSV. Pre-event shrink, post-event directional entry. Needs event → bar alignment |
| 15 | **SFP1** — Swing Failure Pattern | **Dual-TF** (1H swing + 5m FVG) | Most complex dual-TF. 1H swing point detection → SFP flagged → switch to 5m for FVG entry. Session filter (4 modes). May need event-driven TF switching in engine |

**Engine changes summary for Phase 3:**

| Change | Strategies Affected | Priority |
|---|---|- |
| Multi-asset data loader | MO1 | 🔴 Required |
| Two-leg position tracker | PT1 | 🔴 Required |
| Dual-TF resampling (generic) | SWING6, SFP1 | 🟠 Helpful to do once generically |
| External data mock/cache layer | A01, EC1 | 🟠 Helpful — use CSV substitutes for backtest period |
| Volume profile histogram builder | VP1 | 🟡 Self-contained helper, no engine change |

---

### Phase 4 — Meta-Strategy & Dependencies

| Order | Strategy | Depends On | Notes |
|---|---|---|---|
| 16 | **AR1** — Adaptive Regime Switcher | SWING3 + RR1 | Can only be tested once both sub-strategies are implemented. Regime classifier (ADX thresholds) activates one sub-strategy. Must import and instantiate SWING3/RR1 classes internally |
| 17 | **EMA_REJ_V2** — EMA200 Rejection v2 | Corrected Pine Script | Current spec says "correction needed". Fix bugs in `pinescript-fixes/EMA_REJ_V2_fixed.pinescript` first, then translate to Python |

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
