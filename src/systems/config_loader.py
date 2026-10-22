"""Load and validate settings from ``config.json``.

This module should locate the project configuration, parse its JSON data, and
provide validated values such as lives, scoring rules, level dimensions, maze
seed, and time limits. It should report missing or invalid settings clearly
and avoid embedding gameplay defaults in unrelated modules.
"""

import json
from typing import Any
from pydantic import BaseModel, ConfigDict, ValidationError, Field


# In src/systems/config_loader.py

_DEFAULT_CONFIG: dict[str, Any] = {
    "highscore_filename": "data/highscores.json",
    "lives": 3,
    "pacgum": 420,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "levels": [
        {
            "level": 1, "seed": 42, "width": 15, "height": 15,
            "level_max_time": 100,
        },
        {
            "level": 2, "seed": 13, "width": 18, "height": 18,
            "level_max_time": 120,
        },
        {
            "level": 3, "seed": 37, "width": 20, "height": 20,
            "level_max_time": 140,
        },
        {
            "level": 4, "seed": 22, "width": 23, "height": 23,
            "level_max_time": 150,
        },
        {
            "level": 5, "seed": 20, "width": 28, "height": 23,
            "level_max_time": 200,
        },
        {
            "level": 6, "seed": 26, "width": 34, "height": 23,
            "level_max_time": 230,
        },
        {
            "level": 7, "seed": 16, "width": 38, "height": 23,
            "level_max_time": 250,
        },
    ]
}


class LevelConfig(BaseModel):
    """Schema validation model for a single game level."""
    model_config = ConfigDict(extra="ignore")
    level: int = Field(default=1, gt=0)
    seed: int = Field(default=42, gt=0)
    width: int = Field(default=15, gt=7, lt=48)
    height: int = Field(default=15, gt=7, lt=24)
    level_max_time: int = Field(default=100, ge=0)


class GameConfig(BaseModel):
    """Schema validation model for global game configuration."""
    model_config = ConfigDict(extra="ignore")
    highscore_filename: str = Field(
        default="data/highscores.json", min_length=1
    )
    levels: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig()], min_length=1
    )
    lives: int = Field(default=3, gt=0)
    pacgum: int = Field(default=420, ge=0)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)


def load_config(filename: str) -> dict[str, Any]:
    """Load and validate JSON configuration file or return defaults."""
    default_config = _DEFAULT_CONFIG.copy()

    try:
        with open(filename, "r") as f:
            content = f.read()

        if not content.strip():
            print(
                f"Warning: Config file '{filename}' is empty. "
                "Using default configuration."
            )
            return default_config

        lines = [
            line for line in content.splitlines()
            if not line.strip().startswith("#")
        ]
        raw = json.loads("\n".join(lines))

        if not isinstance(raw, dict):
            print(
                f"Warning: Invalid format in {filename}. "
                "Using default configuration."
            )
            return default_config

        validate_config(raw)

        return GameConfig(**raw).model_dump()

    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print(f"Warning: {e}. Falling back to default configuration.")
        return default_config
    except ValidationError as e:
        print("Invalid game configuration schema:")
        for err in e.errors(include_url=False):
            loc = ".".join(str(loc) for loc in err["loc"])
            print(f"  - {loc}: {err['msg']}")
        print("Falling back to default full configuration.")
        return default_config


def validate_config(config_file: str | dict[str, Any]) -> bool:
    """Validate highscore file format in the loaded configuration."""
    if isinstance(config_file, str):
        config = load_config(config_file)
    else:
        config = config_file
    filename = config.get(
        "highscore_filename", GameConfig().highscore_filename
    )
    filename_parts = filename.split(".")
    if len(filename_parts) != 2 or filename_parts[-1] != "json":
        print(
            "High score file must have exactly one .json extension: "
            f"{filename}"
        )
        raise SystemExit(1)

    return True
