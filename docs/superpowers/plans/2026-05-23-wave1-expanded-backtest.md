# Wave 1 Expanded Backtest Optimization — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run a 4-stage funnel optimization campaign for 7 strategies across 44 symbols × 4 timeframes × 3 directions × 3 SL types, track progress in BACKTEST-ROADMAP.md, and save results to `results/`.

**Architecture:** Funnel approach — Stage 1 runs each strategy at its home TF across all 44 symbols; only passing combos (≥30 trades, OOS Sharpe > 0) proceed to Stage 2 (off-TF expansion), then Stage 3 (DOW filter), then Stage 4 (summary + robustness). Each stage updates BACKTEST-ROADMAP.md immediately.

**Tech Stack:** Python · BacktestingMCP CLI (`python -m src.cli.main`) · Binance historical data (already in DB) · results/ markdown files for outputs

---

## Context

All commands run from: `C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP`

Activate venv first: `activate.bat` (Windows) or `source activate.sh`

CLI entry point: `python -m src.cli.main`

Results saved to: `C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\`

Roadmap file: `C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\BACKTEST-ROADMAP.md`

### Strategy Registry Keys

| Strategy | Registry Key |
|---|---|
| SWING2 | `swing2_bb_squeeze` |
| SWING3 | `swing3_supertrend_adx` |
| SWING4 | `swing4_macd_divergence` |
| SWING5 | `swing5_keltner_breakout` |
| EMA_REJ_V1 | `ema_rejection_v1` |
| DC1 | `dc1_donchian_channel` |
| RR1 | `rr1_range_mean_reversion` |

### Symbol Universe (44 coins)

```
TOP27: BTCUSDT ETHUSDT SOLUSDT HYPEUSDT SHIBUSDT NEARUSDT DOGEUSDT ONDOUSDT BNBUSDT
       SUIUSDT ADAUSDT TAOUSDT LINKUSDT TONUSDT BCHUSDT FILUSDT INJUSDT AVAXUSDT
       ENAUSDT UNIUSDT AAVEUSDT DOTUSDT ATOMUSDT LTCUSDT POLUSDT DASHUSDT TRXUSDT
MID8:  FETUSDT ICPUSDT RENDERUSDT CHZUSDT ARBUSDT APTUSDT ETCUSDT OPUSDT
SML9:  ALGOUSDT SANDUSDT MANAUSDT FLOWUSDT AXSUSDT GMXUSDT DYDXUSDT RUNEUSDT SEIUSDT
```

### SL Type Convention

Each strategy supports 3 SL variants passed via `--parameters` JSON:
- `"sl_type": "fixed"` → uses `stop_loss_pct` (BaseStrategy default, e.g. 2%)
- `"sl_type": "atr"` → uses `atr_stop_mult` (ATR-based distance)
- `"sl_type": "embedded"` → omit `sl_type` (strategy uses its own built-in SL logic)

### Pass Filter

A run passes Stage 1/2 if:
- `num_trades >= 30` over the full test window AND
- OOS `sharpe_ratio > 0` (from walk-forward with 70/30 split)

### Test Dates

- Full window: `--start 2022-01-01 --end 2024-12-31`
- Train split (70%): 2022-01-01 → 2024-01-10
- OOS split (30%): 2024-01-10 → 2024-12-31

---

## Pre-flight: Verify Data Availability

Before running any strategy, check that historical data exists for all 44 symbols at each required timeframe. Missing data must be downloaded first.

### Task 0: Data audit and download

**Files:**
- Read: BacktestingMCP CLI data commands
- Write: `results/data_audit.md`

- [ ] **Step 0.1: List available data in DB**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
activate.bat
python -m src.cli.main data list-data
```

Expected: table of symbol/timeframe/date-range pairs already stored.

- [ ] **Step 0.2: Download missing 1H data for all 44 symbols (2021-01-01 to 2024-12-31)**

Run for each symbol that lacks 1H data from 2021 onward. Example batch:

```bash
python -m src.cli.main data download --symbol BTC/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ETH/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol SOL/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol HYPE/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol SHIB/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol NEAR/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol DOGE/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ONDO/USDT --timeframe 1h --start 2022-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol BNB/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol SUI/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ADA/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol TAO/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol LINK/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol TON/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol BCH/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol FIL/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol INJ/USDT --timeframe 1h --start 2022-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol AVAX/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ENA/USDT --timeframe 1h --start 2024-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol UNI/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol AAVE/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol DOT/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ATOM/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol LTC/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol POL/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol DASH/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol TRX/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol FET/USDT --timeframe 1h --start 2022-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ICP/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol RENDER/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol CHZ/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ARB/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol APT/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ETC/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol OP/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol ALGO/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol SAND/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol MANA/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol FLOW/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol AXS/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol GMX/USDT --timeframe 1h --start 2022-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol DYDX/USDT --timeframe 1h --start 2022-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol RUNE/USDT --timeframe 1h --start 2021-01-01 --end 2024-12-31
python -m src.cli.main data download --symbol SEI/USDT --timeframe 1h --start 2023-01-01 --end 2024-12-31
```

