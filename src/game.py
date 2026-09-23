"""Coordinate the Pac-Man game state and rules.

This module should own the current level, score, lives, player, ghosts,
collectibles, timing state, and transitions between gameplay states. It should
apply gameplay rules in response to engine events while leaving drawing to the
UI renderer and persistent scores to the high-score system.
"""
import pygame
import time
from enum import Enum, auto
from .ui import menus

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    HIGH_SCORES = auto()
    HELP = auto()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0) #black

def point_in_box(px: int, py: int, x: int, y: int, w: int, h: int) -> bool:
    """Check whether a point falls inside a rectangular box.

    Args:
        px: X coordinate of the point to test.
        py: Y coordinate of the point to test.
        x: X coordinate of the box's top-left corner.
        y: Y coordinate of the box's top-left corner.
        w: Box width.
        h: Box height.

    Returns:
        True if the point lies within the box, False otherwise.
    """
    return x <= px <= x + w and y <= py <= y + h

def centered_x(image: pygame.Surface) -> int:
    """Calculate the X coordinate to center an image on the screen."""
    return (WINDOW_WIDTH - image.get_width()) // 2

def run() -> None:
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PAC-MAN")

    assets = menus.load_assets()
    header_image    = assets["header"]
    background_image = assets["background"]
    play_image      = assets["play"]
    highscore_image = assets["highscores"]
    help_image      = assets["help"]
    exit_image      = assets["exit"]

    play_x = centered_x(play_image)
    play_y = 275
    score_x = centered_x(highscore_image)
    score_y = 335
    help_x = centered_x(help_image)
    help_y = 395
    exit_x = centered_x(exit_image)
    exit_y = 455

    current_state = GameState.MENU

    running = True
    while running:
        frame_start = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                px, py = event.pos
                if point_in_box(px, py, play_x, play_y, play_image.get_width(), play_image.get_height()):
                    current_state = GameState.PLAYING
                    print("play clicked")
                elif point_in_box(px, py, help_x, help_y, help_image.get_width(), help_image.get_height()):
                    current_state = GameState.HELP
                    print("help clicked")
                elif point_in_box(px, py, score_x, score_y, highscore_image.get_width(), highscore_image.get_height()):
                    current_state = GameState.HIGH_SCORES
                    print("highscore clicked")
                elif point_in_box(px, py, exit_x, exit_y, exit_image.get_width(), exit_image.get_height()):
                    running = False

        if current_state == GameState.MENU:
            window.blit(background_image, (0, 0))
            window.blit(header_image, (150, -150))
            window.blit(play_image,      (play_x,  play_y))
            window.blit(highscore_image, (score_x, score_y))
            window.blit(help_image,      (help_x,  help_y))
            window.blit(exit_image,      (exit_x,  exit_y))
        # elif current_state == GameState.PLAYING:
        #     window.fill(BACKGROUND_COLOR)
        # elif current_state == GameState.HIGH_SCORES:
        #     window.fill(BACKGROUND_COLOR)
        # elif current_state == GameState.HELP:
        #     window.fill(BACKGROUND_COLOR)

        pygame.display.flip()

        elapsed = time.time() - frame_start
        sleep_time = (1 / FPS) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    pygame.quit()


