"""Provide the main runtime loop and low-level game timing.

This module should collect input, advance the game by elapsed time, dispatch
updates to the game state, and request rendering. It should keep frame timing
and event-loop details separate from Pac-Man rules so the game logic remains
testable without a graphical window.
"""
