from mazegenerator.mazegenerator import MazeGenerator

# ── Config ────────────────────────────────────────────────────────────────
SIZE = (15, 15)
SEED = 42
# ──────────────────────────────────────────────────────────────────────────

BLUE, RESET = "\x1b[34m", "\x1b[0m"
N, E, S, W = 1, 2, 4, 8

# Junction glyphs indexed by arms: 1=up 2=right 4=down 8=left
GLYPHS = " ║═╚║║╔╠═╝═╩╗╣╦╬"


def render_maze(maze):
    h, w = len(maze), len(maze[0])
    hw, vw, ft = set(), set(), set()  # horizontal walls, vertical walls, "42" cells

    for y in range(h):
        for x in range(w):
            c = maze[y][x]
            if c == 15:                       # the "42": no walls of its own
                ft.add((x, y))
                continue
            if c & N: hw.add((x, y))
            if c & S: hw.add((x, y + 1))
            if c & W: vw.add((x, y))
            if c & E: vw.add((x + 1, y))

    grid = [[" "] * (4 * w + 1) for _ in range(2 * h + 1)]

    for y in range(h + 1):
        for x in range(w + 1):
            arms = (N * ((x, y - 1) in vw) | E * ((x, y) in hw)
                    | S * ((x, y) in vw) | W * ((x - 1, y) in hw))
            grid[2 * y][4 * x] = GLYPHS[arms]
    for x, y in hw:
        grid[2 * y][4 * x + 1:4 * x + 4] = "═══"
    for x, y in vw:
        grid[2 * y + 1][4 * x] = "║"

    for x, y in ft:
        grid[2 * y + 1][4 * x + 1:4 * x + 4] = "███"
        if (x + 1, y) in ft:
            grid[2 * y + 1][4 * x + 4] = "█"
        if (x, y + 1) in ft:
            grid[2 * y + 2][4 * x + 1:4 * x + 4] = "███"
        if {(x + 1, y), (x, y + 1), (x + 1, y + 1)} <= ft:
            grid[2 * y + 2][4 * x + 4] = "█"

    return "\n".join(BLUE + "".join(row) + RESET for row in grid)


if __name__ == "__main__":
    print(f"size: {SIZE[0]} x {SIZE[1]}")
    print(f"seed: {SEED}")
    print()
    print(render_maze(MazeGenerator(size=SIZE, seed=SEED).maze))