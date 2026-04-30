"""Configuration management for PyLock.
Handles loading, saving, updating, and reseting user config."""
import json
import os

CONFIG_PATH = os.path.expanduser("~/.pylock_config.json")

#CONFIG CONSTANTS
DEFAULT_CONFIG = {
    "min_length": 12,
    "require_symbols": True,
    "require_numbers": True,
    "no_repeats": True,
    "default_algo": "bcrypt"
}


def load_config():
    """Load config from file or return defaults if missing/corrupted."""
    if not os.path.exists(CONFIG_PATH):
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """Persist config to file."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def set_config(key, value):
    """Update a specific config key with type casting and validation."""
    config = load_config()

    if key not in DEFAULT_CONFIG:
        raise ValueError("Invalid config key")

    if isinstance(DEFAULT_CONFIG[key], bool):
        value = value.lower() in ["true", "1", "yes"]

    elif isinstance(DEFAULT_CONFIG[key], int):
        value = int(value)

    config[key] = value
    save_config(config)

    return config


def reset_config():
    """Reset config to default values."""
    save_config(DEFAULT_CONFIG.copy())
    return DEFAULT_CONFIG