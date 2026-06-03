# Stage 4 — Summary & Robustness Design Spec

**Date:** 2026-06-03
**Status:** Approved
**Scope:** 10 strategies · 1,943 filtered Stage 3 combos · param sensitivity ±10% · SUMMARY.md + BACKTEST-ROADMAP.md

---

## 1. Objective

Complete the 4-stage optimization funnel by:
1. Running parameter sensitivity analysis on the strongest Stage 3 combos to identify which are robust (performance doesn't collapse when params are nudged ±10%)
2. Writing a `SUMMARY.md` per strategy ranking all analysed combos by Sharpe with robustness flags
3. Appending a Wave 1 results table to `BACKTEST-ROADMAP.md`

---

## 2. Input & Filter

**Source:** All `results/{STRATEGY}/stage3/*_dow.json` files (2,314 total combos across 10 strategies)

**Sensitivity filter:** `winner_sharpe >= 0.5` → **1,943 combos** advance to sensitivity analysis

**Strategies:** SWING2, SWING3, SWING4, SWING5, EMA_REJ_V1, DC1, VR1, AGGR_PULLBACK, MO1, VP1

---

## 3. Parameter Sensitivity Rules

For each filtered combo, each numeric param in `best_params` is nudged:

| Param type | Nudge up (×1.1) | Nudge down (×0.9) |
|---|---|---|
| Integer (e.g., `st_period`) | `max(1, round(value × 1.1))` | `max(1, round(value × 0.9))` |
| Float (e.g., `st_factor`) | `round(value × 1.1, 4)` | `round(value × 0.9, 4)` |
| String / bool / `"direction"` key | skip | skip |

**Robustness flag per param:**
```
sensitive = True  if  any nudge_sharpe < winner_sharpe × 0.8
```
(Sharpe drops >20% from winner. `None` sharpe — eval error — is treated as non-sensitive.)

**Combo-level robustness:**
```
robust = True  if  no individual param is sensitive
```

**DOW mask applied:** `winner_mask` from Stage 3 result — same mask the winner was selected under. Indicators are precomputed once per combo; only `best_params` changes per nudge.

**Estimated compute:** 1,943 combos × ~7 params × 2 nudges = ~27,202 evaluations (comparable to Stage 3)

---

## 4. Architecture — Approach A

Same pattern as wave2/wave3. `stage4_utils.py` owns shared logic; 10 thin per-strategy scripts own strategy-specific indicator + eval code.

### File structure

```
optimization/
├── wave2/    # Stage 2 scripts
├── wave3/    # Stage 3 scripts
└── wave4/    # NEW
    ├── stage4_utils.py
    ├── run_swing2_stage4_sensitivity.py
    ├── run_swing3_stage4_sensitivity.py
    ├── run_swing4_stage4_sensitivity.py
    ├── run_swing5_stage4_sensitivity.py
    ├── run_ema_rej_v1_stage4_sensitivity.py
    ├── run_dc1_stage4_sensitivity.py
    ├── run_vr1_stage4_sensitivity.py
    ├── run_aggr_pullback_stage4_sensitivity.py
    ├── run_mo1_stage4_sensitivity.py
    ├── run_vp1_stage4_sensitivity.py
    └── generate_stage4_summary.py

results/
├── {STRATEGY}/stage4/{SYMBOL}_{TF}_{DIR}_{SL}_sensitivity.json
├── {STRATEGY}/SUMMARY.md
└── BACKTEST-ROADMAP.md   (updated in-place)
```

---

## 5. `stage4_utils.py` Contract

### `load_stage3_passing(strategy_id, results_base, sharpe_threshold=0.5)`

Reads all `results/{STRATEGY}/stage3/*_dow.json`, returns list of dicts for combos where `winner_sharpe >= sharpe_threshold`:

```python
{
    "symbol":            str,   # e.g. "BTCUSDT"
    "timeframe":         str,   # e.g. "4h"
    "direction":         str,
    "sl_type":           str,
    "best_params":       dict,
    "winner_mask":       str,   # e.g. "MON-FRI"
    "winner_sharpe":     float,
    "winner_trades":     int,
    "stage2_oos_sharpe": float,
}
```

### `nudge_params(best_params, factor)`

Returns a copy of `best_params` with numeric values nudged by `factor`:
- Skip: any value that is a string or bool, any key named `"direction"`
- Integer values: `max(1, round(value * factor))`
- Float values: `round(value * factor, 4)`

### `run_sensitivity_parallel(strategy_id, results_base, worker_fn, backtesting_mcp, workers=None, skip_download=False)`

- Calls `load_stage3_passing` to get filtered combos
- Builds task dicts: `{sym, tf, direction, sl_type, best_params, winner_mask, winner_sharpe, winner_trades, stage2_oos_sharpe}`
- Skips tasks where output `*_sensitivity.json` already exists and has no error note
- Dispatches via `ProcessPoolExecutor` with `BrokenExecutor` retry
- Writes each result JSON to `results/{STRATEGY}/stage4/`
- Prints progress per task

---

## 6. Per-Strategy Sensitivity Script Structure

### What is copied from the Stage 3 counterpart (verbatim)

- All indicator computation functions
- `_eval_single_dow(close_s, le_base, lx, se_base, sx, atr, sl_type, best_params, dow_days, freq)` — unchanged
- `LIMITED_DATA`, `TF_MAP`, `TF_FREQ_MAP`, `VENV_SITE_PACKAGES`, `SYMBOLS`

### What is different from Stage 3

- Import: `from stage4_utils import run_sensitivity_parallel, nudge_params, load_stage3_passing, DOW_MASKS`
- New constant: `SENSITIVITY_FILTER = 0.5`
- `_worker_v2(task)` — new implementation (see below)
- `main()` — calls `run_sensitivity_parallel`

### `_worker_v2(task)` flow

```
1. Unpack task: sym, tf, direction, sl_type, best_params, winner_mask, winner_sharpe, ...
2. Load full 3-year data at TF, split 70/30, take OOS slice
3. Compute indicators ONCE on test_data → le_t, lx_t, se_t, sx_t, atr_t, close_s_t
4. Get dow_days = DOW_MASKS[winner_mask]
5. For each param_name, param_value in best_params.items():
     if not numeric or param_name == "direction": skip
     for factor in [1.1, 0.9]:
         nudged = nudge_params(best_params, factor)
         sharpe, trades = _eval_single_dow(
             close_s_t, le_t, lx_t, se_t, sx_t, atr_t,
             sl_type, nudged, dow_days=dow_days, freq=TF_FREQ_MAP[tf]
         )
         record sharpe and trades
     mark param as sensitive if any nudge drops sharpe < winner_sharpe * 0.8
6. robust = no param is sensitive
7. Return result dict
```

**Key efficiency:** Indicators are computed once per combo. All ~14 nudge evaluations share the same `le_t`, `se_t`, `atr_t` arrays — only `best_params` (the SL/TP values) changes per nudge. For indicator params (e.g., `st_period`), the signals `le_t`/`se_t` would technically change with the nudged indicator — however, the nudge is applied to `best_params` which is passed to `_eval_single_dow`. Since the signals are pre-computed from the original `best_params`, indicator param sensitivity reflects the SL/TP sensitivity only. This is a deliberate approximation: re-computing indicators for each nudge would require 14× more indicator work per combo and eliminate the pre-compute optimization. The sensitivity analysis therefore measures robustness of the SL/TP configuration, not full re-optimization sensitivity.

---

## 7. Sensitivity JSON Output

**Path:** `results/{STRATEGY}/stage4/{SYMBOL}_{TF}_{DIR}_{SL}_sensitivity.json`

```json
{
  "strategy": "swing3_supertrend_adx",
  "symbol": "AAVEUSDT",
  "timeframe": "15m",
  "direction": "long",
  "sl_type": "atr",
  "stage": 4,
  "best_params": {"st_period": 14, "st_factor": 2.0, "adx_threshold": 25, "ema_filter": 50,
                  "direction": "long", "atr_stop_mult": 3.5, "rr_ratio": 1.5},
  "winner_mask": "MON-FRI",
  "winner_sharpe": 0.5919,
  "winner_trades": 79,
  "stage2_oos_sharpe": 0.4586,
  "sensitivity": {
    "st_period":     {"up": {"sharpe": 0.54, "trades": 72},
                      "down": {"sharpe": 0.61, "trades": 85}, "sensitive": false},
    "atr_stop_mult": {"up": {"sharpe": 0.31, "trades": 79},
                      "down": {"sharpe": 0.67, "trades": 79}, "sensitive": true}
  },
  "robust": false,
  "note": "v2/vectorbt"
}
```

`robust: true` = no param nudge caused >20% Sharpe drop. These are the candidates to consider for live deployment.

---

## 8. `generate_stage4_summary.py`

**Usage:** `python generate_stage4_summary.py <STRATEGY_ID | ALL>`

### `results/{STRATEGY}/SUMMARY.md`

Per-strategy file, contains:
- Header: strategy, date, total combos analysed, count robust, % robust
- **Top Combos table** (all combos where sensitivity JSON exists, sorted by winner_sharpe desc):

| Symbol | Off-TF | Direction | SL | Winner Mask | Winner Sharpe | Stage2 Sharpe | Trades | Robust |
|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 4h | long | atr | MON-FRI | 1.82 | 0.91 | 34 | ✅ |

### `BACKTEST-ROADMAP.md` update

Appends a new section after the existing content (only if the section doesn't already exist — idempotent):

```markdown
---

## Wave 1 — Optimization Results (Stages 1–4)

**Generated:** YYYY-MM-DD  
**Strategies:** 10 · **Symbols:** 39 · **Test window:** 2022-01-01 → 2024-12-31

| Strategy | Home TF | S1 Pass | S2 Pass | S3 DOW Improved | S4 Robust | Best Combo |
|---|---|---|---|---|---|---|
| SWING3 | 1h | 274/468 | 195 | 42/195 | N/T | BTCUSDT 4h long atr MON-FRI Ŝ=1.82 |
```

(N = robust count, T = total sensitivity combos)

---

## 9. Important Design Note — Sensitivity Approximation

The sensitivity analysis pre-computes signals from the original `best_params` and only varies the SL/TP configuration per nudge. Nudging indicator params (e.g., `st_period`) does NOT re-compute new signals — the same `le_t`/`se_t` are used for all nudges. This is a deliberate approximation that trades accuracy for speed (14× faster per combo vs full re-computation). The result measures **SL/TP robustness** more than **indicator param robustness**. Future work (Stage 5 or Wave 2) could address full sensitivity with per-param re-computation.

---

## 10. What Comes After

Stage 4 completes Wave 1. After all 10 SUMMARY.md files are written:
- Review top robust combos per strategy for live deployment candidates
- Wave 2: apply the same 4-stage funnel to the remaining strategies (SWING1, SWING6, EMA_REJ_V2, etc.)
