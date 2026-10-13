# Acceptance Test Plan & Bug Log

## 1. Acceptance Test Matrix

| Test ID | Feature / Component | Test Scenario | Expected Result | Result |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | **Maze Generation** | Launch Level 1 and Level 10 configurations. | Correct window dimensions generated; center "42" obstacle present; no closed off/inaccessible corridors. | **PASS** |
| **TC-02** | **Player Movement** | Press Arrow keys / WASD before an upcoming intersection. | Buffered turn executes as soon as tile boundary is reached; player stops when facing a wall. | **PASS** |
| **TC-03** | **Collectibles** | Eat regular pac-gums and super pac-gums. | +10 awarded for normal gum; +50 for super gum; eaten collectibles vanish; total gum count decreases. | **PASS** |
| **TC-04** | **Ghost AI Chase** | Observe Red, Pink, Cyan, and Orange ghosts in CHASE state. | Red chases directly; Pink aims ahead; Cyan flanks; Orange retreats to corner when within 4 tiles. | **PASS** |
| **TC-05** | **Frightened State** | Eat a super pac-gum. | All active ghosts turn blue/dead sprite; speed drops to 2 px/frame; ghosts flee away from Pac-Man for 7 seconds. | **PASS** |
| **TC-06** | **Eating Ghosts** | Collide with a ghost during Frightened state. | Ghost enters EATEN state; vanishes; floating "+200" popup renders at coordinates for 1.0 second. | **PASS** |
| **TC-07** | **Ghost Respawn** | Allow Frightened timer to expire after eating ghosts. | Eaten ghosts respawn at starting spawn corners in CHASE mode; surviving ghosts return to CHASE mode. | **PASS** |
| **TC-08** | **High Scores** | Submit nickname after game over and exit. | Score correctly appended, sorted in descending order, and rendered on High Scores screen. | **PASS** |
| **TC-09** | **Pause Menu** | Press <kbd>P</kbd> or <kbd>Esc</kbd> during active gameplay. | Game pauses; window changes to pause screen; Continue resumes at exact position; Menu returns to title. | **PASS** |
| **TC-10** | **Cheats** | Press <kbd>1</kbd>, <kbd>2</kbd>, <kbd>3</kbd>, <kbd>4</kbd>, <kbd>5</kbd> during gameplay. | 1=Invincible; 2=Level skip; 3=Ghost freeze; 4=+1 Life; 5=High speed toggle with coordinate grid snap. | **PASS** |

---

## 2. Bug Log & Fixes

| Bug ID | Description | Root Cause | Fix Implemented |
| :---: | :--- | :--- | :--- |
| **BUG-01** | Frightened timer never expired | In `game.py`, `frighten()` was called inside a per-frame coordinate check, resetting `frightened_timer` 40 times per second. | Changed `eat_collectibles()` to return a boolean `super_eaten` flag, triggering `frighten()` strictly once upon consumption. |
| **BUG-02** | Ghost speed stuck at 2 px/frame | Ghost `draw()` method had a side-effect setting `self.speed = 2` whenever state was `FRIGHTENED`, overriding speed restoration. | Removed state mutation side-effects from `draw()`. Speed is managed strictly inside `frighten()` and `update()`. |
| **BUG-03** | Ghost clipping off the maze after frightened mode | When returning from speed 2 to speed 4, the ghost was at an odd pixel coordinate and permanently skipped `% tile_size == 0` checks. | Added coordinate realignment `round(pos / tile_size) * tile_size` upon transitioning from FRIGHTENED back to CHASE. |
| **BUG-04** | Ghost stacking / visual merging | Multiple ghosts chasing Pac-Man chose the exact same tile at intersections, rendering on top of each other. | Added collision avoidance in `Ghost.update()`: ghosts detect other ghosts occupying destination tiles and choose open alternatives. |
| **BUG-05** | `font not initialized` on game launch | `menus.load_assets()` initialized fonts before `pygame.font.init()` was called by the engine. | Added explicit `pygame.font.init()` check inside `create_window()` and `load_assets()`. |
| **BUG-06** | `Ghost.update()` positional argument mismatch | `game.py` passed `self.ghosts` as a 4th argument, but `Ghost.update` had only 3 parameters. | Added `other_ghosts=None` to `Ghost.update()` parameter list. |

