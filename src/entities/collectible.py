"""Define dots, power dots, and other collectible gameplay objects.

This module should describe collectible type, position, visibility, and point
value. It should provide the state needed for the game to remove a collectible
when the player reaches it, without handling score persistence or drawing.
"""
from enum import Enum, auto

class CollectibleType(Enum):
    PACGUM = auto()
    SUPER_PACGUM = auto()

class Collectible:
    def __init__(self, x: int, y: int, c_type: CollectibleType, points: int):
        self.x = x
        self.y = y
        self.type = c_type
        self.points = points
        self.visible = True

    def valid_gum_cells(self,maze):
        """Return a list of valid grid cells for gum collectibles."""
        cells = []
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] != 15:
                    cells.append((x, y))
        return cells