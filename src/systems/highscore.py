"""Read, update, validate, and save high scores.

This module should manage the high-score file named by configuration, preserve
the expected record format, sort or limit scores according to game rules, and
handle a missing first-run file. It should keep persistence details separate
from gameplay and the on-screen score display.
"""

import json
from pathlib import Path
from pydantic import BaseModel, ConfigDict, ValidationError, Field


from typing import Any


class Highscore(BaseModel):
    """Model schema representing a validated high-score entry."""
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=2, max_length=10)
    score: int = Field(ge=0)


def load_scores(filename: str) -> list[dict[str, Any]]:
    """Read and parse validated high scores from a JSON file."""
    path = Path(filename)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("[]", encoding="utf-8")
            return []

        content = path.read_text(encoding="utf-8")

        lines = [
            line for line in content.splitlines()
            if not line.strip().startswith("#")
        ]
        raw = json.loads("\n".join(lines))

        if not isinstance(raw, list):
            print(f"Warning: Invalid format in {filename}. ")
            return []

        return [Highscore(**item).model_dump() for item in raw]

    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON syntax in '{filename}'. ")
        return []
    except ValidationError as e:
        print("Invalid highscore schema:")
        for err in e.errors(include_url=False):
            loc = ".".join(str(loc) for loc in err["loc"])
            print(f"  - {loc}: {err['msg']}")
        return []
    except OSError as error:
        print(f"Could not access highscore file '{filename}': {error}")
        return []


def save_highscore(filename: str, player: str, score: int) -> None:
    """Append a new score and persist top scores to the JSON file."""
    path = Path(filename)
    try:
        scores = load_scores(filename)
        if scores is None:
            scores = []

        scores.append({"name": player, "score": score})
        sorted_scores = sorted(
            scores, key=lambda x: x["score"], reverse=True
        )[:10]

        path.write_text(
            json.dumps(sorted_scores, indent=4), encoding="utf-8"
        )

    except OSError as error:
        print(f"Could not save highscore file '{filename}': {error}")
