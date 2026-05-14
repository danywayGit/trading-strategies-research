# Trading Strategies Research

Central research repo for developing, validating, and backtesting crypto futures trading strategies.

## Structure

```
trading-strategies-research/
├── pinescript-fixes/       # Corrected Pine Script files (bugs fixed, ready for TradingView)
├── backtest-descriptions/  # Strategy specs in plain text — fed to BacktestingMCP
├── results/                # Backtest output: CSVs, metrics, parameter grids
└── ideas/                  # Raw strategy ideas, notes, hypotheses
```

## Workflow

1. **TradingView** → develop + visually validate strategy logic in Pine Script
2. **pinescript-fixes/** → fix syntax/logic bugs identified in review
3. **backtest-descriptions/** → translate strategy to plain-text spec for BacktestingMCP
4. **BacktestingMCP** → GPU-accelerated parameter optimization on Binance historical data
5. **results/** → store best parameters, equity curves, Sharpe, drawdown metrics
6. **Trading-WebHook-Bot** → deploy winning strategies as live alerts

## Strategies

| ID | Name | Timeframe | Type | Status |
|----|------|-----------|------|--------|
| SWING1 | EMA Wave + Volume | 1H | Trend | Ready to backtest |
| SWING2 | BB Squeeze Breakout | 4H | Breakout | Ready to backtest |
| SWING3 | Supertrend + ADX | 1H-4H | Trend / Trail | Ready to backtest |
| SWING4 | MACD Divergence | 2H | Reversal | Ready to backtest |
| SWING5 | Keltner Breakout | 1H | Breakout | Ready to backtest |
| SWING6 | MTF EMA Stack | 30m entry / 4H bias | Trend | Ready to backtest |
| EMA_REJ_V1 | EMA200 Rejection | 1H-4H | Counter-trend | Ready to backtest |
| EMA_REJ_V2 | EMA200 Rejection v2 | 1H-4H | Counter-trend | Fix needed (see pinescript-fixes) |
| AGGR_PB | Aggressive Pullback | 1H-4H | Pullback | Ready to backtest |

## Exchange Target

Binance Futures (USDT-M perpetuals)
