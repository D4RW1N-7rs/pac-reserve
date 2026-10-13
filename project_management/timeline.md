# Project Timeline & Progress Tracking

## Development Phases & Milestones

```
Phase 1: Setup & Maze (Days 1-5)
[██████████████████████████████] 100% Completed

Phase 2: Entities & Movement (Days 6-10)
[██████████████████████████████] 100% Completed

Phase 3: Ghost AI & Frightened States (Days 11-17)
[██████████████████████████████] 100% Completed

Phase 4: Persistence, Engine Refactor & UI (Days 17-22)
[██████████████████████████████] 100% Completed

Phase 5: Cheats, Acceptance Testing & Delivery (Days 22-25)
[██████████████████████████████] 100% Completed
```

---

## Planned vs. Actual Timeline

| Phase / Milestone | Planned Duration | Actual Duration | Variance | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Milestone 1:** Architecture setup, `mazegenerator` integration, 42 logo embedding, bitmask renderer | 3 days | 3 days | On schedule | Completed |
| **Milestone 2:** Player movement, tile collision, turning queues, sprite animation | 2 days | 2.5 days | +0.5 day | Completed |
| **Milestone 3:** Collectibles spawning, dot eating, score calculation | 1.5 days | 1 day | -0.5 day | Completed |
| **Milestone 4:** Ghost BFS pathfinding & 4 distinct AI personalities (Blinky, Pinky, Inky, Clyde) | 2.5 days | 3 days | +0.5 day | Completed |
| **Milestone 5:** Frightened mode, ghost eating popup, speed change grid snapping | 1.5 days | 2 days | +0.5 day | Completed |
| **Milestone 6:** Architecture refactoring (`pac-man.py`, `src/engine.py`, `src/game.py`) | 1 day | 1 day | On schedule | Completed |
| **Milestone 7:** Config & highscore persistence validation (Pydantic, JSON) | 1 day | 1 day | On schedule | Completed |
| **Milestone 8:** Peer-review cheat mode (<kbd>1</kbd>-<kbd>5</kbd>), Acceptance testing & documentation | 1.5 days | 1 day | -0.5 day | Completed |

---

## Kanban Board Snapshot

### Done (Completed)
- [x] Integrate `mazegenerator` with braided loops and solid center "42" logo
- [x] Tile-based collision detection using bitwise operators (`cell & wall`)
- [x] Smooth player movement with direction buffering (`next_direction`)
- [x] Four-frame mouth opening/closing animation in all 4 cardinal directions
- [x] Dynamic generation of pac-gums and super pac-gums
- [x] Blinky (Red): Direct BFS chase
- [x] Pinky (Pink): 4-tile forward ambush
- [x] Inky (Cyan): Flanking from rear
- [x] Clyde (Orange): Scatter-to-corner vs. proximity chase
- [x] Frightened state (7-second timer, reverse flee AI, dead ghost sprite, flash warning)
- [x] Float `+200` score popup on ghost consumption
- [x] Dynamic window resizing per level based on maze width/height
- [x] High-scores table with sorting, unique names, and Pydantic validation
- [x] Refactor monolith `run()` into `engine.py` and modular `PacmanGame`
- [x] Implement CLI with `argparse` supporting positional config arguments
- [x] Cheat codes (<kbd>1</kbd>=invincible, <kbd>2</kbd>=skip, <kbd>3</kbd>=freeze, <kbd>4</kbd>=lives, <kbd>5</kbd>=fast)
- [x] Snap player and ghost coordinates on speed changes via `round()`

