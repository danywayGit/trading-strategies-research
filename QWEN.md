# QWEN.md — Trading Strategies Research

> Ce fichier sert de contexte instructionnel pour les sessions Qwen Code dans ce dépôt.

## Aperçu du projet

Ceci est un **dépôt de recherche et documentation** (pas de code exécutable) servant de base de connaissances centrale pour le développement, la validation et le backtesting de **stratégies de trading sur futures crypto Binance (USDT-M perpetuals)**.

Le dépôt relie trois systèmes externes :

| Étape | Outil | Rôle |
|---|---|---|
| 1 | **TradingView** (répo frère) | Conception des signaux en Pine Script |
| 2 | **BacktestingMCP** (répo frère) | Validation GPU, optimisation de paramètres |
| 3 | **Trading-WebHook-Bot** (répo frère) | Exécution live sur Binance |

## Structure

```
trading-strategies-research/
├── pinescript-fixes/       # Fichiers Pine Script corrigés (prêts pour TradingView)
│   └── BUGS.md             # Rapport détaillé des bugs critiques identifiés
├── backtest-descriptions/  # Spécifications de stratégies en texte clair (pour BacktestingMCP)
├── results/                # Sorties de backtest : CSV, métriques, grilles de paramètres (à remplir)
└── ideas/                  # Idées brutes, notes, hypothèses (vide actuellement)
```

## Workflow

1. **Design** — Développer la logique en Pine Script sur TradingView (sources dans `TradingView/`)
2. **Review & fix** — Corriger les bugs de syntaxe/logique → versions correctes dans `pinescript-fixes/`
3. **Spécification** — Traduire la stratégie en spec texte dans `backtest-descriptions/*.md`
4. **Backtest** — Lancé via `BacktestingMCP` (Python, GPU/CuPy, données Binance historiques)
5. **Résultats** — Stocker les meilleurs paramètres, courbes d'équité, Sharpe, max drawdown dans `results/`
6. **Déploiement** — Alerts TradingView → `Trading-WebHook-Bot` (Flask) exécute sur Binance Futures

## Stratégies (9 au total)

| ID | Nom | Timeframe | Type |
|---|---|---|---|
| SWING1 | EMA Wave + Volume | 1H | Trend |
| SWING2 | BB Squeeze Breakout | 4H | Breakout |
| SWING3 | Supertrend + ADX | 1H–4H | Trend / Trail |
| SWING4 | MACD Divergence | 2H | Reversal |
| SWING5 | Keltner Breakout | 1H | Breakout |
| SWING6 | MTF EMA Stack | 30m entry / 4H bias | Trend |
| EMA_REJ_V1 | EMA200 Rejection v1 | 1H–4H | Counter-trend |
| EMA_REJ_V2 | EMA200 Rejection v2 | 1H–4H | Counter-trend (correction nécessitée) |
| AGGR_PB | Aggressive Pullback | 1H–4H | Pullback (engulfing + EMA) |

Chaque stratégie possède :
- Un fichier spec dans `backtest-descriptions/`
- Une version corrigée (si applicable) dans `pinescript-fixes/`

Toutes ciblent **Binance Futures USDT-M perpetuals**, dans les deux sens (long ET short).

## Conventions Pine Script

- Les fichiers doivent commencer par `//@version=5` ou `//@version=6` — aucun artifact markdown ou chat avant cette ligne
- Sizing toujours **risk-based** : `qty = (equity × risk_pct) / stop_distance`
- Utiliser `strategy.exit(stop=..., limit=...)` avec **des prix absolus** — jamais `loss=` / `profit=` (ceux-ci prennent des distances en points, pas des prix)
- Les fichiers v6 (`ema_rejection_strategy*.pinescript`, `aggressive_pullback_strategy.pinescript`) sont plus propres et servent de référence de style

## Spécs BacktestingMCP

Les fichiers dans `backtest-descriptions/` sont conçus pour être passés à BacktestingMCP (génération IA ou implémentation manuelle en Python). Chaque spec contient :

- Logique d'entrée/sortie en anglais clair avec paramètres exacts des indicateurs
- Formule de position sizing
- Grille de paramètres pour les runs d'optimisation
- Symboles suggérés et notes sur le comportement attendu

### Implémentation Python pour BacktestingMCP

- Sous-classer `BaseStrategy` depuis `src/core/backtesting_engine.py`
- Définir les paramètres comme attributs de classe (int/float/str/bool/list)
- Implémenter `init(self)` pour les indicateurs, `next(self)` pour la logique bar-à-bar
- S'enregistrer dans `src/strategies/templates.py` → `STRATEGY_REGISTRY`

## Bugs historiques connus

Voir `pinescript-fixes/BUGS.md` pour le rapport complet. Résumé :

| Bug | Sévérité | Impact |
|---|---|---|
| BUG-001 | 🔴 Critique | `loss=`/`profit=` au lieu de `stop=`/`limit=` → SL/TP ne se déclenchent jamais |
| BUG-002 | 🔴 Critique | Artifacts de chat bloquant la compilation |
| BUG-003 | 🔴 Critique | Conditions `shortStayedBelow`/`longStayedAbove` toujours fausses (EMA Rejection v2) |
| BUG-004 | 🟡 Visuel | Lignes TP statiques incorrectes sur SWING3 (sans impact backtest) |

Les versions corrigées se trouvent dans `pinescript-fixes/*_fixed.pinescript`.

## Répos frères

| Repo | Rôle |
|---|---|
| `TradingView/` | Sources Pine Script — indicateurs + stratégies |
| `BacktestingMCP/` | Moteur de backtesting Python (GPU/CuPy, serveur MCP, CLI) |
| `DownloadBinanceHistorycalData/` | Entrepôt de données OHLCV historiques |
| `Trading-WebHook-Bot/` | Bot Flask webhook — reçoit les alerts, exécute sur Binance |

> Ne pas modifier ces répos sans permission explicite de l'utilisateur.

## Conventions de nomination

| Préfixe | Type |
|---|---|
| `SWING1–SWING6` | Stratégies swing (1H–4H) |
| `EMA_REJ_V1/V2` | Rejet EMA200 (counter-trend) |
| `AGGR_PB` | Pullback agressif |
