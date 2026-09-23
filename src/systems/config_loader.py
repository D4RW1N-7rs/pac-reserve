"""Load and validate settings from ``config.json``.

This module should locate the project configuration, parse its JSON data, and
provide validated values such as lives, scoring rules, level dimensions, maze
seed, and time limits. It should report missing or invalid settings clearly
and avoid embedding gameplay defaults in unrelated modules.
"""

import json
from pydantic import BaseModel, ConfigDict, ValidationError, Field

class LevelConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")
    level: int = Field(default=1, gt=0)
    seed: int = Field(default=42, gt=0)
    width: int = Field(default=15, gt=0)
    height: int = Field(default=15, gt=0)

class GameConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")
    highscore_filename: str = Field(default="highscores.json", min_length=1)
    levels: list[LevelConfig] = Field(default=[LevelConfig()], min_length=1)
    lives: int = Field(default=3, gt=0)
    pacgum: int = Field(default=42, gt=0)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int = Field(default=42, gt=0)
    level_max_time: int = Field(default=90, gt=0)

def load_config(filename: str) -> dict:
    default_config = GameConfig().model_dump()

    try:
        with open(filename, "r") as f:
            lines = [line for line in f if not line.strip().startswith("#")]
            raw = json.loads("".join(lines))
            
        if not isinstance(raw, dict):
            print(f"Warning: Invalid format in {filename}. "
                  "Using default configuration.")
            return default_config
        
        return GameConfig(**raw).model_dump()
        
    except FileNotFoundError:
        print(f"Warning: Config file '{filename}' not found. "
              "Using default configuration.")
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON syntax in '{filename}'. "
              "Using default configuration.")
    except ValidationError as e:
        print("Invalid game configuration schema:")
        for err in e.errors(include_url=False):
            loc = ".".join(str(loc) for loc in err["loc"])
            print(f"  - {loc}: {err['msg']}")
    except PermissionError:
        print(f"Permission denied when accessing {filename}")
        
    return default_config

if __name__ == "__main__":
    config = load_config("config.json")
    filename_parts = config["highscore_filename"].split(".")
    if len(filename_parts) != 2 or filename_parts[-1] not in ("txt", "json"):
        print(f"High score file must have exactly one .txt or .json extension: {config['highscore_filename']}")
        exit(1)
    print("Loaded Configuration:", config)

