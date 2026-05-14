# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **research and documentation repo** — no runnable code lives here. It is the central knowledge base for crypto futures trading strategy development, connecting TradingView (signal design) → BacktestingMCP (GPU validation) → Trading-WebHook-Bot (live execution).

There are no build commands, tests, or dependencies to install.

## Repo Structure

```
pinescript-fixes/       # Corrected Pine Script files ready to paste into TradingView
  BUGS.md               # Full bug report with explanations and code examples
backtest-descriptions/  # Strategy specs in plain English — fed to BacktestingMCP as prompts
results/                # Backtest output: CSVs, equity curves, parameter grids (populated over time)
ideas/                  # Raw hypotheses, notes, early-stage strategy ideas
```

## Workflow

1. **Design** in TradingView (Pine Script) — source files live in the `TradingView` repo
2. **Review & fix** bugs → corrected files go in `pinescript-fixes/`
3. **Translate** strategy logic to a `backtest-descriptions/*.md` spec
4. **Backtest** via `BacktestingMCP` (separate repo, GPU-accelerated, Binance historical data)
5. **Store results** in `results/` with symbol, timeframe, best params, Sharpe, max drawdown
6. **Deploy** winning strategies as TradingView alerts → `Trading-WebHook-Bot` executes on Binance Futures

## Sibling Repos (do not edit without permission)

| Repo | Role |
|------|------|
| `TradingView/` | Pine Script source — strategy indicators + strategies |
| `BacktestingMCP/` | Python backtesting engine (GPU/CuPy, MCP server, CLI) |
| `DownloadBinanceHistorycalData/` | Historical OHLCV data warehouse |
| `Trading-WebHook-Bot/` | Flask webhook bot — receives alerts, executes on Binance |

## Strategy Naming Convention

| Prefix | Type |
|--------|------|
| `SWING1–SWING6` | Swing strategies (1H–4H timeframes) |
| `EMA_REJ_V1/V2` | EMA200 rejection counter-trend |
| `AGGR_PB` | Aggressive pullback (engulfing + EMA) |

Each strategy has a matching file in `backtest-descriptions/` and (once fixed) in `pinescript-fixes/`.

## Pine Script Rules

- All strategies target **Binance Futures USDT-M perpetuals**, long and short
- Position sizing is always **risk-based**: `qty = (equity × risk_pct) / stop_distance`
- Use `strategy.exit(stop=..., limit=...)` with **absolute prices** — never `loss=` / `profit=` (those take point-distances, not prices)
- Files must start with `//@version=5` or `//@version=6` — no markdown or chat artifacts before that line
- v6 files (`ema_rejection_strategy*.pinescript`, `aggressive_pullback_strategy.pinescript`) are cleaner and serve as style references

## BacktestingMCP Integration

Strategies in `backtest-descriptions/` are plain-text specs designed to be passed to BacktestingMCP's AI strategy generation or implemented manually as Python classes.

Each spec includes:
- Entry/exit logic in plain English with exact indicator parameters
- Position sizing formula
- Parameter grid for optimization runs
- Suggested symbols and notes on expected behavior

When implementing a spec as a Python strategy for BacktestingMCP:
- Subclass `BaseStrategy` from `src/core/backtesting_engine.py`
- Define parameters as class attributes (int/float/str/bool/list)
- Implement `init(self)` for indicators, `next(self)` for bar logic
- Register in `src/strategies/templates.py` → `STRATEGY_REGISTRY`

## Known Bugs (Pine Script)

See `pinescript-fixes/BUGS.md` for full details. Critical issues:
- **BUG-001**: SWING1/2/4/5/6 use `loss=`/`profit=` instead of `stop=`/`limit=` → SL/TP never trigger
- **BUG-002**: SWING1/2/4/6 contain chat message artifacts that break compilation
- **BUG-003**: EMA Rejection v2 `shortStayedBelow`/`longStayedAbove` always evaluates false → zero trades

Fixed versions are in `pinescript-fixes/*_fixed.pinescript`.
