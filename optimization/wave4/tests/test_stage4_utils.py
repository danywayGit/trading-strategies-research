# Run with: python -m pytest tests/test_stage4_utils.py -v
# Requires: BacktestingMCP venv which has pytest
import json, sys, tempfile
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent))
from stage4_utils import nudge_params, load_stage3_passing, SENSITIVITY_FILTER

def _write_stage3_json(base, strategy_id, symbol, tf, direction, sl_type,
                       winner_sharpe, winner_mask="ALL", best_params=None):
    d = base / strategy_id / "stage3"
    d.mkdir(parents=True, exist_ok=True)
    payload = {"symbol": symbol, "timeframe": tf, "direction": direction,
               "sl_type": sl_type, "winner_sharpe": winner_sharpe,
               "winner_mask": winner_mask, "winner_trades": 30,
               "stage2_oos_sharpe": 0.6, "best_params": best_params or {"p": 1}}
    (d / f"{symbol}_{tf}_{direction}_{sl_type}_dow.json").write_text(json.dumps(payload))

def test_nudge_params_floats_up():
    assert nudge_params({"st_factor": 2.0}, 1.1)["st_factor"] == pytest.approx(2.2, rel=1e-4)

def test_nudge_params_floats_down():
    assert nudge_params({"st_factor": 2.0}, 0.9)["st_factor"] == pytest.approx(1.8, rel=1e-4)

def test_nudge_params_integers_up():
    r = nudge_params({"st_period": 10}, 1.1)
    assert r["st_period"] == 11 and isinstance(r["st_period"], int)

def test_nudge_params_integers_down():
    r = nudge_params({"st_period": 10}, 0.9)
    assert r["st_period"] == 9 and isinstance(r["st_period"], int)

def test_nudge_params_integer_minimum_one():
    assert nudge_params({"st_period": 1}, 0.9)["st_period"] == 1

def test_nudge_params_skips_direction_key():
    r = nudge_params({"st_period": 10, "direction": "long"}, 1.1)
    assert r["direction"] == "long" and r["st_period"] == 11

def test_nudge_params_skips_string_values():
    r = nudge_params({"mode": "fast", "period": 5}, 1.1)
    assert r["mode"] == "fast" and r["period"] == 6

def test_nudge_params_skips_bool_values():
    # bool is subclass of int — must be excluded explicitly
    r = nudge_params({"use_filter": True, "period": 10}, 1.1)
    assert r["use_filter"] is True and r["period"] == 11

def test_nudge_params_does_not_mutate_input():
    original = {"st_period": 10}
    nudge_params(original, 1.1)
    assert original["st_period"] == 10

def test_load_stage3_passing_filters_by_sharpe():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage3_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr", winner_sharpe=0.8)
        _write_stage3_json(tmp, "SWING3", "ETHUSDT", "4h", "long", "embedded", winner_sharpe=0.3)
        result = load_stage3_passing("SWING3", tmp, sharpe_threshold=0.5)
        syms = [r["symbol"] for r in result]
        assert "BTCUSDT" in syms and "ETHUSDT" not in syms

def test_load_stage3_passing_includes_all_required_keys():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage3_json(tmp, "SWING3", "BTCUSDT", "4h", "both", "atr",
                           winner_sharpe=0.9, winner_mask="MON-FRI",
                           best_params={"st_period": 10})
        result = load_stage3_passing("SWING3", tmp)
        assert len(result) == 1
        for key in ("symbol","timeframe","direction","sl_type","best_params",
                    "winner_mask","winner_sharpe","winner_trades","stage2_oos_sharpe"):
            assert key in result[0], f"Missing key: {key}"

def test_load_stage3_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        assert load_stage3_passing("NONEXISTENT", Path(tmp)) == []

def test_load_stage3_passing_skips_none_winner_sharpe():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d = tmp / "SWING3" / "stage3"; d.mkdir(parents=True)
        payload = {"symbol": "BTCUSDT", "timeframe": "4h", "direction": "both",
                   "sl_type": "atr", "winner_sharpe": None, "winner_mask": "ALL",
                   "winner_trades": 30, "stage2_oos_sharpe": 0.5, "best_params": {}}
        (d / "BTCUSDT_4h_both_atr_dow.json").write_text(json.dumps(payload))
        assert load_stage3_passing("SWING3", tmp) == []

def test_sensitivity_filter_default():
    assert SENSITIVITY_FILTER == 0.5