Note: newer tokens (ENA, SUI, TAO, TON, ARB, APT, OP, RENDER, SEI) have limited history — shorten `--start` accordingly. If a symbol fails download, skip it and note in `results/data_audit.md`.

- [ ] **Step 0.3: Download 4H data for all 44 symbols**

Repeat Step 0.2 with `--timeframe 4h` for all 44 symbols.

- [ ] **Step 0.4: Download 15m data for all 44 symbols**

Repeat Step 0.2 with `--timeframe 15m` for all 44 symbols. Note: 15m data is large — start from 2022-01-01 at minimum.

- [ ] **Step 0.5: Download 12H data for all 44 symbols**

Repeat Step 0.2 with `--timeframe 12h` for all 44 symbols.

- [ ] **Step 0.6: Record which symbols have insufficient data**

Create `results/data_audit.md`:
```markdown
# Data Audit — 2026-05-23

## Available symbols per timeframe
| Symbol | 1H start | 4H start | 15m start | 12H start | Notes |
|---|---|---|---|---|---|
| BTCUSDT | 2021-01-01 | 2021-01-01 | 2022-01-01 | 2021-01-01 | |
| ... | | | | | |

## Symbols skipped (insufficient data)
- ENARUSDT: only from 2024-01 — <1 year, skip for Stage 1 window (2022-2024)
```

Any symbol with less than 6 months of data in the test window (2022-01-01 → 2024-12-31) is skipped for that timeframe.

- [ ] **Step 0.7: Commit data audit**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
git add results/data_audit.md
git commit -m "data: audit of available symbols and timeframes for Wave 1"
```

---

## Stage 1 — Home TF Optimization

### Task 1: SWING2 Stage 1 (4H, all 44 symbols)

**Files:**
- Write: `results/SWING2/stage1/` (one .json per passing combo)
- Write: `results/SWING2/stage1/SWING2_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md` (update SWING2 row)

The SWING2 embedded SL uses `atr_stop_mult` as a trailing ATR stop. The 3 variants are:
- `embedded`: default strategy behavior (ATR stop via `atr_stop_mult`)
- `atr`: override with tighter/looser `atr_stop_mult` range
- `fixed`: override with `stop_loss_pct` (BaseStrategy fallback)

For each of the 44 available symbols, run 3 direction × 3 SL variants = 9 optimize commands.

- [ ] **Step 1.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING2\stage1
```

- [ ] **Step 1.2: Run SWING2 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Expected output: best params + Sharpe/trades printed to stdout.

- [ ] **Step 1.3: Check trade count and run walk-forward for passing combos**

If `num_trades >= 30`, run walk-forward with the best params from Step 1.2:

```bash
python -m src.cli.main backtest walk-forward \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"direction":"both"}'
```

Replace parameter values with actual best params from Step 1.2.

Expected output: Train vs OOS metrics table with Verdict.

- [ ] **Step 1.4: Save result to JSON if passes filter**

If `num_trades >= 30` AND OOS Sharpe > 0, create:
`results/SWING2/stage1/BTCUSDT_4h_both_embedded.json`

```json
{
  "strategy": "swing2_bb_squeeze",
  "symbol": "BTCUSDT",
  "timeframe": "4h",
  "direction": "both",
  "sl_type": "embedded",
  "stage": 1,
  "test_window": "2022-01-01/2024-12-31",
  "best_params": {"bb_length": 20, "bb_mult": 2.0, "squeeze_bars": 5, "macd_fast": 12, "macd_slow": 26, "atr_stop_mult": 2.5, "rr_ratio": 2.5, "direction": "both"},
  "train_sharpe": 0.0,
  "oos_sharpe": 0.0,
  "num_trades": 0,
  "win_rate_pct": 0.0,
  "max_drawdown_pct": 0.0,
  "verdict": "PASS"
}
```

Fill actual values from CLI output. If it fails the filter, create the file with `"verdict": "FAIL"` and the reason.

- [ ] **Step 1.5: Repeat Steps 1.2–1.4 for BTCUSDT with direction=long and direction=short**

For `direction=long`:
```bash
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["long"]}' \
  --top-n 5
```

For `direction=short`:
```bash
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["short"]}' \
  --top-n 5
```

Save passing results as `BTCUSDT_4h_long_embedded.json` and `BTCUSDT_4h_short_embedded.json`.

- [ ] **Step 1.6: Run fixed % SL variant for BTCUSDT (all 3 directions)**

For fixed SL, add `stop_loss_pct` to the grid and exclude `atr_stop_mult` from the optimization (use default 2.5):

