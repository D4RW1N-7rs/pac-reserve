# Retrospective & Blocker Analysis

This document summarizes key challenges encountered during the project, conflicts or technical blocks, and how they were resolved.

---

## 1. Major Blocking Points & Solutions

### Blocker 1: Large Maze Recursion Limit
- **Challenge:** Generating Level 10 ($47 \times 26$ grid) using recursive depth-first search threw `RecursionError: maximum recursion depth exceeded in comparison`.
- **Resolution:** Re-implemented `_generate_maze` in `MazeGenerator` using an explicit stack (`list`) and local generator iterators. This allowed arbitrary maze dimensions without altering Python system recursion limits.

### Blocker 2: Frightened Ghost Flee Logic & Coordinate Desynchronization
- **Challenge:** Initial attempts to make frightened ghosts run away attempted an inverted BFS search that created path loops. Furthermore, switching speeds mid-corridor desynchronized pixel coordinates from the 40-pixel grid, causing ghosts to walk through walls.
- **Resolution:**
  1. Replaced the BFS search with an $O(1)$ squared-distance maximization heuristic.
  2. Applied grid snapping via `round(pixel / tile_size) * tile_size` on state and speed changes.

### Blocker 3: Monolithic `run()` Function Refactoring
- **Challenge:** As features grew, `run()` in `game.py` exceeded 450 lines, interleaving event processing, state changes, physics, and drawing. Coordinating simultaneous code edits led to merge conflicts.
- **Resolution:**
  1. Isolated low-level display and frame timing into `src/engine.py`.
  2. Wrapped game states, levels, and entity management into an object-oriented `PacmanGame` class.
  3. Cleaned `pac-man.py` down to a standard 20-line entry point with `argparse`.

---

## 2. Team Lessons Learned & Takeaways

1. **State Mutation in Draw Loops:** Never alter entity velocity, timers, or states inside `draw()` methods. Separating rendering from state logic prevented several tricky timing bugs.
2. **Deterministic Tile Grids:** Grid-based games require strict alignment whenever entity speed is not an exact divisor of tile size.
3. **Pydantic Validation:** Catching malformed configurations at file-loading time with descriptive messages eliminated dozens of runtime attribute errors during level progression testing.

