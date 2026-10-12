*This project has been created as part of the 42 curriculum by ohariss, oissfoul.*

# Pac-Man

## Description

This project is a recreation of the classic arcade game **Pac-Man**, implemented in Python with Pygame for the 42 curriculum. The objective of the game is to guide Pac-Man through a maze to consume all pac-gums and super pac-gums while evading four ghosts, each equipped with its own pursuit artificial intelligence.

Key highlights of the project:
- **Procedurally Generated Mazes:** Uses an adapted maze generator creating non-perfect (braided) mazes to eliminate dead-ends, embedding the iconic "42" pattern as a central obstacle.
- **Classic Ghost AI Personalities:** Individual pathfinding behaviors for all four ghosts (Blinky, Pinky, Inky, and Clyde), complete with Frightened and Eaten states.
- **Configurable Levels & Highscores:** 10 distinct level stages configured via JSON, persistent high-score ranking, dynamic window resizing, and complete menu interfaces.

---

## Instructions

### Compilation & Installation

The project requires Python 3.10 or higher. Install the dependencies using `pip`:
```bash
pip install -r requirements.txt
```
Or use the Makefile helper:
```bash
make install
```

### Execution

Launch the game with the default configuration (`config.json`):
```bash
python3 pac-man.py
```
You can also pass a custom configuration file as an argument:
```bash
python3 pac-man.py config.json
```
Or execute using the Makefile:
```bash
make run
```

### Controls
- **Arrow Keys / WASD:** Move Pac-Man Up, Down, Left, or Right.
- **P / Escape:** Pause / Resume the game.
- **Alphanumeric keys / Backspace / Enter:** Input and submit your name on Game Over and Victory screens.

### Cheat Mode (Evaluation & Testing)
Press the corresponding number key during gameplay to toggle or activate cheats:
- <kbd>1</kbd>: **Invincibility** — Toggle on/off (Pac-Man cannot lose lives to ghosts).
- <kbd>2</kbd>: **Level Skip** — Instantly clears all dots and wins the current level.
- <kbd>3</kbd>: **Ghost Freeze** — Toggle ghost movement on/off.
- <kbd>4</kbd>: **Extra Lives** — Grants +1 life to the player.
- <kbd>5</kbd>: **Increased Speed** — Toggles Pac-Man between normal speed (5 px/frame) and high speed (8 px/frame) with automatic tile realignment.

---

## Configuration

Settings and level profiles are loaded from a JSON configuration file (`config.json`) validated via Pydantic schemas.

### Top-Level Configuration

| Key | Type | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `highscore_filename` | `str` | `"data/highscore.json"` | Path to the persistent high-scores JSON file. |
| `lives` | `int` | `3` | Initial number of lives given to the player. |
| `pacgum` | `int` | `1` (or `420`) | Max pellet count ratio/density in walkable corridors. |
| `points_per_pacgum` | `int` | `10` | Score points rewarded for each pac-gum eaten. |
| `points_per_super_pacgum` | `int` | `50` | Score points rewarded for each energizer super pac-gum. |
| `points_per_ghost` | `int` | `200` | Score points rewarded for eating a frightened ghost. |
| `levels` | `list` | 10 level configs | Array containing configuration parameters for all 10 stages. |

### Level Schema
Each level entry inside `levels` configures:
- `level` (`int`): Level index number (1 to 10).
- `seed` (`int`): Random seed producing deterministic maze layout generation.
- `width` (`int`): Grid width in cells.
- `height` (`int`): Grid height in cells.
- `level_max_time` (`int`): Time limit (in seconds) to complete the level before Game Over.

---

## Highscore

### How the Highscore System Works
- **Storage:** High scores are stored in a dedicated JSON file (`data/highscores.json`).
- **Submission:** Upon game termination (either losing all lives or beating all 10 levels), the player enters a nickname (between 2 and 10 alphanumeric characters).
- **Validation & Ranking:** The system ensures unique player names, sorts scores in descending order, and displays the top 10 on the High Scores screen.
- **Data Protection:** Data parsing is backed by Pydantic schema validation (`Highscore` model) to handle missing files, corrupted syntax, or malformed entries gracefully without crashing.

### Why This Design Was Implemented
JSON was chosen because it is human-readable, portable across platforms, and easy to inspect. Backing it with Pydantic ensures data integrity, safe error recovery on missing files, and a strict separation of persistent storage from rendering logic.

---

## Maze Generation

The game integrates the assigned `mazegenerator` package (wrapped in `src/systems/maze_integration.py`):
1. **Iterative DFS Carving:** Carves the maze path using an explicit stack rather than recursion, eliminating the risk of exceeding Python's recursion limit on large grids.
2. **Central "42" Logo:** Prior to carving paths, an isolated "42" pattern (cells with value `15`) is embedded in the center of the maze as an unenterable obstacle block.
3. **Braiding (`perfect=False`):** Standard depth-first search mazes are "perfect" trees containing numerous dead-ends. A player trapped in a dead-end would have no escape from chasing ghosts. The braiding routine identifies cells with three walls and removes one wall into an adjacent corridor, creating loops and multiple viable traversal paths.
4. **Bitmask Wall Representation:** Each cell uses a 4-bit bitmask (`UP = 1`, `RIGHT = 2`, `DOWN = 4`, `LEFT = 8`). Wall collisions are determined through fast bitwise operations (`cell & wall_bit`).