```bash
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"stop_loss_pct":[1.5,2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Save as `BTCUSDT_4h_both_fixed.json`. Repeat for `direction=long` and `direction=short`.

- [ ] **Step 1.7: Run ATR multiplier SL variant for BTCUSDT (all 3 directions)**

ATR variant uses a wider range of `atr_stop_mult`:

```bash
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[1.5,2.0,2.5,3.0,4.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Save as `BTCUSDT_4h_both_atr.json`. Repeat for `direction=long` and `direction=short`.

- [ ] **Step 1.8: Repeat Steps 1.2–1.7 for all remaining 43 symbols**

Work through the full symbol list in order. For each symbol: run 9 combos (3 dir × 3 SL), save JSON, mark ✅/❌ in BACKTEST-ROADMAP.md Stage 1 Detail table for SWING2.

- [ ] **Step 1.9: Write SWING2 Stage 1 summary**

Create `results/SWING2/stage1/SWING2_stage1_summary.md`:

```markdown
# SWING2 — Stage 1 Summary (4H, all 44 symbols)

**Date:** YYYY-MM-DD
**Pass filter:** num_trades ≥ 30 AND OOS Sharpe > 0
**Total combos run:** 396 (44 symbols × 3 dir × 3 SL)

## Pass/Fail Table

| Symbol | both/emb | both/atr | both/fixed | long/emb | long/atr | long/fixed | short/emb | short/atr | short/fixed |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | ✅/❌ | ... | ... | ... | ... | ... | ... | ... | ... |
| ETHUSDT | ... | | | | | | | | |
...

## Passing Combos (proceed to Stage 2)
| Symbol | Direction | SL Type | OOS Sharpe | Trades | Best Params |
|---|---|---|---|---|---|
| BTCUSDT | both | embedded | 0.82 | 45 | {"bb_length": 20, ...} |
...

## Stage 1 pass rate: X / 396
```

- [ ] **Step 1.10: Update BACKTEST-ROADMAP.md — SWING2 Stage 1 complete**

In the Stage Tracker table, update SWING2 row:
- Stage 1: `✅`
- S1 Pass: `X/396`

In the Stage 1 Detail — SWING2 table, fill each cell with ✅ (pass) or ❌ (fail).

- [ ] **Step 1.11: Commit SWING2 Stage 1 results**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
git add results/SWING2/ BACKTEST-ROADMAP.md
git commit -m "results: SWING2 Stage 1 complete — X/396 combos pass"
```

---

### Task 2: SWING3 Stage 1 (1H, all 44 symbols)

**Files:**
- Write: `results/SWING3/stage1/` (one .json per combo)
- Write: `results/SWING3/stage1/SWING3_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

SWING3 embedded SL = Supertrend trailing stop (inherent in strategy logic). The 3 SL variants:
- `embedded`: Supertrend trail (default)
- `atr`: override stop at entry with explicit `atr_stop_mult` distance, no trail
- `fixed`: override stop at entry with `stop_loss_pct`, no trail

- [ ] **Step 2.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage1
```

- [ ] **Step 2.2: Run SWING3 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy swing3_supertrend_adx \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"st_period":[7,10,14],"st_factor":[2.0,3.0,4.0],"adx_threshold":[20,25,30],"ema_filter":[50,100,200],"adx_period":[10,14],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 2.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy swing3_supertrend_adx \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"st_period":10,"st_factor":3.0,"adx_threshold":30,"ema_filter":50,"adx_period":14,"direction":"both"}'
```

Replace with actual best params from Step 2.2.

- [ ] **Step 2.4: Save result JSON**

Save to `results/SWING3/stage1/BTCUSDT_1h_both_embedded.json` with same schema as Task 1 Step 1.4.

- [ ] **Step 2.5: Run ATR SL variant for BTCUSDT (all 3 directions)**

For `atr` variant, add `atr_stop_mult` to grid (strategy will use it as stop distance at entry instead of Supertrend trail — requires strategy to accept `atr_stop_mult` override; if not supported natively, treat same as embedded with tighter/looser `st_factor`):

```bash
python -m src.cli.main backtest optimize \
  --strategy swing3_supertrend_adx \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"st_period":[7,10,14],"st_factor":[1.5,2.0,2.5,3.0,4.0],"adx_threshold":[20,25,30],"ema_filter":[50,100,200],"adx_period":[10,14],"direction":["both"]}' \
  --top-n 5
```

Note: For SWING3, the ATR SL variant tests a wider `st_factor` range (1.5–4.0) since `st_factor` controls the ATR multiplier in Supertrend. Save as `BTCUSDT_1h_both_atr.json`.

- [ ] **Step 2.6: Run fixed % SL variant for BTCUSDT (all 3 directions)**

```bash
python -m src.cli.main backtest optimize \
  --strategy swing3_supertrend_adx \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"st_period":[7,10,14],"st_factor":[2.0,3.0,4.0],"adx_threshold":[20,25,30],"ema_filter":[50,100,200],"stop_loss_pct":[1.5,2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Save as `BTCUSDT_1h_both_fixed.json`.

- [ ] **Step 2.7: Repeat Steps 2.2–2.6 for all remaining 43 symbols**

- [ ] **Step 2.8: Write SWING3 Stage 1 summary**

Create `results/SWING3/stage1/SWING3_stage1_summary.md` with same structure as SWING2 summary (Step 1.9).

- [ ] **Step 2.9: Update BACKTEST-ROADMAP.md — SWING3 Stage 1 complete**

- [ ] **Step 2.10: Commit SWING3 Stage 1 results**

```bash
git add results/SWING3/ BACKTEST-ROADMAP.md
git commit -m "results: SWING3 Stage 1 complete — X/396 combos pass"
```

---

### Task 3: SWING4 Stage 1 (4H, all 44 symbols)

**Files:**
- Write: `results/SWING4/stage1/`
- Write: `results/SWING4/stage1/SWING4_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

SWING4 embedded SL = `atr_stop_mult` at entry (fixed ATR stop, no trail).

- [ ] **Step 3.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING4\stage1
```

- [ ] **Step 3.2: Run SWING4 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy swing4_macd_divergence \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"macd_fast":[10,12],"macd_slow":[24,26],"macd_signal":[7,9],"rsi_period":[10,14],"divergence_lookback":[3,5,8,10],"rsi_long_max":[40,45,50],"rsi_short_min":[50,55,60],"atr_stop_mult":[1.5,2.0,2.5],"rr_ratio":[1.5,2.0,2.5],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 3.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy swing4_macd_divergence \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"macd_fast":12,"macd_slow":26,"macd_signal":9,"rsi_period":14,"divergence_lookback":5,"rsi_long_max":45,"rsi_short_min":55,"atr_stop_mult":2.0,"rr_ratio":2.0,"direction":"both"}'
```

Replace with actual best params.

- [ ] **Step 3.4: Save result JSON to `results/SWING4/stage1/BTCUSDT_4h_both_embedded.json`**

- [ ] **Step 3.5: Run fixed % SL variant (all 3 directions)**

```bash
python -m src.cli.main backtest optimize \
  --strategy swing4_macd_divergence \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"macd_fast":[10,12],"macd_slow":[24,26],"macd_signal":[7,9],"rsi_period":[10,14],"divergence_lookback":[3,5,8,10],"rsi_long_max":[40,45,50],"rsi_short_min":[50,55,60],"stop_loss_pct":[1.5,2.0,2.5,3.0],"rr_ratio":[1.5,2.0,2.5],"direction":["both"]}' \
  --top-n 5
```

Save as `BTCUSDT_4h_both_fixed.json`.

- [ ] **Step 3.6: Run ATR multiplier SL variant (all 3 directions)**

```bash
python -m src.cli.main backtest optimize \
  --strategy swing4_macd_divergence \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"macd_fast":[10,12],"macd_slow":[24,26],"macd_signal":[7,9],"rsi_period":[10,14],"divergence_lookback":[3,5,8,10],"rsi_long_max":[40,45,50],"rsi_short_min":[50,55,60],"atr_stop_mult":[1.0,1.5,2.0,2.5,3.0,4.0],"rr_ratio":[1.5,2.0,2.5],"direction":["both"]}' \
  --top-n 5
```

Save as `BTCUSDT_4h_both_atr.json`.

- [ ] **Step 3.7: Repeat Steps 3.2–3.6 for all remaining 43 symbols**

- [ ] **Step 3.8: Write SWING4 Stage 1 summary and update BACKTEST-ROADMAP.md**

- [ ] **Step 3.9: Commit**

```bash
git add results/SWING4/ BACKTEST-ROADMAP.md
git commit -m "results: SWING4 Stage 1 complete — X/396 combos pass"
```

---

### Task 4: SWING5 Stage 1 (1H, all 44 symbols)

**Files:**
- Write: `results/SWING5/stage1/`
- Write: `results/SWING5/stage1/SWING5_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

SWING5 embedded SL = `atr_stop_mult` at entry. Note: CCI filter is inactive per existing results — include CCI params in grid anyway to confirm.

- [ ] **Step 4.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING5\stage1
```

- [ ] **Step 4.2: Run SWING5 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy swing5_keltner_breakout \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"kc_length":[15,20,25],"kc_mult":[1.5,2.0,2.5],"cci_period":[14,20,28],"cci_long_min":[-100,-50,0],"cci_short_max":[0,50,100],"atr_stop_mult":[1.5,2.0,2.5],"rr_ratio":[2.0,3.0,4.0],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 4.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy swing5_keltner_breakout \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"kc_length":25,"kc_mult":2.0,"cci_period":20,"cci_long_min":-100,"cci_short_max":100,"atr_stop_mult":2.0,"rr_ratio":3.0,"direction":"both"}'
```

Replace with actual best params.

- [ ] **Step 4.4: Save result JSON to `results/SWING5/stage1/BTCUSDT_1h_both_embedded.json`**

- [ ] **Step 4.5: Run fixed % SL and ATR SL variants for BTCUSDT (all 3 directions)**

Fixed % variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy swing5_keltner_breakout \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"kc_length":[15,20,25],"kc_mult":[1.5,2.0,2.5],"cci_period":[14,20,28],"cci_long_min":[-100,-50,0],"cci_short_max":[0,50,100],"stop_loss_pct":[1.5,2.0,2.5,3.0],"rr_ratio":[2.0,3.0,4.0],"direction":["both"]}' \
  --top-n 5
```

