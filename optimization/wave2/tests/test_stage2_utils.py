import json
import sys
import tempfile
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
from stage2_utils import load_stage1_passing, OFF_TF_MAP, SHARPE_FILTER


def _write_stage1_json(base_dir, strategy_id, symbol, tf, direction, sl_type,
                       oos_sharpe, verdict="PASS"):
    d = base_dir / strategy_id / "stage1"
    d.mkdir(parents=True, exist_ok=True)
    payload = {
        "symbol": symbol, "timeframe": tf, "direction": direction,
        "sl_type": sl_type, "oos_sharpe": oos_sharpe, "verdict": verdict,
    }
    (d / f"{symbol}_{tf}_{direction}_{sl_type}.json").write_text(json.dumps(payload))


def test_load_stage1_passing_filters_below_threshold():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage1_json(tmp, "SWING3", "BTCUSDT", "1h", "both", "atr", 0.8)
        _write_stage1_json(tmp, "SWING3", "ETHUSDT", "1h", "long", "embedded", 0.3)
        _write_stage1_json(tmp, "SWING3", "SOLUSDT", "1h", "short", "fixed_pct", 0.6)

        result = load_stage1_passing("SWING3", tmp, sharpe_threshold=0.5)

        assert ("BTCUSDT", "both", "atr") in result
        assert ("SOLUSDT", "short", "fixed_pct") in result
        assert ("ETHUSDT", "long", "embedded") not in result


def test_load_stage1_passing_excludes_fail_verdict():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_stage1_json(tmp, "SWING3", "BTCUSDT", "1h", "both", "atr",
                           oos_sharpe=0.9, verdict="FAIL")
        result = load_stage1_passing("SWING3", tmp)
        assert len(result) == 0


def test_load_stage1_passing_empty_for_missing_dir():
    with tempfile.TemporaryDirectory() as tmp:
        result = load_stage1_passing("NONEXISTENT", Path(tmp))
        assert result == set()


def test_load_stage1_passing_skips_corrupt_json():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d = tmp / "SWING3" / "stage1"
        d.mkdir(parents=True)
        (d / "BTCUSDT_1h_both_atr.json").write_text("{invalid json")
        result = load_stage1_passing("SWING3", tmp)
        assert result == set()


def test_off_tf_map_1h_home():
    assert set(OFF_TF_MAP["1h"]) == {"15m", "4h", "12h"}
    assert len(OFF_TF_MAP["1h"]) == 3


def test_off_tf_map_4h_home():
    assert set(OFF_TF_MAP["4h"]) == {"15m", "1h", "12h"}
    assert len(OFF_TF_MAP["4h"]) == 3


def test_sharpe_filter_default_is_half():
    assert SHARPE_FILTER == 0.5
