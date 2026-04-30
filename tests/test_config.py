import tempfile
from pylock.core import config as cfg


def test_load_default_config():
    config = cfg.load_config()
    assert "min_length" in config
    assert "default_algo" in config


def test_set_and_get_config():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        cfg.CONFIG_PATH = tmp.name

        cfg.set_config("min_length", "16")
        config = cfg.load_config()

        assert config["min_length"] == 16


def test_reset_config():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        cfg.CONFIG_PATH = tmp.name

        cfg.set_config("min_length", "20")
        cfg.reset_config()

        config = cfg.load_config()
        assert config["min_length"] == 12


def test_invalid_config_key():
    try:
        cfg.set_config("invalid_key", "value")
        assert False
    except ValueError:
        assert True