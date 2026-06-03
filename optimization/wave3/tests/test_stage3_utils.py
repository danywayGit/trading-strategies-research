# Run with: python -m pytest tests/test_stage3_utils.py -v
# Requires: pip install pytest  (or use BacktestingMCP venv which has pytest)
import json
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from stage3_utils import DOW_MASKS, MIN_TRADES, MIN_LIFT, select_winner, load_stage2_passing


def _write_stage2_json(base, strategy_id, symbol, tf, direction, sl_type,
                       oos_sharpe, best_params=None, verdict="PASS"):
    d = base / strategy_id / "stage2"
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": symbol, "timeframe": tf, "direction": direction,
        "sl_type": sl_type, "oos_sharpe": oos_sharpe, "verdict": verdict,
        "best_params": best_params or {"p": 1},
    }
    (d / f"{symbol}_{tf}_{direction}_{sl_type}.json").write_text(json.dumps(payload))


def _make_dow_results(all_s=0.8, monf_s=1.1, monf_t=25, all_t=38):
    return {
        "ALL":     {"oos_sharpe": all_s,  "num_trades": all_t},
        "MON-FRI": {"oos_sharpe": monf_s, "num_trades": monf_t},
        "SAT-SUN": {"oos_sharpe": 0.3,   "num_trades": 12},
        "MON":     {"oos_sharpe": 0.9,   "num_trades": 8},
        "TUE":     {"oos_sharpe": 0.95,  "num_trades": 9},
        "WED":     {"oos_sharpe": 0.7,   "num_trades": 7},
        "THU":     {"oos_sharpe": 1.0,   "num_trades": 6},
        "FRI":     {"oos_sharpe": 0.85,  "num_trades": 8},
    }


def test_select_winner_picks_best_with_improvement():
    results = _make_dow_results(all_s=0.8, monf_s=1.1, monf_t=25)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "MON-FRI"
    assert sharpe == 1.1
    assert trades == 25
    assert improved is True


def test_select_winner_defaults_to_all_insufficient_lift():
    results = _make_dow_results(all_s=0.8, monf_s=0.89, monf_t=25)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_defaults_to_all_insufficient_trades():
    results = _make_dow_results(all_s=0.8, monf_s=1.5, monf_t=15)
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_boundary_exact_lift():
    # Exactly 0.10 above ALL — must NOT be accepted (strictly greater required)
    results = _make_dow_results(all_s=0.8, monf_s=0.90, monf_t=25)
    mask, _, _, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_select_winner_boundary_above_lift():
    # 0.101 above ALL — should be accepted
    results = _make_dow_results(all_s=0.8, monf_s=0.901, monf_t=25)
    mask, _, _, improved = select_winner(results)
    assert mask == "MON-FRI"
    assert improved is True


def test_select_winner_all_no_trades_defaults_gracefully():
    results = {k: {"oos_sharpe": None, "num_trades": 0} for k in DOW_MASKS}
    mask, sharpe, trades, improved = select_winner(results)
    assert mask == "ALL"
    assert improved is False


def test_dow_masks_has_8_entries():
    assert len(DOW_MASKS) == 8


def test_dow_masks_all_is_none():
    assert DOW_MASKS["ALL"] is None


def test_dow_masks_weekdays():
    assert DOW_MASKS["MON-FRI"] == {0, 1, 2, 3, 4}


def test_load_stage2_passing_reads_pass_only():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage2_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr", 0.8)
        _write_stage2_json(tmp, "SWING3", "ETHUSDT", "4h", "long", "embedded", 0.3, verdict="FAIL")
        result = load_stage2_passing("SWING3", tmp)
        assert len(result) == 1
        assert result[0]["symbol"] == "BTCUSDT"
        assert result[0]["stage2_oos_sharpe"] == 0.8
        assert "best_params" in result[0]


def test_load_stage2_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_stage2_passing("NONEXISTENT", Path(tmp))
        assert result == []


def test_load_stage2_passing_rejects_non_usdt_symbol():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Write a PASS result with a non-USDT symbol (malformed)
        d = tmp / "SWING3" / "stage2"
        d.mkdir(parents=True, exist_ok=True)
        payload = {
            "symbol": "BTC",  # missing USDT suffix
            "timeframe": "4h", "direction": "both", "sl_type": "atr",
            "oos_sharpe": 0.9, "verdict": "PASS", "best_params": {},
        }
        (d / "BTC_4h_both_atr.json").write_text(json.dumps(payload))
        result = load_stage2_passing("SWING3", tmp)
        assert result == []
