"""Provide the main runtime loop and low-level game timing.

This module should collect input, advance the game by elapsed time, dispatch
updates to the game state, and request rendering. It should keep frame timing
and event-loop details separate from Pac-Man rules so the game logic remains
testable without a graphical window.
"""


# import pygame
# import time

# from src.game import run

# FPS = 40
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600



# def engine_loop(config, highscores) -> None:
#     """Run the main game loop, calling update and render functions."""
#     pygame.init()
#     window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#     pygame.display.set_caption("PAC-MAN")
#     frame_start = time.time()

#     running = True

#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
        
#             run(config, highscores, event, window)


#         # Control the frame rate
#         pygame.display.flip()
        
#         elapsed = time.time() - frame_start
#         sleep_time = (1 / FPS) - elapsed
#         if sleep_time > 0:
#             time.sleep(sleep_time)

#     pygame.quit()

