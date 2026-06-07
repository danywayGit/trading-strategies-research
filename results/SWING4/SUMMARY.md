# SWING4 — Summary (home TF: 4H)

**Date:** 2026-06-04
**Combos analysed:** 98
**Robust:** 63 / 98 (64.3%)
  _(Robust = no param nudge ±10% drops OOS Sharpe by >20%)_
  _(Note: sensitivity measures SL/TP params; indicator params use pre-computed signals per spec §9)_

---

## Top Combos

| Symbol | Off-TF | Direction | SL | Winner Mask | Winner Sharpe | Stage2 Sharpe | Trades | Robust |
|---|---|---|---|---|---|---|---|---|
| ENAUSDT | 1h | long | embedded | THU+FRI+SUN | 6.614063903859933 | 4.272 | 23 | ✅ |
| ENAUSDT | 1h | long | fixed_pct | MON+THU+FRI+SUN | 6.322942357290221 | 4.8262 | 28 | ✅ |
| ENAUSDT | 1h | long | fixed_signal | MON+THU+FRI+SUN | 6.322942357290221 | 4.8262 | 28 | ✅ |
| ENAUSDT | 15m | long | atr | TUE+WED+THU+FRI+SAT+SUN | 5.2732473976098095 | 4.8866 | 69 | ✅ |
| ENAUSDT | 1h | long | atr | THU+FRI+SUN | 4.465743971333842 | 3.1031 | 23 | ✅ |
| ENAUSDT | 15m | long | embedded | FRI+SUN | 4.441397754493645 | 2.7634 | 29 | ✅ |
| ENAUSDT | 1h | both | fixed_pct | MON+TUE+FRI+SAT+SUN | 4.004514128052518 | 3.1885 | 57 | ❌ |
| ENAUSDT | 1h | both | fixed_signal | MON+TUE+FRI+SAT+SUN | 4.004514128052518 | 3.1885 | 57 | ❌ |
| ENAUSDT | 12h | both | fixed_pct | ALL | 3.7967171472396632 | 3.7967 | 15 | ✅ |
| ENAUSDT | 12h | both | fixed_signal | ALL | 3.7967171472396632 | 3.7967 | 15 | ✅ |
| TAOUSDT | 15m | short | embedded | TUE+FRI+SAT | 3.7024127426553837 | 1.8318 | 28 | ✅ |
| TAOUSDT | 15m | short | atr | MON+SAT | 3.685411747977875 | 1.3416 | 26 | ❌ |
| DOTUSDT | 15m | short | fixed_pct | TUE+SUN | 3.138647165645347 | 0.4153 | 114 | ✅ |
| DOTUSDT | 15m | short | fixed_signal | TUE+SUN | 3.138647165645347 | 0.4153 | 114 | ✅ |
| DYDXUSDT | 15m | short | fixed_pct | MON+TUE+SUN | 3.0366174386802136 | 1.2849 | 133 | ✅ |
| DYDXUSDT | 15m | short | fixed_signal | MON+TUE+SUN | 3.0366174386802136 | 1.2849 | 133 | ✅ |
| AAVEUSDT | 1h | long | embedded | MON+WED+FRI | 3.0257498958506353 | 0.5462 | 52 | ❌ |
| SUIUSDT | 1h | long | embedded | MON+SAT+SUN | 2.9794360679337806 | 1.7663 | 33 | ✅ |
| OPUSDT | 15m | short | fixed_pct | MON+TUE | 2.707461605876899 | 0.8869 | 85 | ✅ |
| OPUSDT | 15m | short | fixed_signal | MON+TUE | 2.707461605876899 | 0.8869 | 85 | ✅ |
| SEIUSDT | 1h | long | embedded | MON+FRI | 2.6689415060016324 | 0.5657 | 20 | ✅ |
| INJUSDT | 1h | short | atr | SAT | 2.5956327564785413 | 0.9048 | 25 | ✅ |
| NEARUSDT | 1h | long | atr | THU+FRI | 2.561685061846132 | 0.8019 | 66 | ❌ |
| NEARUSDT | 1h | long | embedded | THU+FRI | 2.561685061846132 | 0.8019 | 66 | ❌ |
| DYDXUSDT | 1h | short | fixed_pct | MON+TUE+SUN | 2.5525672737647205 | 0.1147 | 62 | ✅ |
| DYDXUSDT | 1h | short | fixed_signal | MON+TUE+SUN | 2.5525672737647205 | 0.1147 | 62 | ✅ |
| DASHUSDT | 15m | short | fixed_pct | MON+TUE+THU+SUN | 2.5259758006170876 | 1.0231 | 214 | ✅ |
| DASHUSDT | 15m | short | fixed_signal | MON+TUE+THU+SUN | 2.5259758006170876 | 1.0231 | 214 | ✅ |
| ATOMUSDT | 1h | short | fixed_pct | TUE+WED+THU+SUN | 2.469266124928323 | 0.2306 | 123 | ❌ |
| ATOMUSDT | 1h | short | fixed_signal | TUE+WED+THU+SUN | 2.469266124928323 | 0.2306 | 123 | ❌ |
| TAOUSDT | 1h | short | atr | TUE+WED+THU+SAT+SUN | 2.455617625099777 | 1.7581 | 21 | ❌ |
| ATOMUSDT | 15m | short | fixed_pct | TUE+THU+SUN | 2.4342309832984106 | 1.2561 | 160 | ✅ |
| ATOMUSDT | 15m | short | fixed_signal | TUE+THU+SUN | 2.4342309832984106 | 1.2561 | 160 | ✅ |
| MANAUSDT | 15m | short | fixed_pct | MON+TUE | 2.4146805319537896 | 0.7913 | 80 | ✅ |
| MANAUSDT | 15m | short | fixed_signal | MON+TUE | 2.4146805319537896 | 0.7913 | 80 | ✅ |
| ENAUSDT | 15m | long | fixed_pct | TUE+WED+THU+FRI | 2.40668057140377 | 1.5881 | 66 | ✅ |
| ENAUSDT | 15m | long | fixed_signal | TUE+WED+THU+FRI | 2.40668057140377 | 1.5881 | 66 | ✅ |
| SUIUSDT | 1h | long | atr | FRI+SAT+SUN | 2.3675397315499707 | 1.1198 | 27 | ❌ |
| AAVEUSDT | 15m | long | embedded | FRI | 2.3656419620699647 | 0.0569 | 72 | ✅ |
| GMXUSDT | 1h | long | embedded | WED | 2.3589106784755876 | 0.9773 | 28 | ❌ |
| UNIUSDT | 12h | long | fixed_pct | MON+WED+THU+FRI+SUN | 2.3292024828824447 | 1.0108 | 23 | ✅ |
| UNIUSDT | 12h | long | fixed_signal | MON+WED+THU+FRI+SUN | 2.3292024828824447 | 1.0108 | 23 | ✅ |
| GMXUSDT | 1h | long | atr | MON+FRI | 2.304950332237135 | 1.3596 | 29 | ✅ |
| OPUSDT | 1h | short | atr | TUE+THU | 2.1850177749972466 | 1.204 | 52 | ❌ |
| SUIUSDT | 15m | long | atr | TUE+WED+FRI | 2.179159068882456 | 0.6576 | 143 | ✅ |
| SUIUSDT | 15m | long | embedded | TUE+WED+FRI | 2.179159068882456 | 0.6576 | 143 | ✅ |
| UNIUSDT | 15m | long | embedded | FRI+SAT+SUN | 2.0949292595145432 | 0.369 | 116 | ✅ |
| UNIUSDT | 1h | both | atr | TUE+SUN | 2.087052472954931 | 0.2737 | 83 | ✅ |
| DASHUSDT | 1h | short | fixed_pct | WED+THU+SUN | 2.073155675885663 | 0.7377 | 81 | ✅ |
| DASHUSDT | 1h | short | fixed_signal | WED+THU+SUN | 2.073155675885663 | 0.7377 | 81 | ✅ |
| UNIUSDT | 1h | long | atr | MON+TUE+WED+FRI | 2.016094629665087 | 1.1532 | 30 | ❌ |
| UNIUSDT | 1h | both | fixed_pct | THU+FRI+SUN | 2.0096897860956986 | 1.0807 | 163 | ❌ |
| UNIUSDT | 1h | both | fixed_signal | THU+FRI+SUN | 2.0096897860956986 | 1.0807 | 163 | ❌ |
| UNIUSDT | 1h | long | embedded | FRI+SUN | 1.8277464634109342 | 0.4034 | 61 | ❌ |
| SEIUSDT | 15m | long | atr | THU+FRI+SAT+SUN | 1.8161494753551668 | 0.915 | 90 | ❌ |
| OPUSDT | 12h | short | fixed_pct | MON+TUE+WED+SAT+SUN | 1.8053316067283038 | 1.0421 | 21 | ❌ |
| OPUSDT | 12h | short | fixed_signal | MON+TUE+WED+SAT+SUN | 1.8053316067283038 | 1.0421 | 21 | ❌ |
| MANAUSDT | 12h | short | fixed_pct | TUE+WED+THU+FRI+SAT+SUN | 1.8038062303615034 | 1.2783 | 20 | ✅ |
| MANAUSDT | 12h | short | fixed_signal | TUE+WED+THU+FRI+SAT+SUN | 1.8038062303615034 | 1.2783 | 20 | ✅ |
| INJUSDT | 12h | short | fixed_pct | ALL | 1.720309518929444 | 1.7203 | 19 | ✅ |
| INJUSDT | 12h | short | fixed_signal | ALL | 1.720309518929444 | 1.7203 | 19 | ✅ |
| INJUSDT | 1h | short | embedded | THU+SUN | 1.7023844294212171 | 0.9048 | 36 | ❌ |
| ETHUSDT | 1h | long | fixed_pct | FRI+SUN | 1.5330496299800085 | 0.0235 | 26 | ✅ |
| ETHUSDT | 1h | long | fixed_signal | FRI+SUN | 1.5330496299800085 | 0.0235 | 26 | ✅ |
| AXSUSDT | 15m | short | embedded | ALL | 1.4393182300658853 | 1.4393 | 1 | ✅ |
| OPUSDT | 12h | short | atr | ALL | 1.4123678321455821 | 1.4124 | 1 | ✅ |
| FETUSDT | 15m | long | atr | ALL | 1.4027169364939227 | 1.4027 | 1 | ✅ |
| FETUSDT | 15m | long | embedded | ALL | 1.4027169364939227 | 1.4027 | 1 | ✅ |
| AAVEUSDT | 12h | long | atr | ALL | 1.3966114949102741 | 1.3966 | 7 | ✅ |
| AAVEUSDT | 15m | long | atr | WED+THU+FRI+SAT+SUN | 1.365063868674165 | 0.5071 | 211 | ❌ |
| INJUSDT | 15m | short | fixed_pct | TUE+THU+SUN | 1.3546480057059718 | 0.0942 | 164 | ✅ |
| INJUSDT | 15m | short | fixed_signal | TUE+THU+SUN | 1.3546480057059718 | 0.0942 | 164 | ✅ |
| FETUSDT | 12h | long | embedded | ALL | 1.1848206296679469 | 1.1848 | 18 | ❌ |
| SEIUSDT | 15m | long | embedded | ALL | 1.1643362037207914 | 1.1643 | 1 | ✅ |
| SEIUSDT | 12h | both | embedded | ALL | 1.1130656952584026 | 1.1131 | 17 | ✅ |
| ETCUSDT | 12h | long | fixed_pct | ALL | 1.0914293257795378 | 1.0914 | 12 | ❌ |
| ETCUSDT | 12h | long | fixed_signal | ALL | 1.0914293257795378 | 1.0914 | 12 | ❌ |
| BNBUSDT | 12h | both | embedded | ALL | 1.0631485885493073 | 1.0631 | 19 | ✅ |
| AAVEUSDT | 12h | long | embedded | ALL | 1.0327871089693004 | 1.0328 | 6 | ❌ |
| TAOUSDT | 1h | short | embedded | ALL | 1.016411469461501 | 1.0164 | 16 | ❌ |
| BNBUSDT | 12h | both | atr | ALL | 0.9928630367075879 | 0.9929 | 19 | ✅ |
| FETUSDT | 12h | long | atr | ALL | 0.9643772973422351 | 0.9644 | 20 | ❌ |
| ADAUSDT | 1h | long | atr | MON+FRI | 0.9560241433575285 | 0.1402 | 43 | ❌ |
| INJUSDT | 12h | short | atr | ALL | 0.9019099299626144 | 0.9019 | 1 | ✅ |
| INJUSDT | 12h | short | embedded | ALL | 0.9019099299626144 | 0.9019 | 1 | ✅ |
| DASHUSDT | 15m | long | atr | ALL | 0.8878733345326284 | 0.8879 | 1 | ✅ |
| DASHUSDT | 15m | long | embedded | ALL | 0.8878733345326284 | 0.8879 | 1 | ✅ |
| ETHUSDT | 1h | long | atr | WED+FRI+SAT | 0.8448513630591239 | 0.2399 | 23 | ❌ |
| BTCUSDT | 12h | long | embedded | ALL | 0.8393738599307349 | 0.8394 | 11 | ✅ |
| UNIUSDT | 12h | long | atr | ALL | 0.8323852942606469 | 0.8324 | 18 | ❌ |
| AXSUSDT | 12h | short | atr | ALL | 0.7395493081809512 | 0.7395 | 1 | ✅ |
| AXSUSDT | 12h | short | embedded | ALL | 0.7395493081809512 | 0.7395 | 1 | ✅ |
| SEIUSDT | 12h | both | atr | ALL | 0.6319383885903194 | 0.6319 | 18 | ❌ |
| DASHUSDT | 12h | long | atr | ALL | 0.6099074891833214 | 0.6099 | 12 | ❌ |
| ETHUSDT | 12h | long | fixed_pct | ALL | 0.5872471491708591 | 0.5872 | 14 | ❌ |
| ETHUSDT | 12h | long | fixed_signal | ALL | 0.5872471491708591 | 0.5872 | 14 | ❌ |
| DASHUSDT | 1h | long | atr | MON+TUE+WED+FRI | 0.5744051562524772 | 0.3086 | 20 | ❌ |
| SEIUSDT | 1h | long | atr | ALL | 0.5090483720415178 | 0.509 | 21 | ✅ |

**Robust rate: 63 / 98**