ATR multiplier variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy swing5_keltner_breakout \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"kc_length":[15,20,25],"kc_mult":[1.5,2.0,2.5],"cci_period":[14,20,28],"cci_long_min":[-100,-50,0],"cci_short_max":[0,50,100],"atr_stop_mult":[1.0,1.5,2.0,2.5,3.0,4.0],"rr_ratio":[2.0,3.0,4.0],"direction":["both"]}' \
  --top-n 5
```

Repeat both for `direction=long` and `direction=short`. Save 9 JSON files per symbol.

- [ ] **Step 4.6: Repeat Steps 4.2–4.5 for all remaining 43 symbols**

- [ ] **Step 4.7: Write SWING5 Stage 1 summary and update BACKTEST-ROADMAP.md**

- [ ] **Step 4.8: Commit**

```bash
git add results/SWING5/ BACKTEST-ROADMAP.md
git commit -m "results: SWING5 Stage 1 complete — X/396 combos pass"
```

---

### Task 5: EMA_REJ_V1 Stage 1 (1H, all 44 symbols)

**Files:**
- Write: `results/EMA_REJ_V1/stage1/`
- Write: `results/EMA_REJ_V1/stage1/EMA_REJ_V1_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

EMA_REJ_V1 embedded SL = `stop_mult × ATR` at entry.

