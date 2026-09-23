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

def draw_maze(window, maze, tile):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            px = x * tile + PADDING
            py = y * tile + HUD_HEIGHT + PADDING

            if cell == 15:  # solid "42" logo block
                pygame.draw.rect(window, WALL_COLOR, (px, py, tile, tile))
                continue

            if cell & U:  # top wall exists
                pygame.draw.rect(window, WALL_COLOR, (px, py, tile, WALL_THICK))
            if cell & D:  # bottom wall exists
                pygame.draw.rect(window, WALL_COLOR, (px, py + tile - WALL_THICK, tile, WALL_THICK))
            if cell & L:  # left wall exists
                pygame.draw.rect(window, WALL_COLOR, (px, py, WALL_THICK, tile))
            if cell & R:  # right wall exists
                pygame.draw.rect(window, WALL_COLOR, (px + tile - WALL_THICK, py, WALL_THICK, tile))
