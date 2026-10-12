# Pac-Man project documentation.

This file should explain the project's purpose, required Python version and
dependencies, installation steps, how to run the game, how to run tests, and
the role of the main source directories. Add configuration and troubleshooting
notes here as the project grows.


Sure. Let's say the ghost is at tile `(5, 5)` and Pac-Man is at `(5, 3)`. The ghost has 3 legal moves: `UP`, `LEFT`, `RIGHT`.

```python
move_deltas = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
```
This just maps each direction to how it changes the grid position. `UP` means `y - 1`, `RIGHT` means `x + 1`, etc.

```python
pac_x = pacman.pixel_x // tile_size
pac_y = pacman.pixel_y // tile_size
```
Convert Pac-Man's pixel coordinates to grid tile coordinates. Same unit as the ghost.

```python
bfs_move = max(
    legal_moves,
    key=lambda d: (ghost_x + move_deltas[d][0] - pac_x) ** 2
                + (ghost_y + move_deltas[d][1] - pac_y) ** 2
)
```

`max(..., key=...)` goes through every legal move and scores it. The **score is the squared distance** between *where the ghost would land* and *Pac-Man's position*. It picks the move with the **highest score** — i.e. the one that puts the ghost farthest away.

For our example:

| Move | Ghost lands at | Distance² from Pac-Man `(5,3)` |
|------|----------------|-------------------------------|
| UP | `(5, 4)` | `(5-5)²+(4-3)²` = **1** |
| LEFT | `(4, 5)` | `(4-5)²+(5-3)²` = **5** |
| RIGHT | `(6, 5)` | `(6-5)²+(5-3)²` = **5** |

`max` picks `LEFT` or `RIGHT` (tie). Ghost moves sideways — away from Pac-Man who is above it. ✅

**Why squared distance and not regular distance?**
`(dx² + dy²)` gives the same *ranking* as `√(dx²+dy²)` but skips the square root, which is slightly faster and avoids floating point.