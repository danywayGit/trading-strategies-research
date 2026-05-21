# SFP1 — ICT Swing Failure Pattern (SFP) with Multi-Session Filter

> Adapted from equities-style SFP to crypto 24/7 — selectable session timing (NY / London / Asian / Any). Targets BTC, ETH, BNB and top-tier coins on Binance USDT-M perpetual futures.

---
## Strategy Overview

This strategy identifies **Swing Failure Patterns (SFP)** — liquidity raids above/below higher time frame swing points that close back inside the range, signaling a stop hunt / liquidity sweep. Entries are taken on the lower time frame once a **Fair Value Gap (FVG)** forms in the reversal direction. The strategy is designed for **4 selectable window modes** to accommodate the 24/7 crypto market.

| Variable       | Value / Logic |
|---------------|--------------|
| **HTF**        | 1 Hour (1H) — for swing point detection & bias |
| **LTF**        | 5 Minute (5m) — for FVG entry execution |
| **Session modes** | `NY`, `London`, `Asian`, `Any` (user-selectable) |
| **Trigger**    | Price sweeps an HTF swing high/low, then closes back inside |
| **Entry**      | Price retraces into a 5m FVG in trade direction |
| **Stop Loss**  | Beyond candle-2 (middle candle) of the 5m FVG |
| **Take Profit**| Default 2.0 R:R, or next HTF liquidity level |
| **Target Symbols**| BTCUSDT, ETHUSDT, BNBUSDT (+ select majors — see grid below) |

---
## Step-by-Step Logic

### Step 1: Higher Time Frame (HTF) Setup — 1H chart

1. **Bias determination** — Scan the last `lookback_bars` (default 48) hourly bars:
   - **Bullish bias**: EMA(50) > EMA(200) on 1H, **OR** last `lookback_bars` high > last `lookback_bars` low (simple trend slope check)
   - **Bearish bias**: EMA(50) < EMA(200) on 1H, **OR** downward slope
   - **Neutral / no bias**: EMAs crossed, choppy — do **not** trade (wait for a clear bias)
   - *Alternative (no-EMA mode)*: skip bias filter entirely — take SFPs in **both** directions

2. **Swing point identification** — Mark significant swing highs and lows within the lookback period. A swing point is defined as:
   - **Swing Low**: A bar whose low is lower than the `swing_lookback` bars before it AND the `swing_lookback` bars after it
   - **Swing High**: A bar whose high is higher than the `swing_lookback` bars before it AND the `swing_lookback` bars after it
   - Recommended: filter out swing points whose high-low distance is < `swing_min_distance_atr` × ATR(14), to avoid micro-swings in noise

3. Only mark swing points **within the active session window** (see Step 2) or within the last N hourly bars before it (to ensure the liquidity pool is fresh).

### Step 2: Session Timing (4 Modes)

The strategy supports **4 modes** controlled by `session_mode` parameter:

| Mode     | Window (UTC) | Duration | Description |
|----------|-------------|----------|-------------|
| `NY`     | 14:30 – 20:00 | ~5.5 h | New York equity overlap — highest volatility window for crypto |
| `London` | 07:00 – 12:00 | 5 h     | European open overlap |
| `Asian`  | 01:00 – 09:00 | 8 h     | Asian session (Tokyo/Sydney) — lower vol, mean-reversion prone |
| `Any`    | 00:00 – 23:59 | 24 h    | No session filter — catch SFPs around the clock |

- Only consider SFP raids that occur **during or immediately after the session open** (within `session_buffer_minutes` bars of the session start).
- Rationale: The original strategy targets the NY equity open at 09:30 ET because that is when institutional algorithms execute stop-hunts. In crypto, the equivalent volatility spikes are at **NY open (14:30 UTC), London open (07:00 UTC)**, and **Asian session (01:00 UTC)**.
- `session_buffer_minutes` (default = 120): the number of minutes after session open during which SFPs are valid. This accounts for the fact that the liquidity raid may occur slightly after the opening bell.

### Step 3: Identify the Swing Failure Pattern (SFP)

On the **1H chart**, monitor price action relative to marked swing points:

**Long SFP (bullish sweep):**
1. Price wicks **below** a marked HTF swing low (`low < swing_low`)
2. The 1H candle **closes back above** that swing low (`close > swing_low`)
3. This forms a **doji / pin bar / engulfing** shape indicating rejection of the sweep level

**Short SFP (bearish sweep):**
1. Price wicks **above** a marked HTF swing high (`high > swing_high`)
2. The 1H candle **closes back below** that swing high (`close < swing_high`)

**Bias alignment filter:**
- If 1H bias is **bullish** → only take **long SFPs** (sweeps of swing lows)
- If 1H bias is **bearish** → only take **short SFPs** (sweeps of swing highs)
- If no bias filter → take SFPs in both directions

### Step 4: Lower Time Frame (LTF) Execution — 5m chart

Once an HTF SFP is confirmed (1H candle closed back inside the swing point):

