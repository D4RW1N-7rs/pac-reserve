"""Provide the main runtime loop and low-level game timing.

This module owns display window creation, point-in-box and coordinate math,
and the main frame loop that dispatches events, updates, and rendering.
"""
import pygame
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 40


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


def centered_x(image: pygame.Surface, window_width: int) -> int:
    """Calculate the X coordinate to center an image horizontally."""
    return (window_width - image.get_width()) // 2


def centered_y(image: pygame.Surface, window_height: int) -> int:
    """Calculate the Y coordinate to center an image vertically."""
    return (window_height - image.get_height()) // 2


def run_loop(game) -> None:
    """Drive the main game loop, dispatching events, updates, and renders."""
    pygame.init()

    while game.running:
        frame_start = time.time()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game.running = False
                break

        if not game.running:
            break

        game.handle_events(events)
        game.update()
        game.draw()

        pygame.display.flip()

        elapsed = time.time() - frame_start
        sleep_time = (1 / FPS) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    pygame.quit()
