"""Coordinate the Pac-Man game state, entities, and rules.

This module manages game state transitions, levels, scores, lives, player,
ghosts, collectibles, countdown/level timers, event handling, and drawing.
"""

from typing import Any
import pygame
import time
from enum import Enum, auto

from .ui import menus
from .ui.hud import draw_hud
from .ui.renderer import draw_maze, draw_rect, draw_collectibles
from .systems import highscore
from .systems.maze_integration import create_maze
from .systems.config_loader import load_config
from .entities.player import Player
from .entities.collectible import Collectible
from .entities.ghost import Ghost
from .engine import (
    create_window,
    point_in_box,
    centered_x,
    centered_y,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


class GameState(Enum):
    """Enumeration of active game scenes and execution states."""
    MENU = auto()
    PLAYING = auto()
    HIGH_SCORES = auto()
    HELP = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    WINNER = auto()


BACKGROUND_COLOR = (0, 0, 0)
CONFIG_FILE = "config.json"
HIGHSCORE_FILE = "data/highscores.json"
TILE = 40
HUD_HEIGHT = 60
PADDING = 16


def find_middle_spawn(maze: list[list[int]]) -> tuple[int, int]:
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
                    if (
                        0 <= nx < width
                        and 0 <= ny < height
                        and maze[ny][nx] != 15
                    ):
                        return nx, ny
    return start_x, start_y


def eat_collectibles(
    pacman: Player,
    gums: list[Collectible],
    super_gums: list[Collectible],
    tile_size: int,
) -> tuple[int, bool]:
    """Check if Pac-Man has eaten any collectibles and update the score."""
    cell_x = (pacman.pixel_x + tile_size // 2) // tile_size
    cell_y = (pacman.pixel_y + tile_size // 2) // tile_size

    points = 0
    super_eaten = False

    for gum in gums:
        if gum.visible and gum.x == cell_x and gum.y == cell_y:
            gum.visible = False
            points += gum.points

    for s_gum in super_gums:
        if s_gum.visible and s_gum.x == cell_x and s_gum.y == cell_y:
            s_gum.visible = False
            points += s_gum.points
            super_eaten = True

    return points, super_eaten


class PacmanGame:
    """Main controller managing Pac-Man game state, entities, and scenes."""

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        highscores: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize window, assets, configurations, and game state."""
        self.config = (
            config if config is not None else load_config(CONFIG_FILE)
        )
        self.highscore_file = (
            self.config.get("highscore_filename", HIGHSCORE_FILE)
            if self.config
            else HIGHSCORE_FILE
        )
        self.highscores = (
            highscores
            if highscores is not None
            else highscore.load_scores(self.highscore_file)
        )
        if self.highscores is None:
            self.highscores = []

        self.running = True
        self.window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.current_state = GameState.MENU

        # Assets
        self.assets = menus.load_assets()
        self.font = self.assets["font"]
        self.help_font = self.assets["help_font"]

        # Menu button positions
        self.play_x = centered_x(self.assets["play"], WINDOW_WIDTH)
        self.play_y = 275
        self.score_x = centered_x(self.assets["highscores"], WINDOW_WIDTH)
        self.score_y = 335
        self.help_x = centered_x(self.assets["help"], WINDOW_WIDTH)
        self.help_y = 395
        self.exit_x = centered_x(self.assets["exit"], WINDOW_WIDTH)
        self.exit_y = 455
        self.back_x = centered_x(self.assets["back"], WINDOW_WIDTH)
        self.back_y = 520

        # Gameplay state
        self.score = 0
        self.lives = self.config["lives"] if self.config else 3
        self.current_level = 1
        self.level_data: dict[str, Any] = {}
        self.timer = 0
        self.level_time_remaining = 0
        self.last_second_tick = time.time()
        self.level_start_time = 0.0

        # Maze & Entities
        self.maze: list[list[int]] = []
        self.new_w = WINDOW_WIDTH
        self.new_h = WINDOW_HEIGHT
        self.ghosts: list[Ghost] = []
        self.pacman: Player = Player(0, 0, TILE)
        self.gums: list[Collectible] = []
        self.super_gums: list[Collectible] = []

        # UI & Input state
        self.error_message = ""
        self.player_name = ""
        self.eaten_points_popup: (
            tuple[pygame.Surface, tuple[int, int], float] | None
        ) = None

        # Cheats
        self.invincible = False
        self.ghosts_frozen = False

    def start_level(self, level_index: int) -> None:
        """Initialize maze, entities, and window size for the given level."""
        levels = self.config["levels"]
        self.level_data = (
            levels[level_index] if level_index < len(levels) else levels[-1]
        )
        maze = create_maze(
            self.level_data["width"],
            self.level_data["height"],
            self.level_data["seed"],
        )
        self.maze = maze if maze is not None else []

        self.new_w = self.level_data["width"] * TILE + PADDING * 2
        self.new_h = (
            self.level_data["height"] * TILE + HUD_HEIGHT + PADDING * 2
        )

        self.ghosts = [
            Ghost(1, 1, TILE, "red"),
            Ghost(self.level_data["width"] - 2, 1, TILE, "cyan"),
            Ghost(1, self.level_data["height"] - 2, TILE, "orange"),
            Ghost(
                self.level_data["width"] - 2,
                self.level_data["height"] - 2,
                TILE,
                "pink",
            ),
        ]

        start_x, start_y = find_middle_spawn(self.maze)
        self.pacman = Player(start_x, start_y, TILE)

        self.gums, self.super_gums = Collectible.generate_gums(
            self.maze,
            self.level_data["width"],
            self.level_data["height"],
            self.config["pacgum"],
            self.config["points_per_pacgum"],
            self.config["points_per_super_pacgum"],
        )

        self.level_time_remaining = int(self.level_data["level_max_time"])
        self.timer = self.level_time_remaining
        self.last_second_tick = time.time()
        self.level_start_time = time.time()
        self.window = create_window(self.new_w, self.new_h)

    def respawn_after_death(self) -> None:
        """Reset player and ghost positions after losing a life."""
        time.sleep(1)
        if not self.level_data:
            return
        self.ghosts = [
            Ghost(1, 1, TILE, "red"),
            Ghost(self.level_data["width"] - 2, 1, TILE, "cyan"),
            Ghost(1, self.level_data["height"] - 2, TILE, "orange"),
            Ghost(
                self.level_data["width"] - 2,
                self.level_data["height"] - 2,
                TILE,
                "pink",
            ),
        ]
        start_x, start_y = find_middle_spawn(self.maze)
        self.pacman = Player(start_x, start_y, TILE)

    def save_player_score(self) -> None:
        """Validate and save player high score."""
        existing_names = [dic["name"] for dic in self.highscores]
        if len(self.player_name) < 2:
            self.error_message = "NAME MUST BE AT LEAST 2 LETTERS!"
        elif self.player_name in existing_names:
            self.error_message = "NAME ALREADY EXISTS!"
        else:
            highscore.save_highscore(
                self.highscore_file, self.player_name, self.score
            )
            self.highscores = highscore.load_scores(self.highscore_file)
            self.window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.current_state = GameState.MENU
            self.error_message = ""
            self.player_name = ""

    # ==========================
    # EVENT HANDLING
    # ==========================
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Dispatch incoming pygame events to appropriate handlers."""
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)

    def handle_mouse_click(self, pos: tuple[int, int]) -> None:
        """Handle mouse click interactions across all UI screens."""
        px, py = pos

        if self.current_state == GameState.MENU:
            if point_in_box(
                px,
                py,
                self.play_x,
                self.play_y,
                self.assets["play"].get_width(),
                self.assets["play"].get_height(),
            ):
                self.current_level = 1
                self.score = 0
                self.lives = self.config["lives"]
                self.start_level(self.current_level - 1)
                self.current_state = GameState.PLAYING
            elif point_in_box(
                px,
                py,
                self.help_x,
                self.help_y,
                self.assets["help"].get_width(),
                self.assets["help"].get_height(),
            ):
                self.current_state = GameState.HELP
            elif point_in_box(
                px,
                py,
                self.score_x,
                self.score_y,
                self.assets["highscores"].get_width(),
                self.assets["highscores"].get_height(),
            ):
                self.current_state = GameState.HIGH_SCORES
            elif point_in_box(
                px,
                py,
                self.exit_x,
                self.exit_y,
                self.assets["exit"].get_width(),
                self.assets["exit"].get_height(),
            ):
                self.running = False

        elif self.current_state in (GameState.HIGH_SCORES, GameState.HELP):
            if point_in_box(
                px,
                py,
                self.back_x,
                self.back_y,
                self.assets["back"].get_width(),
                self.assets["back"].get_height(),
            ):
                self.current_state = GameState.MENU

        elif self.current_state in (GameState.GAME_OVER, GameState.WINNER):
            save_img = self.assets["save"]
            save_x = centered_x(save_img, self.new_w)
            save_y = centered_y(save_img, self.new_h + 400)
            if point_in_box(
                px, py, save_x, save_y,
                save_img.get_width(), save_img.get_height()
            ):
                self.save_player_score()

        elif self.current_state == GameState.PAUSED:
            cont_img = self.assets["continue"]
            menu_img = self.assets["menu"]
            continue_x = centered_x(cont_img, self.new_w)
            continue_y = centered_y(cont_img, self.new_h)
            menu_x = centered_x(menu_img, self.new_w)
            menu_y = centered_y(menu_img, self.new_h) + 80

            if point_in_box(
                px,
                py,
                continue_x,
                continue_y,
                cont_img.get_width(),
                cont_img.get_height(),
            ):
                self.current_state = GameState.PLAYING
            elif point_in_box(
                px, py, menu_x, menu_y,
                menu_img.get_width(), menu_img.get_height()
            ):
                self.window = create_window(WINDOW_WIDTH, WINDOW_HEIGHT)
                self.current_state = GameState.MENU

    def handle_key_down(self, event: pygame.event.Event) -> None:
        """Handle keyboard events based on the current game state."""
        if self.current_state in (GameState.GAME_OVER, GameState.WINNER):
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            elif event.key == pygame.K_RETURN:
                self.save_player_score()
            else:
                if len(self.player_name) < 10 and (
                    event.unicode.isalnum() or event.unicode == " "
                ):
                    self.player_name += event.unicode

        elif self.current_state == GameState.PLAYING:
            self.pacman.handle_input(event)
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.window = create_window(self.new_w, self.new_h)
                self.current_state = GameState.PAUSED
            else:
                self.apply_cheat(event.key)

        elif self.current_state == GameState.PAUSED:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.window = create_window(self.new_w, self.new_h)
                self.current_state = GameState.PLAYING

    def apply_cheat(self, key: int) -> None:
        """Apply cheats: 1=invincible, 2=skip, 3=freeze, 4=lives, 5=speed."""
        if key in (pygame.K_1, pygame.K_KP1):
            self.invincible = not self.invincible
            status = "ON" if self.invincible else "OFF"
            print(f"[CHEAT] Invincibility: {status}")
        elif key in (pygame.K_2, pygame.K_KP2):
            print("[CHEAT] Level skip!")
            for gum in self.gums:
                gum.visible = False
            for sgum in self.super_gums:
                sgum.visible = False
        elif key in (pygame.K_3, pygame.K_KP3):
            self.ghosts_frozen = not self.ghosts_frozen
            status = "ON" if self.ghosts_frozen else "OFF"
            print(f"[CHEAT] Ghost freeze: {status}")
        elif key in (pygame.K_4, pygame.K_KP4):
            self.lives += 1
            print(f"[CHEAT] Extra life! Lives: {self.lives}")
        elif key in (pygame.K_5, pygame.K_KP5):
            self.pacman.speed = 8 if self.pacman.speed == 5 else 5
            # Snap to nearest tile boundary to re-align with grid modulo checks
            self.pacman.pixel_x = round(self.pacman.pixel_x / TILE) * TILE
            self.pacman.pixel_y = round(self.pacman.pixel_y / TILE) * TILE
            print(f"[CHEAT] Player speed: {self.pacman.speed}")

    # ==========================
    # UPDATE / LOGIC
    # ==========================
    def update(self) -> None:
        """Update gameplay logic, timers, positions, and collisions."""
        if self.current_state != GameState.PLAYING:
            return

        now = time.time()
        time_since_start = now - self.level_start_time

        # 3-second countdown before round starts
        if time_since_start < 3.0:
            self.last_second_tick = now
            return

        self.pacman.update(self.maze, TILE)

        points_won, super_eaten = eat_collectibles(
            self.pacman, self.gums, self.super_gums, TILE
        )
        self.score += points_won

        if super_eaten:
            for ghost in self.ghosts:
                ghost.frighten()

        if now - self.last_second_tick >= 1.0:
            self.level_time_remaining = max(0, self.level_time_remaining - 1)
            self.last_second_tick = now

        self.timer = self.level_time_remaining

        # Update ghosts & check collision
        for ghost in self.ghosts:
            if not self.ghosts_frozen:
                ghost.update(self.maze, TILE, self.pacman)

            if ghost.collide(self.pacman):
                if ghost.state == "FRIGHTENED":
                    pts = self.config.get("points_per_ghost", 200)
                    self.score += pts
                    ghost.state = "EATEN"
                    popup_surf = self.font.render(
                        f"+{pts}", True, (255, 255, 255)
                    )
                    popup_pos = (
                        ghost.pixel_x + PADDING,
                        ghost.pixel_y + HUD_HEIGHT + PADDING,
                    )
                    self.eaten_points_popup = (
                        popup_surf, popup_pos, time.time() + 1.0
                    )
                elif not self.invincible:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.current_state = GameState.GAME_OVER
                        self.player_name = ""
                        time.sleep(1)
                        break
                    else:
                        self.respawn_after_death()
                        break

        # Check level completion
        if not any(gum.visible for gum in self.gums) and not any(
            sgum.visible for sgum in self.super_gums
        ):
            self.current_level += 1
            if self.current_level > len(self.config["levels"]):
                self.current_state = GameState.WINNER
                self.player_name = ""
            else:
                self.start_level(self.current_level - 1)

        # Check timer expiry
        if self.timer <= 0 and self.current_state == GameState.PLAYING:
            self.current_state = GameState.GAME_OVER
            self.player_name = ""

    # ==========================
    # DRAWING / RENDERING
    # ==========================
    def draw(self) -> None:
        """Render the active game state scene to the window."""
        if self.current_state == GameState.MENU:
            self.draw_menu()
        elif self.current_state == GameState.PLAYING:
            self.draw_playing()
        elif self.current_state == GameState.HIGH_SCORES:
            self.draw_highscores()
        elif self.current_state == GameState.HELP:
            self.draw_help()
        elif self.current_state in (GameState.GAME_OVER, GameState.WINNER):
            self.draw_gameover_or_winner()
        elif self.current_state == GameState.PAUSED:
            self.draw_paused()

    def draw_menu(self) -> None:
        """Render the main menu buttons, title header, and background."""
        self.window.blit(self.assets["background"], (0, 0))
        self.window.blit(self.assets["header"], (150, -150))
        self.window.blit(self.assets["play"], (self.play_x, self.play_y))
        self.window.blit(
            self.assets["highscores"], (self.score_x, self.score_y)
        )
        self.window.blit(self.assets["help"], (self.help_x, self.help_y))
        self.window.blit(self.assets["exit"], (self.exit_x, self.exit_y))

    def draw_playing(self) -> None:
        """Render maze, countdown, collectibles, HUD, and entities."""
        now = time.time()
        time_since_start = now - self.level_start_time

        if time_since_start < 3.0:
            self.window.fill(BACKGROUND_COLOR)
            level_text = self.font.render(
                f"level: {self.current_level}", True, (212, 149, 1)
            )
            self.window.blit(
                level_text,
                (
                    centered_x(level_text, self.new_w),
                    centered_y(level_text, self.new_h),
                ),
            )

            seconds_left = 3 - int(time_since_start)
            count_down = self.font.render(
                f"{seconds_left}", True, (212, 149, 1)
            )
            self.window.blit(
                count_down,
                (
                    centered_x(count_down, self.new_w),
                    centered_y(count_down, self.new_h + 100),
                ),
            )
            return

        self.window.fill(BACKGROUND_COLOR)
        draw_maze(self.window, self.maze, TILE)
        draw_collectibles(
            self.window,
            self.gums,
            self.super_gums,
            self.assets["pacgum"],
            self.assets["super-pacgum"],
            TILE,
            PADDING,
            HUD_HEIGHT,
        )
        draw_hud(
            self.window,
            self.font,
            self.current_level,
            self.score,
            self.lives,
            self.assets["small_pac"],
            self.timer,
        )
        self.pacman.draw(self.window, PADDING, HUD_HEIGHT, TILE)

        for ghost in self.ghosts:
            ghost.draw(self.window, PADDING, HUD_HEIGHT, TILE)

        if self.eaten_points_popup:
            popup_surf, popup_pos, end_time = self.eaten_points_popup
            if time.time() < end_time:
                self.window.blit(popup_surf, popup_pos)
            else:
                self.eaten_points_popup = None

    def draw_highscores(self) -> None:
        """Render the high scores leaderboard view and back button."""
        self.window.blit(self.assets["scores_background"], (0, 0))
        scores_header = self.assets["scores_header"]
        self.window.blit(
            scores_header, (centered_x(scores_header, WINDOW_WIDTH), 20)
        )
        menus.draw_high_scores(self.window, self.font, self.highscores)
        self.window.blit(self.assets["back"], (self.back_x, self.back_y))

    def draw_help(self) -> None:
        """Render the help and instructions screen."""
        self.window.fill(BACKGROUND_COLOR)
        menus.draw_help(self.window, self.help_font)
        self.window.blit(self.assets["back"], (self.back_x, self.back_y))

    def draw_gameover_or_winner(self) -> None:
        """Render game over or victory screen with name input."""
        save_img = self.assets["save"]
        save_x = centered_x(save_img, self.new_w)
        save_y = centered_y(save_img, self.new_h + 400)
        self.window.fill((212, 149, 1))

        if self.current_state == GameState.GAME_OVER:
            title_img = self.assets["gameover"]
            self.window.blit(
                title_img,
                (
                    centered_x(title_img, self.new_w),
                    centered_y(title_img, self.new_h),
                ),
            )
        else:
            title_img = self.assets["winner"]
            self.window.blit(
                title_img,
                (
                    centered_x(title_img, self.new_w),
                    centered_y(title_img, self.new_h - 80),
                ),
            )

        self.window.blit(save_img, (save_x, save_y))
        enter_name = self.font.render("Enter your name", True, (0, 0, 0))
        self.window.blit(
            enter_name,
            (
                centered_x(enter_name, self.new_w),
                centered_y(enter_name, self.new_h + 120),
            ),
        )

        rect_w, rect_h = 300, 50
        rect_x = (self.new_w - rect_w) // 2
        rect_y = (self.new_h + 220 - rect_h) // 2
        draw_rect(self.window, rect_x, rect_y, rect_w, rect_h, (0, 0, 0))

        text_surface = self.font.render(
            self.player_name, True, (255, 255, 255)
        )
        self.window.blit(
            text_surface,
            (
                centered_x(text_surface, self.new_w),
                centered_y(text_surface, self.new_h + 220),
            ),
        )

        if self.error_message:
            name_error = self.font.render(
                self.error_message, True, (255, 0, 0)
            )
            self.window.blit(
                name_error,
                (
                    centered_x(name_error, self.new_w),
                    centered_y(name_error, self.new_h + 300),
                ),
            )

    def draw_paused(self) -> None:
        """Render pause screen overlay with resume and menu options."""
        cont_img = self.assets["continue"]
        menu_img = self.assets["menu"]
        continue_x = centered_x(cont_img, self.new_w)
        continue_y = centered_y(cont_img, self.new_h)
        menu_x = centered_x(menu_img, self.new_w)
        menu_y = centered_y(menu_img, self.new_h) + 80

        self.window.fill((212, 149, 1))
        self.window.blit(
            self.assets["pause"],
            (centered_x(self.assets["pause"], self.new_w), -100),
        )
        self.window.blit(cont_img, (continue_x, continue_y))
        self.window.blit(menu_img, (menu_x, menu_y))


def run() -> None:
    """Legacy entry point: constructs PacmanGame and runs via engine."""
    from .engine import run_loop

    game = PacmanGame()
    run_loop(game)
