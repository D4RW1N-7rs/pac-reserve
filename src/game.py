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
from .ui.hud import draw_hud
from .ui.renderer import draw_maze, draw_rect
from .systems import highscore
from .systems.maze_integration import create_maze
from .systems.config_loader import load_config
from .entities.player import Player

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    HIGH_SCORES = auto()
    HELP = auto()
    PAUSED = auto()
    GAME_OVER = auto()


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
CONFIG_FILE = "config.json"
HIGHSCORE_FILE = "data/highscores.json"

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
    """Calculate the X coordinate to center an image on the screen."""
    return (window_width - image.get_width()) // 2

def centered_y(image: pygame.Surface, window_height: int) -> int:
    """Calculate the Y coordinate to center an image on the screen."""
    return (window_height - image.get_height()) // 2


def find_middle_spawn(maze):
    """Return the nearest valid cell to the maze center for Pac-Man."""
    height = len(maze)
    width = len(maze[0]) if height else 0
    center_x = width // 2
    center_y = height // 2
    start_x, start_y = center_x, center_y

    if maze[center_y][center_x] == 15:
        for radius in range(1, max(width, height)):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx = center_x + dx
                    ny = center_y + dy
                    if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] != 15:
                        return nx, ny
    return start_x, start_y


def run() -> None:
    config = load_config(CONFIG_FILE)
    highscores = highscore.load_config(HIGHSCORE_FILE)

    if not config or not highscores:
        return
    
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
    gameover_image= assets["gameover"]
    save_image= assets["save"]

    play_x = centered_x(play_image, WINDOW_WIDTH)
    play_y = 275
    score_x = centered_x(highscore_image, WINDOW_WIDTH)
    score_y = 335
    help_x = centered_x(help_image, WINDOW_WIDTH)
    help_y = 395
    exit_x = centered_x(exit_image, WINDOW_WIDTH)
    exit_y = 455
    back_x = centered_x(back_image, WINDOW_WIDTH)
    back_y = 520


    current_state = GameState.MENU

    TILE = 35
    HUD_HEIGHT = 60
    PADDING = 16


    score = 0 #get_score()  # Placeholder for actual score retrieval logic
    lives = config["lives"]
    current_level = 1
    level_data = config["levels"][current_level - 1]
    timer = int(level_data.get("level_max_time", 0))
    maze = None
    level_time_remaining = timer
    last_second_tick = time.time()
    error_message = ""
    player_name = ""

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
                        level_time_remaining = int(level_data["level_max_time"])
                        last_second_tick = time.time()
                        maze = create_maze(level_data["width"], level_data["height"], level_data["seed"])
                        new_w = level_data["width"]  * TILE + PADDING * 2
                        new_h = level_data["height"] * TILE + HUD_HEIGHT + PADDING * 2
                        window = create_window(new_w, new_h)
                        start_x, start_y = find_middle_spawn(maze)
                        pacman = Player(start_x, start_y, TILE)
                        level_start_time = time.time()
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
                elif current_state == GameState.GAME_OVER:
                    if point_in_box(px, py, save_x, save_y, save_image.get_width(), save_image.get_height()):
                        existing_names = [dic["name"] for dic in highscores]
                        
                        if len(player_name) < 2:
                            error_message = "NAME MUST BE AT LEAST 2 LETTERS!"
                        elif player_name in existing_names:
                            error_message = "NAME ALREADY EXISTS!"
                        else:
                            highscore.save_highscore(HIGHSCORE_FILE, player_name, score)
                            window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
                            current_state = GameState.MENU
                            error_message = ""

            if current_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        existing_names = [dic["name"] for dic in highscores]

                        if len(player_name) < 2:
                            error_message = "NAME MUST BE AT LEAST 2 LETTERS!"
                        elif player_name in existing_names:
                            error_message = "NAME ALREADY EXISTS!"
                        else:
                            highscore.save_highscore(HIGHSCORE_FILE, player_name, score)
                            window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
                            current_state = GameState.MENU
                            error_message = ""
                    else:
                        if len(player_name) <= 10 and (event.unicode.isalnum() or event.unicode == " "):
                            player_name += event.unicode

            if current_state == GameState.PLAYING:
                pacman.handle_input(event)


        if current_state == GameState.MENU:
            window.blit(background_image, (0, 0))
            window.blit(header_image, (150, -150))
            window.blit(play_image,      (play_x,  play_y))
            window.blit(highscore_image, (score_x, score_y))
            window.blit(help_image,      (help_x,  help_y))
            window.blit(exit_image,      (exit_x,  exit_y))

        elif current_state == GameState.PLAYING:
            now = time.time()
            time_since_start = now - level_start_time

            if time_since_start < 3.0:
                # --- WE ARE STILL COUNTING DOWN ---
                window.fill(BACKGROUND_COLOR)
                level = font.render(f"level: {current_level}", True, (212, 149, 1))
                window.blit(level, (centered_x(level, new_w), centered_y(level, new_h)))
                
                seconds_left = 3 - int(time_since_start)
                count_down = font.render(f"{seconds_left}", True, (212, 149, 1))
                window.blit(count_down, (centered_x(count_down, new_w), centered_y(count_down, new_h + 100)))

                last_second_tick = now 
                
            else:
                # --- COUNTDOWN FINISHED, PLAY THE GAME! ---
                pacman.update(maze, TILE)
                if now - last_second_tick >= 1.0:
                    level_time_remaining = max(0, level_time_remaining - 1)
                    last_second_tick = now
                    
                timer = level_time_remaining
                window.fill(BACKGROUND_COLOR)
                draw_maze(window, maze, TILE)
                draw_hud(window, font, current_level, score, lives, pac_head_image, timer)
                pacman.draw(window, PADDING, HUD_HEIGHT, TILE)
                
                if timer <= 0:
                    current_state = GameState.GAME_OVER
                    player_name = ""
            

        elif current_state == GameState.HIGH_SCORES:
            window.blit(scores_background, (0, 0))
            window.blit(scores_header, (centered_x(scores_header, WINDOW_WIDTH), 20))
            highscores = highscore.load_config(HIGHSCORE_FILE)
            menus.draw_high_scores(window,font,highscores)
            window.blit(back_image, (back_x,back_y))

        elif current_state == GameState.HELP:
            window.fill(BACKGROUND_COLOR)
            menus.draw_help(window, help_font)
            window.blit(back_image, (back_x,back_y))

        elif current_state == GameState.GAME_OVER:
            save_x = centered_x(save_image, new_w)
            save_y = centered_y(save_image, new_h + 400)
            window.fill((212, 149, 1))
            window.blit(gameover_image, (centered_x(gameover_image, new_w), centered_y(gameover_image, new_h)))
            window.blit(save_image, (save_x, save_y))
            enter_name = font.render("Enter your name", True, (0, 0, 0))
            window.blit(enter_name, (centered_x(enter_name, new_w), centered_y(enter_name, new_h + 120)))

            rect_w = 300
            rect_h = 50
            rect_x = (new_w - rect_w) // 2
            rect_y = (new_h + 220 - rect_h) // 2
            draw_rect(window, rect_x, rect_y, rect_w, rect_h, (0, 0, 0))

            text_surface = font.render(player_name, True, (255, 255, 255))
            window.blit(text_surface, (centered_x(text_surface, new_w), centered_y(text_surface, new_h + 220)))
            if error_message != "":
                name_error = font.render(error_message, True, (255, 0, 0))
                window.blit(name_error, (centered_x(name_error, new_w), centered_y(name_error, new_h + 300)))

        pygame.display.flip()

        elapsed = time.time() - frame_start
        sleep_time = (1 / FPS) - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    pygame.quit()


