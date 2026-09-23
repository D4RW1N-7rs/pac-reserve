"""Render menus and handle menu selections.

This module should provide title, pause, settings, game-over, and high-score
views as needed. It should convert user selections into clear commands or
state changes while leaving the actual game transitions to the game or engine.
"""
import pygame

def load_button(filename: str) -> pygame.Surface:
    return pygame.image.load(filename)

def load_assets() -> dict[str, pygame.Surface | pygame.font.Font]:
    return {
        "font":       pygame.font.Font(None, 32),
        "header":     pygame.image.load("img/Pac-Man.png"),
        "background": pygame.image.load("img/background.png"),
        "play":       load_button("img/buttons/play.png"),
        "highscores": load_button("img/buttons/highscores.png"),
        "help":       load_button("img/buttons/help.png"),
        "exit":       load_button("img/buttons/exit.png"),
    }
