"""Render menus and handle menu selections.

This module should provide title, pause, settings, game-over, and high-score
views as needed. It should convert user selections into clear commands or
state changes while leaving the actual game transitions to the game or engine.
"""
import pygame
from .renderer import draw_rect

def load_button(filename: str) -> pygame.Surface:
    return pygame.image.load(filename)

def load_assets() -> dict[str, pygame.Surface | pygame.font.Font]:
    return {
        "font":       pygame.font.Font(None, 32),
        "help_font":       pygame.font.Font(None, 22),
        "header":     pygame.image.load("img/Pac-Man.png"),
        "scores_header":     pygame.image.load("img/highscores_title.png"),
        "background": pygame.image.load("img/background.png"),
        "scores_background": pygame.image.load("img/scores_background.png"),
        "play":       load_button("img/buttons/play.png"),
        "highscores": load_button("img/buttons/highscores.png"),
        "help":       load_button("img/buttons/help.png"),
        "exit":       load_button("img/buttons/exit.png"),
        "back":       load_button("img/buttons/back.png")
    }

def draw_high_scores(
        window: pygame.Surface, font: pygame.font.Font, 
        scores: list[dict[str, str | int]]) -> None:
    """Draw the high-score table on the given window."""
    sorted_scores = sorted(scores, key=lambda e: e["score"], reverse=True)
    for i in range(10):
        rank = font.render(f"#{i+1}",True,(255, 255, 255))
        y = 120 + i * 40
        window.blit(rank,(200,y))
        if i < len(sorted_scores):
            name = font.render(sorted_scores[i]["name"],True,(255, 255, 255))
            score = font.render(str(sorted_scores[i]["score"]),True,(255, 255, 255))
            window.blit(name,(300,y))
            window.blit(score,(500,y))
        else:
            dots = font.render("---",True,(255, 255, 255))
            window.blit(dots,(300,y))
            window.blit(dots,(500,y))
        if i < 9:
            draw_rect(window, 180, y + 30, 400, 1, (255, 213, 0))

def draw_help(window: pygame.Surface, font: pygame.font.Font) -> None:
    lines = [
    ("CONTROLS",          (255, 200, 0)),
    ("Arrow Keys / WASD : Move", (255, 255, 255)),
    ("P: Pause",           (255, 255, 255)),
    ("OBJECTIVE",         (255, 200, 0)),
    ("Eat all dots to complete the level",  (255, 255, 255)),
    ("Avoid ghosts — you lose a life on contact",  (255, 255, 255)),
    ("Eat a Power Pellet to make ghosts edible",  (255, 255, 255)),
    ("Eat an edible ghost for bonus points",  (255, 255, 255)),
    ("Complete all 3 levels to win",  (255, 255, 255)),
    ("Each level has a time limit — don't be slow!",  (255, 255, 255)),
    ("SCORING",               (255, 200, 0)),
    ("Dot           : +10",   (255, 255, 255)),
    ("Power Pellet  : +100",   (255, 255, 255)),
    ("Ghost         : +200",   (255, 255, 255)),
    ("bonus         : +200",   (255, 255, 255)),
    ("LIVES",               (255, 200, 0)),
    ("# You start with 3 lives",  (255, 255, 255)),
    ("# Respawn in the center after losing a life",  (255, 255, 255)),
    ("# Game over when all lives are lost",  (255, 255, 255)),
    ("CHEATS",               (255, 200, 0)),
    ("1 : Invincibility (no life lost; ghosts cannot eat the player).",  (255, 255, 255)),
    ("2 : Level skip (immediately win the current level).",  (255, 255, 255)),
    ("3 : Ghost freeze (ghosts stop moving).",  (255, 255, 255)),
    ("4 : Extra lives (add extra lives to the player).",  (255, 255, 255)),
    ("5 : Increased speed (player moves faster).",  (255, 255, 255)),

    ]
    for i, (text, color) in enumerate(lines):
        if color is None:
            continue
        line_surface = font.render(text, True, color)
        y = 20 + i * 20
        window.blit(line_surface, (100, y))







