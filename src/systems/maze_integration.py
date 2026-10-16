"""Adapt the installed ``mazegenerator`` package for Pac-Man.

This module should construct ``MazeGenerator`` instances, translate generated
cell wall bitmasks into the game's maze representation, identify traversable
locations and level boundaries. Keepthe third-party package import and
conversion logic here so the rest of thegame does not depend on its
internal representation.
"""


from typing import cast
from mazegenerator.mazegenerator import MazeGenerator


def create_maze(
    width: int, height: int, seed: int
) -> list[list[int]] | None:
    """Generate and return a maze grid with walls and corridors."""
    try:
        gen = MazeGenerator(size=(width, height), seed=seed, perfect=False)
        return cast(list[list[int]], gen.maze)
    except Exception as e:
        print(f"Maze generator failed: {e}")
        return None
