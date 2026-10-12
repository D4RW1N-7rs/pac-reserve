from mazegenerator.mazegenerator import MazeGenerator
maze = MazeGenerator(size=(15, 15), seed=42).maze
for y in range(15):
    for x in range(14):
        right = x + 1
        has_e = (maze[y][x] & 2) != 0
        has_w = (maze[y][right] & 8) != 0
        if maze[y][x] != 15 and maze[y][right] != 15 and has_e != has_w:
            print(f"Mismatch at y={y}, x={x}: E={has_e}, W={has_w}")
