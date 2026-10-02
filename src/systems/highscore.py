"""Read, update, validate, and save high scores.

This module should manage the high-score file named by configuration, preserve
the expected record format, sort or limit scores according to game rules, and
handle a missing first-run file. It should keep persistence details separate
from gameplay and the on-screen score display.
"""

import json
import os
from pydantic import BaseModel, ConfigDict, ValidationError, Field

class Highscore(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=2, max_length=10)
    score: int = Field(ge=0)

def load_scores(filename: str) -> list[Highscore]:

    try:
        with open(filename, "r") as f:
            content = f.read()

        lines = [line for line in content.splitlines()
                 if not line.strip().startswith("#")]
        raw = json.loads("\n".join(lines))
            
        if not isinstance(raw, list):
            print(f"Warning: Invalid format in {filename}. ")
            return []
        
        return [Highscore(**item).model_dump() for item in raw]

    except FileNotFoundError:
        print(f"Warning: highscore file '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON syntax in '{filename}'. ")
        return []
    except ValidationError as e:
        print("Invalid highscore schema:")
        for err in e.errors(include_url=False):
            loc = ".".join(str(loc) for loc in err["loc"])
            print(f"  - {loc}: {err['msg']}")
        return []
    except PermissionError:
        print(f"Permission denied when accessing {filename}")
        return []


def save_highscore(filename: str, player: str, score: int) -> None:
    if not os.path.exists(filename):
        print(f"Warning: highscore file '{filename}' not found.")
        return

    try:
        scores = load_scores(filename)
        if scores is None:
            scores = []

        scores.append({"name": player, "score": score})
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

        with open(filename, "w") as f:
            json.dump(sorted_scores, f, indent=4)

    except PermissionError:
        print(f"Permission denied when accessing {filename}")
