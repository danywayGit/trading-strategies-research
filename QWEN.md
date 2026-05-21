# QWEN.md — Trading Strategies Research

> This file serves as instructional context for Qwen Code sessions in this repository.

## Project Overview

This is a **research and documentation repository** (no executable code) acting as a central knowledge base for the development, validation, and backtesting of **trading strategies on Binance crypto futures (USDT-M perpetuals)**.

The repository connects three external systems:

| Step | Tool | Role |
|---|---|---|
| 1 | **TradingView** (sibling repo) | Signal design in Pine Script |
| 2 | **BacktestingMCP** (sibling repo) | GPU validation, parameter optimization |
| 3 | **Trading-WebHook-Bot** (sibling repo) | Live execution on Binance |
| 4 | **altfinsMCP** (sibling repo) | Trading ideas, signals, chart patterns |

## Structure

```
trading-strategies-research/
├── pinescript-fixes/       # Corrected Pine Script files (ready for TradingView)
│   └── BUGS.md             # Detailed report of critical bugs identified
├── backtest-descriptions/  # Strategy specifications in plain text (for BacktestingMCP)
├── results/                # Backtest outputs: CSV, metrics, parameter grids (to be filled)
└── ideas/                  # Raw ideas, notes, hypotheses
```

## Workflow

1. **Design** — Develop logic in Pine Script on TradingView (sources in `TradingView/`)
2. **Review & fix** — Correct syntax/logical bugs → corrected versions in `pinescript-fixes/`
3. **Specification** — Translate the strategy into a text spec in `backtest-descriptions/*.md`
4. **Backtest** — Launched via `BacktestingMCP` (Python, GPU/CuPy, Binance historical data)
5. **Results** — Store best parameters, equity curves, Sharpe, max drawdown in `results/`
6. **Deployment** — TradingView alerts → `Trading-WebHook-Bot` (Flask) executes on Binance Futures

## Strategies (19 total)

| ID | Name | Timeframe | Type |
|---|---|---|---|
| SWING1 | EMA Wave + Volume | 1H | Trend |
| SWING2 | BB Squeeze Breakout | 4H | Breakout |
| SWING3 | Supertrend + ADX | 1H–4H | Trend / Trail |
| SWING4 | MACD Divergence | 2H | Reversal |
| SWING5 | Keltner Breakout | 1H | Breakout |
| SWING6 | MTF EMA Stack | 30m entry / 4H bias | Trend |
| EMA_REJ_V1 | EMA200 Rejection v1 | 1H–4H | Counter-trend |
| EMA_REJ_V2 | EMA200 Rejection v2 | 1H–4H | Counter-trend (correction needed) |
| AGGR_PB | Aggressive Pullback | 1H–4H | Pullback (engulfing + EMA) |
| RR1 | Range Mean Reversion | 4H | Mean Reversion (RSI + BB + Stoch) |
| VP1 | Volume Profile Breakout | 1H | Breakout (POC + VAH/VAL) |
| VR1 | VWAP Mean Reversion | 1H | Counter-trend (VWAP Z-score) |
| A01 | Screener Signal Composite | 4H | Data-driven (altFINS SHORT_TERM_TREND) |
| MO1 | Cross-Asset Momentum Rotation | 4H | Rotation / Relative Momentum |
| DC1 | Donchian Channel + ATR | 4H | Breakout (Mini Turtle) |
| PT1 | BTC/ETH Pair Trading | 1H | Pair / Market-Neutral |
| AR1 | Adaptive Regime Switcher | 4H | Meta-Strategy (Regime-based) |
| EC1 | Event Catalyst Alpha | 1H–4H | Event-Driven (altFINS) |
| SFP1 | ICT Swing Failure Pattern | 1H HTF / 5m LTF | Reversal / Liquidity Sweep (SFP + FVG) |

Each strategy has:
- A spec file in `backtest-descriptions/`
- A corrected version (if applicable) in `pinescript-fixes/`

All target **Binance Futures USDT-M perpetuals**, in both directions (long AND short).

## Pine Script Conventions

- Files must start with `//@version=5` or `//@version=6` — no markdown or chat artifacts before this line
- Sizing always **risk-based** : `qty = (equity × risk_pct) / stop_distance`
- Use `strategy.exit(stop=..., limit=...)` with **absolute prices** — never `loss=` / `profit=` (those take point distances, not prices)
- v6 files (`ema_rejection_strategy*.pinescript`, `aggressive_pullback_strategy.pinescript`) are cleaner and serve as a style reference

## BacktestingMCP Specs

Files in `backtest-descriptions/` are designed to be passed to BacktestingMCP (AI generation or manual Python implementation). Each spec contains:

- Entry/exit logic in clear English with exact indicator parameters
- Position sizing formula
- Parameter grid for optimization runs
- Suggested symbols and notes on expected behavior

### Python Implementation for BacktestingMCP

- Subclass `BaseStrategy` from `src/core/backtesting_engine.py`
- Define parameters as class attributes (int/float/str/bool/list)
- Implement `init(self)` for indicators, `next(self)` for bar-by-bar logic
- Register in `src/strategies/templates.py` → `STRATEGY_REGISTRY`

## Known Historical Bugs

See `pinescript-fixes/BUGS.md` for the full report. Summary:

| Bug | Severity | Impact |
|---|---|---|
| BUG-001 | 🔴 Critical | `loss=`/`profit=` instead of `stop=`/`limit=` → SL/TP never trigger |
| BUG-002 | 🔴 Critical | Chat artifacts blocking compilation |
| BUG-003 | 🔴 Critical | `shortStayedBelow`/`longStayedAbove` conditions always false (EMA Rejection v2) |
| BUG-004 | 🟡 Visual | Incorrect static TP lines on SWING3 (no backtest impact) |

Corrected versions are located in `pinescript-fixes/*_fixed.pinescript`.

## Sibling Repos

| Repo | Role |
|---|---|
| `TradingView/` | Pine Script sources — indicators + strategies |
| `BacktestingMCP/` | Python backtesting engine (GPU/CuPy, MCP server, CLI) |
| `DownloadBinanceHistorycalData/` | OHLCV historical data warehouse |
| `Trading-WebHook-Bot/` | Flask webhook bot — receives alerts, executes on Binance |

> Do not modify these repos without explicit permission from the user.

## Naming Conventions

| Prefix | Type |
|---|---|
| `SWING1–SWING6` | Swing strategies (1H–4H) |
| `EMA_REJ_V1/V2` | EMA200 Rejection (counter-trend) |
| `AGGR_PB` | Aggressive Pullback |
| `RR1` | Range Mean Reversion |
| `VP1` | Volume Profile Breakout |
| `VR1` | VWAP Mean Reversion |
| `A01` | Screener Signal Composite (altFINS) |
| `MO1` | Cross-Asset Momentum Rotation |
| `DC1` | Donchian Channel Breakout |
| `PT1` | Pair Trading (Market-Neutral) |
| `AR1` | Adaptive Regime Switcher (Meta) |
| `EC1` | Event Catalyst Alpha (altFINS) |