- [ ] **Step 5.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\EMA_REJ_V1\stage1
```

- [ ] **Step 5.2: Run EMA_REJ_V1 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy ema_rejection_v1 \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"ema200_length":[150,200,250],"rejection_lookback":[5,10,15],"rsi_period":[10,14],"rsi_ema_period":[7,9,14],"rsi_confirm_window":[2,3,5],"stop_mult":[2.0,3.0,4.0],"rr_ratio":[1.5,2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 5.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy ema_rejection_v1 \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"ema200_length":200,"rejection_lookback":10,"rsi_period":14,"rsi_ema_period":9,"rsi_confirm_window":3,"stop_mult":3.0,"rr_ratio":2.0,"direction":"both"}'
```

Replace with actual best params.

- [ ] **Step 5.4: Save result JSON to `results/EMA_REJ_V1/stage1/BTCUSDT_1h_both_embedded.json`**

- [ ] **Step 5.5: Run fixed % SL and ATR SL variants (all 3 directions)**

Fixed % variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy ema_rejection_v1 \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"ema200_length":[150,200,250],"rejection_lookback":[5,10,15],"rsi_period":[10,14],"rsi_ema_period":[7,9,14],"rsi_confirm_window":[2,3,5],"stop_loss_pct":[1.5,2.0,2.5,3.0],"rr_ratio":[1.5,2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

ATR multiplier variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy ema_rejection_v1 \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"ema200_length":[150,200,250],"rejection_lookback":[5,10,15],"rsi_period":[10,14],"rsi_ema_period":[7,9,14],"rsi_confirm_window":[2,3,5],"stop_mult":[1.0,1.5,2.0,2.5,3.0,4.0],"rr_ratio":[1.5,2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Repeat for `direction=long` and `direction=short`. Save 9 JSON files per symbol.

- [ ] **Step 5.6: Repeat Steps 5.2–5.5 for all remaining 43 symbols**

- [ ] **Step 5.7: Write EMA_REJ_V1 Stage 1 summary and update BACKTEST-ROADMAP.md**

- [ ] **Step 5.8: Commit**

```bash
git add results/EMA_REJ_V1/ BACKTEST-ROADMAP.md
git commit -m "results: EMA_REJ_V1 Stage 1 complete — X/396 combos pass"
```

---

### Task 6: DC1 Stage 1 (4H, all 44 symbols)

**Files:**
- Write: `results/DC1/stage1/`
- Write: `results/DC1/stage1/DC1_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

DC1 embedded SL = ATR trailing stop (Turtle-style `trail_atr_mult`). SL variants:
- `embedded`: trailing ATR stop (default DC1 behavior)
- `atr`: fixed ATR stop at entry (`sl_atr_mult` only, no trail)
- `fixed`: `stop_loss_pct` override

- [ ] **Step 6.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\DC1\stage1
```

- [ ] **Step 6.2: Run DC1 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy dc1_donchian_channel \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"donchian_length":[15,20,25,55],"adx_threshold":[20,25,30],"adx_exit":[15,20,25],"sl_atr_mult":[1.5,2.0,3.0],"trail_atr_mult":[1.5,2.0,2.5],"atr_period":[10,14,21],"vol_avg_period":[14,20,30],"vol_mult":[0.8,1.0,1.2],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 6.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy dc1_donchian_channel \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"donchian_length":20,"adx_threshold":25,"adx_exit":20,"sl_atr_mult":2.0,"trail_atr_mult":2.0,"atr_period":14,"vol_avg_period":20,"vol_mult":1.0,"direction":"both"}'
```

Replace with actual best params.

- [ ] **Step 6.4: Save result JSON to `results/DC1/stage1/BTCUSDT_4h_both_embedded.json`**

- [ ] **Step 6.5: Run fixed % and ATR variants for BTCUSDT (all 3 directions)**

Fixed % variant (disables trail, uses fixed stop):
```bash
python -m src.cli.main backtest optimize \
  --strategy dc1_donchian_channel \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"donchian_length":[15,20,25,55],"adx_threshold":[20,25,30],"adx_exit":[15,20,25],"stop_loss_pct":[1.5,2.0,2.5,3.0],"atr_period":[10,14,21],"vol_avg_period":[14,20,30],"vol_mult":[0.8,1.0,1.2],"direction":["both"]}' \
  --top-n 5