1. Switch to the **5m chart**
2. Wait for a **Fair Value Gap (FVG)** to form in the direction of the trade:
   - **Long FVG**: A 3-candle pattern where candle[2].high < candle[0].low (gap between candle 0's low and candle 2's high)
   - **Short FVG**: A 3-candle pattern where candle[2].low > candle[0].high (gap between candle 0's high and candle 2's low)
3. Set a **limit order** at the FVG boundary:
   - Long: entry limit at the **top** of the FVG zone (candle[2].high)
   - Short: entry limit at the **bottom** of the FVG zone (candle[2].low)
4. If the FVG is not formed within `max_ltf_wait_bars` (default = 24 bars = 2 hours on 5m) from the SFP confirmation, **skip the trade**.

**FVG must be found within the session window.** If the FVG forms outside the session window, abort.

### Step 5: Risk Management and Exit

| Component | Logic |
|-----------|-------|
| **Position Sizing** | `quantity = (equity × risk_pct) / (entry_price − stop_price)` (for longs; absolute for shorts) |
| **Stop Loss** | Placed **beyond candle-2** (middle candle) of the 5m FVG that formed the entry zone. For longs: below candle-2 low; for shorts: above candle-2 high. Add `sl_buffer_atr` × ATR(14, 5m) as a buffer. |
| **Take Profit** | Default: 2.0 × risk distance from entry (2:1 R:R). Alternative targets (controlled by `tp_mode`): |
| TP Mode `fixed_rr` | Fixed R:R ratio (default 2.0) |
| TP Mode `htf_liquidity` | Target the next HTF swing high (for longs) or swing low (for shorts) on the 1H chart |
| TP Mode `partial` | 50% at 2:1 R:R, remaining 50% at next HTF liquidity level |
| **Same-day close** | If `close_at_session_end` = true, close all open positions at the end of the trading session window. This is relevant for the original prop firm rule (~4:00 PM ET = 21:00 UTC). On crypto, this is optional since positions can be held overnight — but the backtest grid should include it. |

---
## Indicators Used

| Indicator | Parameters | Timeframe | Role |
|-----------|-----------|-----------|------|
| EMA(50)   | length=50 | 1H | Bias determination (cross vs EMA200) |
| EMA(200)  | length=200 | 1H | Bias determination |
| ATR(14)   | length=14 | 1H  | Swing point minimum distance filter |
| ATR(14)   | length=14 | 5m | Stop-loss buffer |
| FVG       | 3-candle pattern | 5m | Entry zone identification |

**No RSI, MACD, Stochastic, BB, Supertrend, Keltner — pure price action + volume profile + session context.**

---
## Parameter Grid for Optimization

| Parameter | Recommended | Range | Step | Rationale |
|-----------|-----------|-------|------|-----------|
| `lookback_bars` | 48 | [24, 48, 72, 96] | 24 | How far back to scan for swings & bias |
| `swing_lookback` | 5 | [3, 5, 8, 10] | 2 | Zigzag-style pivot detection width |
| `swing_min_distance_atr` | 1.0 | [0.5, 1.0, 1.5, 2.0] | 0.5 | Filter micro-swings |
| `session_mode` | `NY` | [`NY`, `London`, `Asian`, `Any`] | — | Session timing filter |
| `session_buffer_minutes` | 120 | [60, 120, 180, 240] | 60 | Minutes after session open to accept SFP |
| `max_ltf_wait_bars` | 24 | [12, 24, 48, 96] | 12 | Max 5m bars to wait for FVG |
| `risk_pct` | 1.0 | [0.5, 1.0, 1.5, 2.0] | 0.5 | Risk per trade (% of equity) |
| `tp_mode` | `fixed_rr` | [`fixed_rr`, `htf_liquidity`, `partial`] | — | Take profit target logic |
| `rr_ratio` | 2.0 | [1.5, 2.0, 2.5, 3.0] | 0.5 | Fixed reward:r-risk multiple |
| `sl_buffer_atr` | 0.5 | [0.0, 0.3, 0.5, 1.0] | 0.1 | ATR buffer added to stop-loss |
| `use_bias_filter` | true | [true, false] | — | Whether to require EMA bias alignment |
| `close_at_session_end` | false | [true, false] | — | Auto-close at session end |

---
## Suggested Symbols

| Priority | Symbol | Rationale |
|----------|--------|-----------|
| **Must** | BTCUSDT | Highest liquidity, cleanest SFP signals |
| **Must** | ETHUSDT | Second most liquid, good SFP fidelity |
| **Must** | BNBUSDT | Binance native, strong SFP patterns |
| **Should** | SOLUSDT | High vol, clear swings |
| **Should** | XRPUSDT | Liquidity pool raids visible |
| **Should** | DOGEUSDT | Meme volatility can create sharp SFP |
| **Optional** | LINKUSDT, AVAXUSDT, ADAUSDT | Top-20 alts, backtest first |

---
## BacktestingMCP Implementation Notes

### LTF/HTF Data Alignment Challenge
This strategy requires **two timeframes simultaneously** (1H for HTF, 5m for LTF). In BacktestingMCP:

**Option A (Recommended):** Use a single 5m feed, and synthesize 1H bars by resampling every 12 bars:
- `ohlcv_5m` → rolling window of 12 bars → compute 1H open/high/low/close
- Swing points on synthesized 1H data
- FVG detection on native 5m data

