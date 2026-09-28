"""Coordinate the Pac-Man game state and rules.

This module should own the current level, score, lives, player, ghosts,
collectibles, timing state, and transitions between gameplay states. It should
apply gameplay rules in response to engine events while leaving drawing to the
UI renderer and persistent scores to the high-score system.
"""
import pygame
import time
from enum import Enum, auto

from .ui.renderer import draw_maze
from .ui import menus
from .systems import highscore
from .systems.maze_integration import create_maze
from .systems.config_loader import load_config
from .ui.hud import draw_hud


class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    HIGH_SCORES = auto()
    HELP = auto()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)

def create_window(width: int, height: int) -> pygame.Surface:
    """Open a brand-new window of the given size, centered on screen."""
    pygame.display.quit()
    pygame.display.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PAC-MAN")
    return window

def point_in_box(px: int, py: int, x: int, y: int, w: int, h: int) -> bool:
    """Check whether a point falls inside a rectangular box."""
    return x <= px <= x + w and y <= py <= y + h

def centered_x(image: pygame.Surface) -> int:
    """Calculate the X coordinate to center an image on the screen."""
    return (WINDOW_WIDTH - image.get_width()) // 2

def run() -> None:
    pygame.init()
    window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_caption("PAC-MAN")

    assets = menus.load_assets()
    font = assets["font"]
    help_font = assets["help_font"]
    header_image    = assets["header"]
    scores_header = assets["scores_header"]
    scores_background = assets["scores_background"]
    background_image = assets["background"]
    play_image      = assets["play"]
    highscore_image = assets["highscores"]
    help_image      = assets["help"]
    exit_image      = assets["exit"]
    back_image= assets["back"]
    pac_head_image= assets["pac-head"]

    play_x = centered_x(play_image)
    play_y = 275
    score_x = centered_x(highscore_image)
    score_y = 335
    help_x = centered_x(help_image)
    help_y = 395
    exit_x = centered_x(exit_image)
    exit_y = 455
    back_x = centered_x(back_image)
    back_y = 520

    current_state = GameState.MENU

    TILE = 35
    HUD_HEIGHT = 60
    PADDING = 16
    config = load_config("config.json")

    score = 0 #get_score()  # Placeholder for actual score retrieval logic
    lives = config["lives"]
    current_level = 10
    level_data = config["levels"][current_level - 1]
    maze = None 

    running = True
    while running:
        frame_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                px, py = event.pos
                if current_state == GameState.MENU:
                    if point_in_box(px, py, play_x, play_y, play_image.get_width(), play_image.get_height()):
                        level_data = config["levels"][current_level - 1]
                        maze = create_maze(level_data["width"], level_data["height"], level_data["seed"])
                        new_w = level_data["width"]  * TILE + PADDING * 2
                        new_h = level_data["height"] * TILE + HUD_HEIGHT + PADDING * 2
                        window = create_window(new_w, new_h)
                        current_state = GameState.PLAYING
                    elif point_in_box(px, py, help_x, help_y, help_image.get_width(), help_image.get_height()):
                        current_state = GameState.HELP
                    elif point_in_box(px, py, score_x, score_y, highscore_image.get_width(), highscore_image.get_height()):
                        current_state = GameState.HIGH_SCORES
                    elif point_in_box(px, py, exit_x, exit_y, exit_image.get_width(), exit_image.get_height()):
                        running = False
                elif current_state == GameState.HIGH_SCORES:
                    if point_in_box(px, py, back_x, back_y, back_image.get_width(), back_image.get_height()):
                        current_state = GameState.MENU
                elif current_state == GameState.HELP:
                    if point_in_box(px, py, back_x, back_y, back_image.get_width(), back_image.get_height()):
                        current_state = GameState.MENU

        if current_state == GameState.MENU:
            window.blit(background_image, (0, 0))
            window.blit(header_image, (150, -150))
            window.blit(play_image,      (play_x,  play_y))
            window.blit(highscore_image, (score_x, score_y))
            window.blit(help_image,      (help_x,  help_y))
            window.blit(exit_image,      (exit_x,  exit_y))

        elif current_state == GameState.PLAYING:
            window.fill(BACKGROUND_COLOR)
            draw_maze(window, maze, TILE)
            draw_hud(window, font, current_level, score, lives, pac_head_image)

        elif current_state == GameState.HIGH_SCORES:
            window.blit(scores_background, (0, 0))
            window.blit(scores_header, (centered_x(scores_header), 20))
            scores = highscore.high_scores()
            menus.draw_high_scores(window,font,scores)
            window.blit(back_image, (back_x,back_y))

        elif current_state == GameState.HELP:
            window.fill(BACKGROUND_COLOR)
            menus.draw_help(window, help_font)
            window.blit(back_image, (back_x,back_y))

        pygame.display.flip()

        elapsed = time.time() - frame_start
        sleep_time = (1 / FPS) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    pygame.quit()