```

ATR multiplier variant (fixed entry stop, wider range):
```bash
python -m src.cli.main backtest optimize \
  --strategy dc1_donchian_channel \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"donchian_length":[15,20,25,55],"adx_threshold":[20,25,30],"adx_exit":[15,20,25],"sl_atr_mult":[1.0,1.5,2.0,2.5,3.0,4.0],"atr_period":[10,14,21],"vol_avg_period":[14,20,30],"vol_mult":[0.8,1.0,1.2],"direction":["both"]}' \
  --top-n 5
```

Repeat for `direction=long` and `direction=short`. Save 9 JSON files per symbol.

- [ ] **Step 6.6: Repeat Steps 6.2–6.5 for all remaining 43 symbols**

- [ ] **Step 6.7: Write DC1 Stage 1 summary and update BACKTEST-ROADMAP.md**

- [ ] **Step 6.8: Commit**

```bash
git add results/DC1/ BACKTEST-ROADMAP.md
git commit -m "results: DC1 Stage 1 complete — X/396 combos pass"
```

---

### Task 7: RR1 Stage 1 (4H, all 44 symbols)

**Files:**
- Write: `results/RR1/stage1/`
- Write: `results/RR1/stage1/RR1_stage1_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

RR1 embedded SL = `sl_buffer_atr` (ATR buffer below/above BB level at entry).

- [ ] **Step 7.1: Create results directory**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\RR1\stage1
```

- [ ] **Step 7.2: Run RR1 optimization — BTCUSDT, direction=both, SL=embedded**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\BacktestingMCP
python -m src.cli.main backtest optimize \
  --strategy rr1_range_mean_reversion \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"adx_threshold":[15,20,25],"adx_period":[10,14],"rsi_period":[10,14,21],"rsi_oversold":[25,30,35],"rsi_overbought":[65,70,75],"bb_length":[20,30,50],"bb_mult":[1.5,2.0,2.5],"stoch_k":[14,18,21],"stoch_d":[3,5],"sl_buffer_atr":[0.3,0.5,1.0],"direction":["both"]}' \
  --top-n 5
```

- [ ] **Step 7.3: Walk-forward on best params if num_trades ≥ 30**

```bash
python -m src.cli.main backtest walk-forward \
  --strategy rr1_range_mean_reversion \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"adx_threshold":20,"adx_period":14,"rsi_period":14,"rsi_oversold":30,"rsi_overbought":70,"bb_length":20,"bb_mult":2.0,"stoch_k":14,"stoch_d":3,"sl_buffer_atr":0.5,"direction":"both"}'
```

Replace with actual best params.

- [ ] **Step 7.4: Save result JSON to `results/RR1/stage1/BTCUSDT_4h_both_embedded.json`**

- [ ] **Step 7.5: Run fixed % and ATR variants for BTCUSDT (all 3 directions)**

