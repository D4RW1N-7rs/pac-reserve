"""Draw the maze and active game entities.

This module should render walls, paths, the player, ghosts, collectibles, and
level effects using the selected UI toolkit. It should consume already-decided
game state and avoid changing positions, scores, collisions, or positions.
"""

import pygame

WALL_COLOR = (33, 33, 222)
WALL_THICK = 2
HUD_HEIGHT = 60
PADDING    = 16
U, D, R, L = 1, 4, 2, 8   # bit SET = wall exists

def draw_rect(window: pygame.Surface, x: int, y: int, width: int, height: int, color: tuple[int, int, int]) -> None:
    for pixel_y in range(max(0, y), min(window.get_height(), y + height)):
        for pixel_x in range(max(0, x), min(window.get_width(), x + width)):
            window.set_at((pixel_x, pixel_y), color)

def draw_maze(window, maze, tile):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            px = x * tile + PADDING
            py = y * tile + HUD_HEIGHT + PADDING

            if cell == 15:  # solid "42" logo block
                draw_rect(window, px, py, tile, tile, WALL_COLOR)
                continue

            if cell & U:  # top wall exists
                draw_rect(window, px, py, tile, WALL_THICK, WALL_COLOR)
            if cell & D:  # bottom wall exists
                draw_rect(window, px, py + tile - WALL_THICK, tile, WALL_THICK, WALL_COLOR)
            if cell & L:  # left wall exists
                draw_rect(window, px, py, WALL_THICK, tile, WALL_COLOR)
            if cell & R:  # right wall exists
                draw_rect(window, px + tile - WALL_THICK, py, WALL_THICK, tile, WALL_COLOR)

def valid_gum_cells(maze, tile):
    """Return a list of valid grid cells for gum collectibles."""
    cells = []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] != 15:
                cells.append((x, y))
    return cells