**Option B:** Load 1H data separately and use timestamp alignment. More complex but cleaner.

### Swing Point Detection (Python pseudocode)

```python
def find_swing_lows(lows, lookback=5):
    """Find swing lows using pivot detection"""
    swing_lows = []
    for i in range(lookback, len(lows) - lookback):
        if all(lows[i] <= lows[i - lookback + j] for j in range(lookback)) and \
           all(lows[i] <= lows[i + j] for j in range(lookback)):
            swing_lows.append(i)
    return swing_lows

def find_swing_highs(highs, lookback=5):
    swing_highs = []
    for i in range(lookback, len(highs) - lookback):
        if all(highs[i] >= highs[i - lookback + j] for j in range(lookback)) and \
           all(highs[i] >= highs[i + j] for j in range(lookback)):
            swing_highs.append(i)
    return swing_highs
```

### FVG Detection (5m)

```python
def detect_fvg(longs, highs, lows):
    """Fair Value Gap — bullish (long_FVG)"""
    # Candle 0 low > Candle 2 high → gap between candle 2 high and candle 0 low
    if longs:
        return lows[0] > highs[2]
    else:
        return highs[0] < lows[2]

class FVGZone:
    def __init__(self, longs, highs, lows):
        if longs:
            self.zone_top = highs[2]      # entry limit for long
            self.zone_bottom = lows[0]
            self.candle2_low = lows[2]    # SL anchor for long
            self.candle2_high = highs[2]
        else:
            self.zone_top = highs[0]
            self.zone_bottom = lows[2]    # entry limit for short
            self.candle2_low = lows[2]
            self.candle2_high = highs[2]
```

### Session Window (UTC)

```python
SESSION_WINDOWS = {
    "NY":     (14, 30, 20, 0),    # 14:30 – 20:00 UTC
    "London": (7, 0, 12, 0),     # 07:00 – 12:00 UTC
    "Asian":  (1, 0, 9, 0),      # 01:00 – 09:00 UTC
    "Any":    (0, 0, 24, 0),     # 24 hours
}

def is_in_session(bar_utc_datetime, session_mode, buffer_minutes=120):
    if session_mode == "Any":
        return True
    start_hour, start_min, end_hour, end_min = SESSION_WINDOWS[session_mode]
    session_start = bar_utc_datetime.replace(hour=start_hour, minute=start_min, second=0, microsecond=0)
    session_window_starts = session_start + timedelta(minutes=buffer_minutes)
    session_end = bar_utc_datetime.replace(hour=end_hour, minute=end_min, second=0, microsecond=0)
    return session_start <= bar_utc_datetime <= min(session_window_starts, session_end)
```

---
## Expected Behavior & Notes

- **Win rate expectation**: ~40–55% (as with most SFP/Smart Money strategies — edge comes from R:R, not win rate)
- **Sharpe**: Expect improved Sharpe in `NY` mode due to higher volatility windows
- **Asian session**: Lower volatility → fewer setups, tighter SL, smaller R:R
- **`Any` mode**: Most setups, but also more false signals in chop — may require wider SL
- **Avoid major news events**: CPI, FOMC, halving events, Binance listing announcements — these can create one-sided moves without reversal (SFP failure risk)
- **Minimum volume filter**: Consider a `min_volume_usdt` parameter (e.g., 1H volume > $10M) to ensure the liquidity pool is meaningful
- **Backtest period**: Minimum 6 months (crypto market regime changes), ideally 1+ year
- **Fee impact**: Binance futures ~0.02% taker / 0.01% maker — must account for this in backtest. FVG entries are limit orders → maker fees.

---
## TradingView Pine Script Requirements (for live alerts)

- Dual TF detection (`request.security`) for 1H + 5m
- Alert conditions on SFP confirm
- Webhook to Trading-WebHook-Bot with JSON payload: `{ "symbol", "side", "entry_price", "stop_price", "take_profit" }`
- Must handle requotes and 24/7 data feed

---
## Edge Cases to Handle in Backtest

1. **Multiple swing points in close proximity** — only mark the **most significant** (furthest from current price or largest ATR-distance)
2. **SFP during extreme wick** — if the wick is > 3× the candle body, the SFP signal may be a true spike rather than a stop hunt; consider filtering by `wick_to_body_ratio`
3. **Back-to-back SFPs** — if an SFP is confirmed and then another occurs in the opposite direction within N bars, skip (whipsaw risk)
4. **FVG overlap** — if multiple FVGs form, use the **closest** one to the SFP confirmation

---
## Risk Summary

| Risk | Mitigation |
|------|-----------|
| SFP failure in strong trend (continuation, not reversal) | Bias filter (EMA cross); avoid SFPs against strong momentum |
| Wide wick = stop hunt depth | ATR buffer on SL; filter extreme wicks |
| FVG never forms | `max_ltf_wait_bars` hard timeout |
| Crypto gap risk (flash crash) | Use limit orders, not market; reduce size during low-liq alts |
| Session window stale in summer/winter | UTC-based, no DST issues |
