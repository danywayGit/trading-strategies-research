# Stage 2 — Off-TF Expansion Design Spec

**Date:** 2026-06-01
**Status:** Approved
**Scope:** Wave 1 · 10 strategies · 3 off-timeframes · OOS Sharpe ≥ 0.5 filter from Stage 1

---

## 1. Objective

Expand Stage 1 passing combos across 3 additional timeframes per strategy. Each off-TF runs a full parameter grid re-optimization — not a forward-application of Stage 1 best params. The goal is to find which symbol/direction/SL/TF combinations show robust edge beyond the home timeframe.

---

## 2. Scope

### Strategies included (10)

| Strategy | Home TF | Stage 1 passes | Advance to Stage 2 (Sharpe ≥ 0.5) | Stage 2 runs (×3 TFs) |
|---|---|---|---|---|
| VP1 | 1h | 326 | 243 | 729 |
| SWING5 | 1h | 321 | 203 | 609 |
| MO1 | 4h | 310 | 213 | 639 |
| SWING2 | 4h | 274 | 203 | 609 |
| SWING3 | 1h | 274 | 193 | 579 |
| DC1 | 4h | 263 | 180 | 540 |
| EMA_REJ_V1 | 1h | 237 | 163 | 489 |
| AGGR_PULLBACK | 4h | 159 | 99 | 297 |
| SWING4 | 4h | 130 | 68 | 204 |
| VR1 | 1h | 128 | 63 | 189 |
| **Total** | | **~2,212** | **~1,628** | **~4,884** |

### Strategies excluded from Stage 2

| Strategy | Reason |
|---|---|
| RR1 | Only 12 Stage 1 passes (10.3%), avg OOS Sharpe 0.30 — not worth expanding |
| SFP1 | Designed for 5m only — stays at home TF, no off-TF expansion |

---

## 3. Off-Timeframe Configuration

Stage 2 tests the 3 timeframes not used in Stage 1 for each strategy, drawn from the fixed set {15m, 1h, 4h, 12h}:

| Home TF | Off-TFs |
|---|---|
| 1h | 15m, 4h, 12h |
| 4h | 15m, 1h, 12h |

---

## 4. Stage 1 Filter

Only combos where `Stage 1 OOS Sharpe ≥ 0.5` advance to Stage 2. The Stage 1 pass filter (`OOS Sharpe > 0`) is too low a bar — combos at 0.1–0.2 are marginal and unlikely to generalize across timeframes.

The filter is applied by `stage2_utils.load_stage1_passing()` at the start of each script run, reading from `results/{STRATEGY}/stage1/*.json`.

---

## 5. Architecture — Approach C

10 per-strategy scripts sharing a common `stage2_utils.py` module. Strategy-specific signal logic (numba functions, indicator helpers, vectorbt portfolio construction) is copied verbatim from Stage 1 scripts — no refactoring.

### File structure

```
optimization/
├── wave1/                                        # existing Stage 1 scripts
└── wave2/                                        # NEW
    ├── stage2_utils.py
    ├── run_swing2_stage2_parallel_v2.py
    ├── run_swing3_stage2_parallel_v2.py
    ├── run_swing4_stage2_parallel_v2.py
    ├── run_swing5_stage2_parallel_v2.py
    ├── run_ema_rej_v1_stage2_parallel_v2.py
    ├── run_dc1_stage2_parallel_v2.py
    ├── run_vr1_stage2_parallel_v2.py
    ├── run_aggr_pullback_stage2_parallel_v2.py
    ├── run_mo1_stage2_parallel_v2.py
    ├── run_vp1_stage2_parallel_v2.py
    └── generate_stage2_summary.py

results/
├── {STRATEGY}/stage2/{SYMBOL}_{TF}_{DIR}_{SL}.json
└── stage2_summarized/{STRATEGY}_stage2_summary.md
```

---

## 6. `stage2_utils.py` Contract

### `OFF_TF_MAP`
```python
OFF_TF_MAP = {
    "1h": ["15m", "4h", "12h"],
    "4h": ["15m", "1h", "12h"],
}
```

### `load_stage1_passing(strategy_id, results_base, sharpe_threshold=0.5)`
Reads all `results/{STRATEGY}/stage1/*.json`, returns a `set` of `(symbol_usdt, direction, sl_type)` tuples where `oos_sharpe >= sharpe_threshold` and `verdict == "PASS"`.

### `run_stage2_parallel(strategy_id, home_tf, results_base, worker_fn, workers, skip_download)`
Main executor. Responsibilities:
1. Call `load_stage1_passing` to get filtered combos
2. Expand to `combos × off_tfs` task list: `(sym, tf, direction, sl_type)`
3. Skip tasks where output JSON already exists and has no error note (resume support)
4. Dispatch `worker_fn(sym, tf, direction, sl_type)` via `ProcessPoolExecutor`
5. Write each result JSON to `results/{STRATEGY}/stage2/{SYMBOL}_{TF}_{DIR}_{SL}.json`
6. Print per-task progress and final pass rate

---

## 7. Per-Strategy Script Structure

Each script provides:
- `STRATEGY_ID`, `HOME_TF`, `RESULTS_BASE` constants
- `TF_MAP` — maps TF string to `TimeFrame` enum: `{"15m": TimeFrame.M15, "1h": TimeFrame.H1, "4h": TimeFrame.H4, "12h": TimeFrame.H12}`
- `INDICATOR_PARAMS`, `SL_PARAM_GRID` — identical to Stage 1 script
- All numba / indicator / vectorbt functions — copied verbatim from Stage 1
- `_worker_v2(task)` — worker function with signature `(sym, tf, direction, sl_type)`
- `main()` — parses `--workers` / `--skip-download` args, calls `run_stage2_parallel`

The only differences from Stage 1 worker:
- Task unpacks `tf` from the tuple
- `engine.get_data(symbol_usdt, TF_MAP[tf], start, end)` uses the variable TF
- Result dict has `"stage": 2` and `"timeframe": tf`

---

## 8. Output Format

JSON structure per combo — identical to Stage 1, two fields differ:

```json
{
  "strategy": "swing3_supertrend_adx",
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "direction": "both",
  "sl_type": "atr",
  "stage": 2,
  "test_window": "2022-01-01/2024-12-31",
  "best_params": { ... },
  "train_sharpe": 1.42,
  "oos_sharpe": 0.87,
  "num_trades": 38,
  "win_rate_pct": 57.9,
  "max_drawdown_pct": -11.2,
  "verdict": "PASS",
  "note": "v2/vectorbt"
}
```

**Pass filter:** `num_trades ≥ 30 AND OOS Sharpe > 0` (same as Stage 1)

---

## 9. Summary Generator

`generate_stage2_summary.py` mirrors Stage 1's generator:
- Usage: `python generate_stage2_summary.py <STRATEGY_ID | ALL>`
- Reads `results/{STRATEGY}/stage2/*.json`
- Writes `results/stage2_summarized/{STRATEGY}_stage2_summary.md`
- Summary table includes a `TF` column (same symbol can appear across 3 off-TFs)

---

## 10. What Comes Next (Stage 3)

Stage 3 applies DOW (day-of-week) filters on top of Stage 2 passing combos. It is out of scope for this spec and will be designed separately after Stage 2 completes.
