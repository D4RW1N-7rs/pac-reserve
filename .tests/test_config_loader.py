from src.systems.config_loader import load_config, validate_config


def test_load_config_keeps_level_timing_data():
    config = load_config("config.json")

    assert config["highscore_filename"] == "data/highscore.json"
    assert config["levels"][0]["level_max_time"] == 60
    assert config["levels"][-1]["level_max_time"] == 330


def test_validate_config_accepts_config_path():
    assert validate_config("config.json") is True
