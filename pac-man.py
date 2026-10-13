"""Start the Pac-Man application.

This module is the command-line entry point for the project. It loads
configuration, constructs the Pac-Man game instance, and hands execution
over to the engine run loop.
"""

from src.systems.config_loader import load_config
from src.systems import highscore
from src.game import PacmanGame
from src.engine import run_loop
import argparse

CONFIG_FILE = "config.json"
HIGHSCORE_FILE = "data/highscores.json"


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    arg_parser = argparse.ArgumentParser(description="Pac-Man Game.")
    arg_parser.add_argument(
        "config_file",
        type=str,
        nargs="?",
        default=CONFIG_FILE,
        help="Path to the JSON configuration file.",
    )
    return arg_parser.parse_args()


def main() -> None:
    """Parse CLI arguments, load config and highscores, and run the game."""
    args = parse_arguments()
    config = load_config(args.config_file)
    highscore_file = (
        config.get("highscore_filename", HIGHSCORE_FILE)
        if config
        else HIGHSCORE_FILE
    )
    highscores = highscore.load_scores(highscore_file)
    if not config or highscores is None:
        return

    game = PacmanGame(config=config, highscores=highscores)
    run_loop(game)


if __name__ == "__main__":
    main()
