import pygame
import random
import sys
import os

# Add parent directory to path to import mazegenerator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mazegenerator.mazegenerator import MazeGenerator
from ghost_ui import GhostUI
from pac_ui import PacUI

# ── Config ────────────────────────────────────────────────────────────────
SIZE = (30, 30)
SEED = 42
CELL_SIZE = 30  # pixels per cell
WALL_COLOR = (0, 0, 255)  # Blue walls
BG_COLOR = (0, 0, 0)      # Black background
SPECIAL_COLOR = (50, 50, 50)  # Gray for the special "42" cells
PADDING = 20  # Padding around the maze in pixels
# ──────────────────────────────────────────────────────────────────────────

N, E, S, W = 1, 2, 4, 8

def draw_maze(screen, maze):
    h, w = len(maze), len(maze[0])
    
    for y in range(h):
        for x in range(w):
            c = maze[y][x]
            
            px = x * CELL_SIZE + PADDING
            py = y * CELL_SIZE + PADDING
            
            if c == 15: # the "42" cell
                pygame.draw.rect(screen, SPECIAL_COLOR, (px, py, CELL_SIZE, CELL_SIZE))
                continue
                
            # Draw walls (lines between corners)
            if c & N:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px + CELL_SIZE, py), 2)
            if c & S:
                pygame.draw.line(screen, WALL_COLOR, (px, py + CELL_SIZE), (px + CELL_SIZE, py + CELL_SIZE), 2)
            if c & E:
                pygame.draw.line(screen, WALL_COLOR, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)
            if c & W:
                pygame.draw.line(screen, WALL_COLOR, (px, py), (px, py + CELL_SIZE), 2)


def get_valid_moves(maze, x, y):
    c = maze[y][x]
    moves = []
    h = len(maze)
    w = len(maze[0])
    
    def can_move(dx, dy, wall_flag):
        if c & wall_flag: return False
        nx, ny = x + dx, y + dy
        if ny < 0 or ny >= h or nx < 0 or nx >= w: return False
        if maze[ny][nx] == 15: return False  # Cannot enter the "42"
        return True

    if can_move(0, -1, N): moves.append((0, -1, "U"))
    if can_move(0, 1, S): moves.append((0, 1, "D"))
    if can_move(1, 0, E): moves.append((1, 0, "R"))
    if can_move(-1, 0, W): moves.append((-1, 0, "L"))
    
    return moves


class GhostController:
    def __init__(self, ghost_ui, maze, start_x, start_y):
        self.ghost_ui = ghost_ui
        self.maze = maze
        self.grid_x = start_x
        self.grid_y = start_y
        
        # Pixel coordinates
        self.pixel_x = start_x * CELL_SIZE + PADDING
        self.pixel_y = start_y * CELL_SIZE + PADDING
        self.ghost_ui.set_position(self.pixel_x, self.pixel_y)
        
        self.moving = False
        self.target_grid_x = start_x
        self.target_grid_y = start_y
        self.speed = 2 # Must cleanly divide CELL_SIZE
        self.dx = 0
        self.dy = 0
        
    def update(self):
        if self.moving:
            self.pixel_x += self.dx * self.speed
            self.pixel_y += self.dy * self.speed
            self.ghost_ui.set_position(self.pixel_x, self.pixel_y)
            
            target_pixel_x = self.target_grid_x * CELL_SIZE + PADDING
            target_pixel_y = self.target_grid_y * CELL_SIZE + PADDING
            
            if self.pixel_x == target_pixel_x and self.pixel_y == target_pixel_y:
                self.moving = False
                self.grid_x = self.target_grid_x
                self.grid_y = self.target_grid_y
        else:
            # Ghost is centered in a cell, pick a new direction
            valid_moves = get_valid_moves(self.maze, self.grid_x, self.grid_y)
            
            # Simple logic: try not to go back the way we came unless it's a dead end
            opposites = {"U": "D", "D": "U", "L": "R", "R": "L"}
            current_dir = self.ghost_ui.direction
            
            forward_moves = [m for m in valid_moves if opposites.get(current_dir) != m[2]]
            
            if forward_moves:
                move = random.choice(forward_moves)
            elif valid_moves:
                move = random.choice(valid_moves) # Dead end, reverse
            else:
                return # Trapped
                
            dx, dy, d_str = move
            self.target_grid_x = self.grid_x + dx
            self.target_grid_y = self.grid_y + dy
            self.dx = dx
            self.dy = dy
            self.moving = True
            self.ghost_ui.update_direction(d_str)

    def draw(self, screen):
        self.ghost_ui.draw(screen)


def main():
    pygame.init()
    
    # Generate the maze
    maze = MazeGenerator(size=SIZE, seed=SEED).maze
    
    # Calculate window size based on maze dimensions
    width = len(maze[0]) * CELL_SIZE + PADDING * 2
    height = len(maze) * CELL_SIZE + PADDING * 2
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maze Pygame Visualization")
    
    clock = pygame.time.Clock()
    
    # Create Ghosts
    colors = ["cyan", "orange", "pink", "red"]
    ghosts = []
    
    # Define the 4 corners for the ghosts to spawn
    corners = [
        (0, 0),                            # Top-Left
        (SIZE[0] - 1, 0),                  # Top-Right
        (0, SIZE[1] - 1),                  # Bottom-Left
        (SIZE[0] - 1, SIZE[1] - 1)         # Bottom-Right
    ]
    
    for i, color in enumerate(colors):
        start_x, start_y = corners[i % len(corners)]
        
        # Fallback if a corner happens to be a "42" cell (highly unlikely, but safe)
        if maze[start_y][start_x] == 15:
            for fallback_y in range(SIZE[1]):
                for fallback_x in range(SIZE[0]):
                    if maze[fallback_y][fallback_x] != 15:
                        start_x, start_y = fallback_x, fallback_y
                        break
                if maze[start_y][start_x] != 15: break
                
        ui = GhostUI(color, 0, 0, size=CELL_SIZE)
        controller = GhostController(ui, maze, start_x, start_y)
        ghosts.append(controller)
    
    # --- Pacman Setup ---
    # Find a valid spawn point near the middle for Pacman
    center_x, center_y = SIZE[0] // 2, SIZE[1] // 2
    pac_start_x, pac_start_y = center_x, center_y
    if maze[center_y][center_x] == 15:
        # Search outwards for nearest non-15 cell
        for radius in range(1, max(SIZE)):
            found = False
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = center_x + dx, center_y + dy
                    if 0 <= nx < SIZE[0] and 0 <= ny < SIZE[1] and maze[ny][nx] != 15:
                        pac_start_x, pac_start_y = nx, ny
                        found = True
                        break
                if found: break
            if found: break

    pac_ui = PacUI(0, 0, size=CELL_SIZE)
    pac_controller = GhostController(pac_ui, maze, pac_start_x, pac_start_y) # Reuse GhostController logic for random wandering

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Update logic
        for ghost in ghosts:
            ghost.update()
        pac_controller.update()
            
        # Draw everything
        screen.fill(BG_COLOR)
        draw_maze(screen, maze)
        
        for ghost in ghosts:
            ghost.draw(screen)
        
        pac_controller.draw(screen)
            
        pygame.display.flip()
        clock.tick(60) # 60 FPS cap
        
    pygame.quit()

if __name__ == "__main__":
    main()
