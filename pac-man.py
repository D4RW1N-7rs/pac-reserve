"""Start the Pac-Man application.

This module is the command-line entry point for the project. It should parse
any launch options, load the game configuration, construct the game object,
and start the main loop. Keep orchestration here; game rules belong in
``src/game.py`` and lower-level timing or input concerns belong in the engine.
"""
# import pygame
# from src.engine import engine_loop
# from src.systems import highscore
# from src.systems.config_loader import load_config


# CONFIG_FILE = "config.json"
# HIGHSCORE_FILE = "data/highscores.json"

# config = load_config(CONFIG_FILE)
# highscores = highscore.load_scores(HIGHSCORE_FILE)

# engine_loop(config, highscores)


from src.game import run

run()