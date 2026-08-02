import pytest

from pyinsts.data.load_config import load_config


def test_load_yaml_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "instruments_address:\n"
        "  N9020B: USB0::0x2A8D::0x1D0B::MY55480186::INSTR\n",
        encoding="utf-8",
    )

    config = load_config(str(config_file))
    assert config["instruments_address"]["N9020B"].startswith("USB0::")


def test_load_json_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(
        '{"instruments_address": {"E5052B": "GPIB0::17::INSTR"}}',
        encoding="utf-8",
    )

    config = load_config(str(config_file))
    assert config["instruments_address"]["E5052B"] == "GPIB0::17::INSTR"


def test_missing_config_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(str(tmp_path / "missing.yaml"))
