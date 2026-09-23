"""Read, update, validate, and save high scores.

This module should manage the high-score file named by configuration, preserve
the expected record format, sort or limit scores according to game rules, and
handle a missing first-run file. It should keep persistence details separate
from gameplay and the on-screen score display.
"""
def high_scores() -> list[dict[str, str | int]]:
    """Return the current high-score entries.

    Returns:
        A list of score records, each with a "name" and "score" key.
        Currently a stub — returns an empty list until real
        persistence is implemented.
    """
    return []







