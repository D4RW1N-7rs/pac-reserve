"""Define ghost entities and their movement state.

This module contains the ghost's position, direction, identity, and movement
logic. Collision outcomes and score changes are left to the game rules layer
rather than being mixed into sprite rendering.
"""


import pygame
from collections import deque
from typing import Any, List, Tuple
import random
import time

U, D, R, L = 1, 4, 2, 8

class Ghost():
    def __init__(self, start_grid_x, start_grid_y, tile_size, color):

        self.pixel_x = start_grid_x * tile_size
        self.pixel_y = start_grid_y * tile_size
        self.start_x = start_grid_x
        self.start_y = start_grid_y
        self.color = color
        self.state = "CHASE"  # "FRIGHTENED" / "CHASE"
        self.frightened_timer = 0.0
        self.direction = "LEFT"
        self.speed = 4
        self.load_images()

    def load_images(self):

        self.images = {
            "LEFT": pygame.image.load(f"img/ghosts/L/{self.color}-L.png"),
            "RIGHT": pygame.image.load(f"img/ghosts/R/{self.color}-R.png"),
            "UP": pygame.image.load(f"img/ghosts/U/{self.color}-U.png"),
            "DOWN": pygame.image.load(f"img/ghosts/D/{self.color}-D.png")
        }

    def draw(self, window, padding, hud_height, tile_size):
        image = self.images[self.direction]
        if self.state == "FRIGHTENED":
            image = pygame.image.load("img/ghosts/dead-ghost.png")
            self.speed = 2

        offset_x = (tile_size - image.get_width()) // 2
        offset_y = (tile_size - image.get_height()) // 2

        draw_x = self.pixel_x + padding + offset_x
        draw_y = self.pixel_y + padding + hud_height + offset_y

        window.blit(image, (draw_x, draw_y))

    def bfs(self, maze: list[list[int]], start: tuple[int, int], target: tuple[int, int]) -> str | None:
        directions = [
            ("UP", 0, -1, U),
            ("DOWN", 0, 1, D),
            ("LEFT", -1, 0, L),
            ("RIGHT", 1, 0, R),
        ]

        queue = deque([(start[0],start[1], None)])

        visited = {(start[0], start[1])}  # TODO 2

        while queue:

            # TODO 3: take the oldest item out of the queue
            x, y, first_direction = queue.popleft()

            # TODO 4: if this cell is the target, return the answer
            if (x , y) == target:
                return first_direction

            for name, dx, dy, wall in directions:
                # skip if the current cell has a wall on this side
                cell = maze[y][x]
                if cell & wall:
                    continue

                # compute the neighbor's coordinates
                next_cell_x = x + dx
                next_cell_y = y + dy

                # skip if out of bounds 'houdodo'
                if not 0 <= next_cell_y < len(maze):
                    continue 
                if not 0 <=  next_cell_x < len(maze[0]):
                    continue

                # skip if already visited
                if (next_cell_x, next_cell_y) in visited:
                    continue
                # skip if the neighbor is a solid cell (15)
                if maze[next_cell_y][next_cell_x] == 15:
                    continue

                # mark visited, work out which first direction it carries,
                visited.add((next_cell_x, next_cell_y))

                if first_direction is None:
                    next_direction = name
                else:
                    next_direction = first_direction 

                # and add it to the queue
                queue.append((next_cell_x, next_cell_y, next_direction))

        return None


    def update(self, maze, tile_size, pacman):

        if self.pixel_x % tile_size == 0 and self.pixel_y % tile_size == 0:

            ghost_x = self.pixel_x // tile_size # to know coordinate(x) the ghost 
            ghost_y = self.pixel_y // tile_size # to know coordinate(y) the ghost

            if not (0 <= ghost_y < len(maze) and 0 <= ghost_x < len(maze[0])):
                return 

            cell = maze[ghost_y][ghost_x]

            if cell == 15:
                return 

            legal_moves = []
            if not (cell & U):  # If there is no wall/block in this direction, add that direction to legal_moves. using bitwise
                legal_moves.append("UP")
            if not (cell & D):
                legal_moves.append("DOWN")
            if not (cell & R):
                legal_moves.append("RIGHT")
            if not (cell & L):
                legal_moves.append("LEFT")

            if not legal_moves: 
                return

            goal_x, goal_y = self.get_target_tile(pacman, tile_size, maze)

            if self.state == "CHASE":
                bfs_move = self.bfs(maze, (ghost_x, ghost_y), (goal_x, goal_y))

            elif self.state == "FRIGHTENED":
                bfs_move = self.bfs(maze, (pacman.pixel_x // tile_size, pacman.pixel_y // tile_size), (ghost_x, ghost_y))            

            if bfs_move in legal_moves:
                self.direction = bfs_move
            elif self.direction not in legal_moves:
                self.direction = random.choice(legal_moves)

        # move
        if self.direction == "UP":
            self.pixel_y -= self.speed
        elif self.direction == "DOWN":
            self.pixel_y += self.speed
        elif self.direction == "LEFT":
            self.pixel_x -= self.speed
        elif self.direction == "RIGHT":
            self.pixel_x += self.speed

    def get_target_tile(
            self, pacman: Any, tile_size: int, maze: List[List[int]]
        ) -> Tuple[int, int]:
        """Determine the ghost's target tile based on its specific AI personality."""
        pacman_x = pacman.pixel_x // tile_size
        pacman_y = pacman.pixel_y // tile_size

        maze_height = len(maze)
        maze_width = len(maze[0])

        target_x, target_y = 0, 0 

        if self.color == "red":
            target_x, target_y = pacman_x, pacman_y

        elif self.color == "pink":
            if pacman.current_direction == "UP":
                target_x, target_y = pacman_x, pacman_y - 4
            elif pacman.current_direction == "DOWN":
                target_x, target_y = pacman_x, pacman_y + 4
            elif pacman.current_direction == "LEFT":
                target_x, target_y = pacman_x - 4, pacman_y
            elif pacman.current_direction == "RIGHT":
                target_x, target_y = pacman_x + 4, pacman_y
            else:
                target_x, target_y = pacman_x, pacman_y

        elif self.color == "cyan":
            # Cyan flanks from BEHIND
            if pacman.current_direction == "UP":
                target_x, target_y = pacman_x, pacman_y + 4
            elif pacman.current_direction == "DOWN":
                target_x, target_y = pacman_x, pacman_y - 4
            elif pacman.current_direction == "LEFT":
                target_x, target_y = pacman_x + 4, pacman_y
            elif pacman.current_direction == "RIGHT":
                target_x, target_y = pacman_x - 4, pacman_y
            else:
                target_x, target_y = pacman_x, pacman_y

        elif self.color == "orange":
            # Orange ghost targets Pac-Man if far away, else targets its corner
            distance = (
                (self.pixel_x - pacman.pixel_x) ** 2
                + (self.pixel_y - pacman.pixel_y) ** 2
            ) ** 0.5
            if distance > 4 * tile_size:
                target_x, target_y = pacman_x, pacman_y
            else:
                target_x, target_y = 0, maze_height - 1  # Bottom-left corner
        else:
            target_x, target_y = 0, 0

        # CLAMP the target to the maze boundaries so BFS doesn't exhaust itself!
        target_x = max(0, min(target_x, maze_width - 1))
        target_y = max(0, min(target_y, maze_height - 1))

        return target_x, target_y

    def collide(self,pacman):
        gx = self.pixel_x
        gy = self.pixel_y

        px = pacman.pixel_x
        py = pacman.pixel_y

        thresholdX = 8
        thresholdY = 8

        dx = abs(gx - px)
        dy = abs(gy - py)

        if dx <= thresholdX and dy <= thresholdY:
            return True
        else:
            return False
