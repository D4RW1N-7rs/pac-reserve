"""Start the Pac-Man application.

This module is the command-line entry point for the project. It should parse
any launch options, load the game configuration, construct the game object,
and start the main loop. Keep orchestration here; game rules belong in
``src/game.py`` and lower-level timing or input concerns belong in the engine.
"""
import pygame
from src.game import run

run()