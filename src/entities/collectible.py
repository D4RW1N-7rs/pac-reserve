"""Define dots, power dots, and other collectible gameplay objects.

This module should describe collectible type, position, visibility, and point
value. It should provide the state needed for the game to remove a collectible
when the player reaches it, without handling score persistence or drawing.
"""
from enum import Enum, auto
import random

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

    @staticmethod
    def valid_gum_cells(maze):
        """Return a list of valid grid cells for gum collectibles."""
        cells = []
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] != 15:
                    cells.append((x, y))
        return cells

    @staticmethod
    def generate_gums(maze, width, height, pacgum_count, points_per_pacgum, points_per_super_pacgum):
        
        # Step 1: Get all walkable cells
        valid_cells = Collectible.valid_gum_cells(maze)
        
        # Step 2: Define the 4 super gum corner positions
        super_positions = [
            (0, 0),
            (0, height - 1),
            (width - 1, 0),
            (width - 1, height - 1)
        ]
        
        # Step 3: Remove super gum spots from valid_cells so regular gums don't spawn there
        # TODO: for each pos in super_positions, remove it from valid_cells if it exists
        for pos in super_positions:
            if pos in valid_cells:
                valid_cells.remove(pos)
        
        # Step 4: Pick regular gum positions
        # TODO: if pacgum_count >= len(valid_cells), use all valid_cells
        # TODO: else, use random.sample(valid_cells, pacgum_count) to pick randomly
        if pacgum_count >= len(valid_cells):
            chosen_positions = valid_cells
        else:
            chosen_positions = random.sample(valid_cells, pacgum_count)

        # Step 5: Build the two lists of Collectible objects
        gums = []
        super_gums = []
        # TODO: For each chosen position, create a Collectible(...) and add it to the list
        for pos in chosen_positions:
            gum = Collectible(pos[0], pos[1], CollectibleType.PACGUM, points_per_pacgum)
            gums.append(gum)
        
        # TODO: Create super gum collectibles for each super position
        for pos in super_positions:
            if maze[pos[1]][pos[0]] != 15:
                super_gum = Collectible(pos[0], pos[1], CollectibleType.SUPER_PACGUM, points_per_super_pacgum)
                super_gums.append(super_gum)

        return gums, super_gums