---

## Implementation

### Game Loop & Engine Timing
- Implemented in `src/engine.py` with `pygame.time.Clock()` locked at 40 FPS.
- Decouples input collection, timing, game logic updates, and visual rendering.

### Ghost AI Personalities
Each ghost calculates its decisions when aligned with tile boundaries:
- 🔴 **Blinky (Red):** Direct chaser; runs Breadth-First Search (BFS) directly to Pac-Man's tile.
- 🩷 **Pinky (Pink):** Ambusher; aims for a target tile 4 steps ahead of Pac-Man's heading direction.
- 🩵 **Inky (Cyan):** Flanker; coordinates an angle behind Pac-Man to trap the player.
- 🟠 **Clyde (Orange):** Roamer; pursues Pac-Man when far away ($> 4$ tiles) and retreats to the bottom-left corner when near.

### State Transitions & Grid Snapping
- **Frightened State:** Consuming a super pac-gum activates frightened mode for 7 seconds. Ghosts slow down and flee by choosing moves that maximize squared Euclidean distance away from Pac-Man.
- **Grid Snapping:** When the frightened timer ends and ghosts resume normal speed, their coordinates are re-aligned to the nearest tile using `round(pos / tile_size) * tile_size`. This prevents speed changes from causing off-by-one pixel misalignment that could skip wall checks.
- **Anti-Stacking:** When making turns at intersections, ghosts detect if another ghost already occupies the destination tile, redirecting to alternate open corridors to prevent sprite merging.

---

## General Software Architecture

The project adheres to a clean modular architecture:

```
pacman/
├── pac-man.py                 # CLI entry point (argparse)
├── config.json                # Game configuration & level profiles
├── Makefile                   # Build, run, clean, and lint rules
├── requirements.txt           # Python dependencies
├── data/                      # Persistent storage (highscores.json)
├── mazegenerator/             # Maze generation package (DFS, braiding, shortest path)
│   └── mazegenerator.py
└── src/
    ├── engine.py              # Window management, math helpers, and main run loop
    ├── game.py                # PacmanGame class & gameplay state coordinator
    ├── entities/              # Entity classes
    │   ├── player.py          # Player movement, input, and animation
    │   ├── ghost.py           # Ghost AI targeting, BFS, collision, and states
    │   └── collectible.py     # Pac-gums and super pac-gums generation
    ├── systems/               # Configuration and persistence systems
    │   ├── config_loader.py   # Pydantic JSON config loader and validator
    │   ├── highscore.py       # High score record management and sorting
    │   └── maze_integration.py# Bridge between mazegenerator and game grid
    └── ui/                    # Graphical user interface and rendering
        ├── renderer.py        # Maze wall drawing and collectible rendering
        ├── hud.py             # In-game HUD (score, lives, level, timer)
        └── menus.py           # Menus (Title, High Scores, Help, Game Over, Pause)
```

### Module Relationships
- **`pac-man.py`** parses command-line arguments and passes validated configuration to **`PacmanGame`** (`src/game.py`), handing control over to **`run_loop()`** (`src/engine.py`).
- **`PacmanGame`** owns the game state machine (`MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`, `WINNER`), advances physics/collisions, and delegates drawing tasks to **`src/ui/`**.
- **`Ghost`** and **`Player`** interact with the bitmask grid generated by **`maze_integration.py`**, keeping game physics decoupled from rendering code.

---

## Project Management

- **Methodology:** The project was developed collaboratively using pair programming, feature branching, and iterative milestones.
- **Milestones:**
  1. Maze generator integration and bitmask rendering.
  2. Player movement, grid constraints, and collectible generation.
  3. Ghost pathfinding algorithms (BFS) and behavioral states.
  4. State machine refactoring, engine decoupling, and menu UI.
- **Dedicated Directory:** Scratch scripts, experiment logs, visual architecture sketches (`t.excalidraw`), and unit tests are organized inside the dedicated project management and testing directory [`.testing/`](file:///home/ohariss/Desktop/pacman/.testing) and [`.tests/`](file:///home/ohariss/Desktop/pacman/.tests).

---

## Resources

### References & Documentation
- **Pygame Documentation:** https://www.pygame.org/docs/
- **The Pac-Man Dossier (Jamey Pittman):** Canonical reference for arcade Pac-Man logic, AI targeting tiles, and timing: https://pacman.holycow.us/
- **Maze Generation Algorithms (Jamis Buck):** Comprehensive reference on maze generation, braid mazes, and graph traversal: http://weblog.jamisbuck.org/

### AI Usage Description
AI assistance was used throughout development as a collaborative pair-programming partner: explaining BFS algorithm and Pygame mechanics, reviewing, and debugging hand-written code. All code in this repository was written, tested, and is understood by the authors.

