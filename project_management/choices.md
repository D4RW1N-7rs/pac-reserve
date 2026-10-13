# Architecture & Technical Choices

This document outlines key technical decisions made during development, alternative approaches considered, and rationales for the chosen designs.

---

## 1. Engine & Game Loop Decoupling

### Context
Initial prototypes concentrated window management, asset loading, event polling, collision physics, and screen rendering inside a single 400+ line function in `game.py`.

### Decision
Extract generic game loop mechanics into `src/engine.py` and encapsulate Pac-Man rules into a `PacmanGame` state coordinator:
- **`src/engine.py`:** Owns display creation, geometry helpers (`point_in_box`, centering), clock capping at 40 FPS, and the top-level event loop.
- **`src/game.py`:** Controls gameplay states (`MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`, `WINNER`), level initialization, and score rules.
- **`pac-man.py`:** Minimal CLI entry point using `argparse`.

### Trade-offs & Rationale
- **Alternative:** Keep everything in a single script.
- **Why rejected:** Difficult to unit test, hard for two developers to work on concurrently without merge conflicts, and violates the single-responsibility principle.

---

## 2. Iterative Depth-First Search with Braid Loops

### Context
Standard DFS maze algorithms generate "perfect" mazes (spanning trees without any loops). In Pac-Man, a player entering a dead-end corridor with a ghost behind them cannot survive.

### Decision
Use iterative DFS with explicit stack allocation (avoiding Python recursion depth errors on grids up to $47 \times 26$), followed by a post-generation **braiding pass**:
- Identifies any cell with 3 walls (dead-ends).
- Carves one wall into an adjacent corridor to introduce loops.
- Preserves the central solid cells representing the "42" pattern (cell value `15`).

---

## 3. Bitmask Wall Representation

### Context
Walls need to be rendered and queried during entity movement dozens of times per frame.

### Decision
Represent cell walls as bit flags:
- `UP = 1` ($2^0$)
- `RIGHT = 2` ($2^1$)
- `DOWN = 4` ($2^2$)
- `LEFT = 8` ($2^3$)

### Rationale
- Movement validation reduces to a single bitwise AND operation: `cell & wall`.
- Wall rendering uses bitwise checks to draw only necessary border lines.

---

## 4. Frightened Ghost Evasion & Grid Modulo Snapping

### Context
When ghosts turn frightened, they must flee Pac-Man. In early builds, ghosts used an inverted BFS call that caused pathfinding inversions. Furthermore, switching from speed 2 px/frame to 4 px/frame caused ghosts to skip tile boundary checks (`pixel % 40 == 0`), clipping out of the maze.

### Decision
1. **Distance-Squared Maximization:** When frightened, ghosts evaluate legal turns and pick the direction maximizing Euclidean squared distance $(dx^2 + dy^2)$ from Pac-Man. This runs in $O(1)$ and avoids floating-point square root operations.
2. **Grid Realignment:** When ghosts exit frightened mode or Pac-Man changes speed via cheats, coordinates are snapped using:
   ```python
   pixel = round(pixel / tile_size) * tile_size
   ```
   This ensures entities lock cleanly back onto grid boundaries, preventing boundary-skipping bugs.

---

## 5. Pydantic-Backed JSON Configuration & Persistence

### Context
The game requires flexible stage tuning and persistent high score records.

### Decision
Use JSON files validated with Pydantic (`BaseModel`):
- `config.json` is validated by `GameConfig` and `LevelConfig` models.
- `data/highscores.json` is validated by `Highscore` models.
- Graceful recovery: missing or corrupt files trigger fallbacks with non-fatal user warnings instead of crashing the game.