Fixed % variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy rr1_range_mean_reversion \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"adx_threshold":[15,20,25],"adx_period":[10,14],"rsi_period":[10,14,21],"rsi_oversold":[25,30,35],"rsi_overbought":[65,70,75],"bb_length":[20,30,50],"bb_mult":[1.5,2.0,2.5],"stoch_k":[14,18,21],"stoch_d":[3,5],"stop_loss_pct":[1.5,2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

ATR multiplier variant:
```bash
python -m src.cli.main backtest optimize \
  --strategy rr1_range_mean_reversion \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"adx_threshold":[15,20,25],"adx_period":[10,14],"rsi_period":[10,14,21],"rsi_oversold":[25,30,35],"rsi_overbought":[65,70,75],"bb_length":[20,30,50],"bb_mult":[1.5,2.0,2.5],"stoch_k":[14,18,21],"stoch_d":[3,5],"sl_buffer_atr":[0.2,0.3,0.5,0.8,1.0,1.5],"direction":["both"]}' \
  --top-n 5
```

Repeat for `direction=long` and `direction=short`. Save 9 JSON files per symbol.

- [ ] **Step 7.6: Repeat Steps 7.2–7.5 for all remaining 43 symbols**

- [ ] **Step 7.7: Write RR1 Stage 1 summary and update BACKTEST-ROADMAP.md**

- [ ] **Step 7.8: Commit**

```bash
git add results/RR1/ BACKTEST-ROADMAP.md
git commit -m "results: RR1 Stage 1 complete — X/396 combos pass"
```

---

## Stage 2 — Off-TF Expansion

### Task 8: Stage 2 — All 7 strategies on remaining 3 timeframes

**Files:**
- Write: `results/{STRATEGY}/stage2/` (one .json per passing combo)
- Write: `results/{STRATEGY}/stage2/{STRATEGY}_stage2_summary.md`
- Modify: `BACKTEST-ROADMAP.md`

For each strategy, take every symbol that passed Stage 1 (from the stage1 summary PASS list). Run the same 3 dir × 3 SL optimization on the 3 timeframes NOT tested in Stage 1.

| Strategy | Home TF (done) | Off-TFs to test |
|---|---|---|
| SWING2 | 4H | 15m, 1H, 12H |
| SWING3 | 1H | 15m, 4H, 12H |
| SWING4 | 4H | 15m, 1H, 12H |
| SWING5 | 1H | 15m, 4H, 12H |
| EMA_REJ_V1 | 1H | 15m, 4H, 12H |
| DC1 | 4H | 15m, 1H, 12H |
| RR1 | 4H | 15m, 1H, 12H |

- [ ] **Step 8.1: Create stage2 directories for all 7 strategies**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING2\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING4\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING5\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\EMA_REJ_V1\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\DC1\stage2
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\RR1\stage2
```

- [ ] **Step 8.2: For each passing Stage 1 combo, run the strategy on each off-TF**

Example — SWING2 passed on BTCUSDT/both/embedded. Now test on 15m, 1H, 12H:

```bash
# 15m
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 15m \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5

# 1h
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 1h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5

# 12h
python -m src.cli.main backtest optimize \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 12h \
  --start 2022-01-01 --end 2024-12-31 \
  --objective sharpe_ratio \
  --param-grid '{"bb_length":[15,20,25],"bb_mult":[1.8,2.0,2.2],"squeeze_bars":[3,5,8],"macd_fast":[10,12],"macd_slow":[24,26],"atr_stop_mult":[2.0,2.5,3.0],"rr_ratio":[2.0,2.5,3.0],"direction":["both"]}' \
  --top-n 5
```

Follow same walk-forward → save JSON pattern as Stage 1. File naming: `{SYMBOL}_{TF}_{DIR}_{SL}.json`.

Repeat for all other strategies using their respective param grids (same grids as Stage 1, just different `--timeframe`).

- [ ] **Step 8.3: Write Stage 2 summary for each strategy**

Create `results/{STRATEGY}/stage2/{STRATEGY}_stage2_summary.md` with same structure as Stage 1 summary, plus a column for timeframe.

- [ ] **Step 8.4: Update BACKTEST-ROADMAP.md Stage 2 columns for all 7 strategies**

- [ ] **Step 8.5: Commit all Stage 2 results**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
git add results/ BACKTEST-ROADMAP.md
git commit -m "results: Stage 2 off-TF expansion complete for all 7 Wave 1 strategies"
```

---

## Stage 3 — DOW Filter

### Task 9: DOW mask analysis on Stage 2 winners

**Files:**
- Write: `results/{STRATEGY}/stage3/{SYMBOL}_{TF}_dow_analysis.md`
- Modify: `BACKTEST-ROADMAP.md`

For each passing Stage 2 combo, apply 8 DOW masks using `trading_days` parameter in BaseStrategy. The `trading_days` parameter accepts a list of integers (0=Monday, 1=Tuesday, ..., 6=Sunday).

- [ ] **Step 9.1: Create stage3 directories**

```bash
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING2\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING3\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING4\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\SWING5\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\EMA_REJ_V1\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\DC1\stage3
mkdir -p C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research\results\RR1\stage3
```

- [ ] **Step 9.2: For each passing Stage 2 combo, run 8 DOW mask backtests**

Example — SWING2 on BTCUSDT 4H both/embedded with best params `{"bb_length":20,...}`:

```bash
# ALL (baseline — no filter)
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[0,1,2,3,4,5,6]}'

# MON-FRI only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[0,1,2,3,4]}'

# SAT-SUN only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[5,6]}'

# MON only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze --symbol BTCUSDT --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[0]}'

# TUE only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze --symbol BTCUSDT --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[1]}'

# WED only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze --symbol BTCUSDT --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[2]}'

# THU only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze --symbol BTCUSDT --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[3]}'

# FRI only
python -m src.cli.main backtest run \
  --strategy swing2_bb_squeeze --symbol BTCUSDT --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 --direction both \
  --parameters '{"bb_length":20,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"trading_days":[4]}'
```

Record `sharpe_ratio` and `num_trades` from each run's output.

- [ ] **Step 9.3: Write DOW analysis file**

Create `results/SWING2/stage3/BTCUSDT_4h_dow_analysis.md`:

```markdown
# SWING2 — BTCUSDT 4H DOW Analysis

**Base params:** {"bb_length": 20, "bb_mult": 2.0, ...}
**Direction:** both · SL: embedded
**Pass threshold:** Sharpe > baseline × 1.05 AND trades ≥ 20

| DOW Mask | Sharpe | Trades | vs Baseline | Selected? |
|---|---|---|---|---|
| ALL (baseline) | 0.82 | 45 | — | — |
| MON-FRI | 0.75 | 38 | -8.5% | ❌ |
| SAT-SUN | 0.91 | 12 | +10.9% | ❌ too few trades |
| MON | 0.70 | 8 | -14.6% | ❌ |
| TUE | 0.88 | 9 | +7.3% | ❌ too few trades |
| WED | 0.85 | 9 | +3.6% | ❌ <5% improvement |
| THU | 0.79 | 9 | -3.7% | ❌ |
| FRI | 0.86 | 8 | +4.9% | ❌ <5% improvement |

**Winner:** ALL (no DOW filter — no mask beats baseline by >5% with ≥20 trades)
```

Fill with actual values. If a mask wins, note it as winner.

- [ ] **Step 9.4: Repeat Step 9.2–9.3 for all passing Stage 2 combos across all 7 strategies**

- [ ] **Step 9.5: Update BACKTEST-ROADMAP.md Stage 3 columns**

- [ ] **Step 9.6: Commit Stage 3 results**

```bash
git add results/ BACKTEST-ROADMAP.md
git commit -m "results: Stage 3 DOW filter analysis complete for all Wave 1 strategies"
```

---

## Stage 4 — Summary & Robustness

### Task 10: Write SUMMARY.md per strategy and robustness check

**Files:**
- Write: `results/{STRATEGY}/SUMMARY.md`
- Modify: `BACKTEST-ROADMAP.md`

- [ ] **Step 10.1: Write SUMMARY.md for each of the 7 strategies**

Create `results/{STRATEGY}/SUMMARY.md` with this structure (example for SWING2):

```markdown
# SWING2 — BB Squeeze Breakout · Wave 1 Summary

**Date:** YYYY-MM-DD
**Strategies tested:** 1 (swing2_bb_squeeze)
**Symbols tested:** 44
**Timeframes tested:** 4H (Stage 1), 15m / 1H / 12H (Stage 2)
**Total combos run:** Stage 1: 396, Stage 2: X × 3 TFs × 9 = Y

---

## Top 10 Passing Combos (by OOS Sharpe)

| Rank | Symbol | TF | Dir | SL | OOS Sharpe | Trades | Max DD% | Best Params | DOW Mask |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BTCUSDT | 4H | both | embedded | 0.92 | 52 | -4.1% | {"bb_length":20,...} | ALL |
...

---

## Robustness Check

For each top combo, nudge each parameter ±10% and check Sharpe degradation:

| Combo | Param nudged | Nudged value | OOS Sharpe | Δ vs base | Stable? |
|---|---|---|---|---|---|
| BTC/4H/both/embedded | bb_length 20→18 | 18 | 0.88 | -4.3% | ✅ |
| BTC/4H/both/embedded | bb_length 20→22 | 22 | 0.91 | -1.1% | ✅ |
| BTC/4H/both/embedded | rr_ratio 2.5→2.25 | 2.25 | 0.79 | -14.1% | ⚠️ sensitive |
...

**Sensitivity flags:** List params where Sharpe drops >20% on nudge — these are fragile.

---

## Deployment Candidates

Combos where ALL of these hold:
- OOS Sharpe > 0.5
- Trades ≥ 30
- Max DD < 15%
- No parameter is flagged as sensitive (Sharpe drop < 20% on ±10% nudge)

| Symbol | TF | Dir | SL | OOS Sharpe | Verdict |
|---|---|---|---|---|---|
| BTCUSDT | 4H | both | embedded | 0.92 | ✅ Deploy candidate |
...
```

- [ ] **Step 10.2: Run parameter sensitivity checks for all deployment candidates**

For each deployment candidate, run one backtest per parameter with ±10% nudge using `backtest run`:

Example — SWING2 BTCUSDT 4H both/embedded, nudging `bb_length` from 20 → 18:

```bash
python -m src.cli.main backtest walk-forward \
  --strategy swing2_bb_squeeze \
  --symbol BTCUSDT \
  --timeframe 4h \
  --start 2022-01-01 --end 2024-12-31 \
  --train-ratio 0.7 \
  --parameters '{"bb_length":18,"bb_mult":2.0,"squeeze_bars":5,"macd_fast":12,"macd_slow":26,"atr_stop_mult":2.5,"rr_ratio":2.5,"direction":"both"}'
```

Record OOS Sharpe from output. Repeat for each param, each direction of nudge.

- [ ] **Step 10.3: Update BACKTEST-ROADMAP.md Stage 4 column and Best Combos for all 7 strategies**

Set Stage 4 = ✅ and fill Best Combos with top 1-3 deployment candidates per strategy.

- [ ] **Step 10.4: Commit final summaries**

```bash
cd C:\Users\danyw\Documents\Git\DanywayGit\trading-strategies-research
git add results/ BACKTEST-ROADMAP.md
git commit -m "results: Wave 1 Stage 4 complete — summaries and robustness checks for all 7 strategies"
```

---

## Completion Gate

Wave 1 is complete when:
- [ ] All 7 strategies have `results/{STRATEGY}/SUMMARY.md`
- [ ] BACKTEST-ROADMAP.md shows ✅ for Stage 1–4 on all 7 rows
- [ ] At least 1 deployment candidate identified (or documented why none passed)
- [ ] All results committed to git

Next step: Begin Wave 2 (12 remaining strategies) following the same funnel. Update BACKTEST-ROADMAP.md Wave 2 section with strategy shortlisting based on Wave 1 findings.
