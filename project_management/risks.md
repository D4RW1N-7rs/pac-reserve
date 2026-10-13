# Risk Analysis & Mitigation

This document identifies potential risks evaluated during the project lifecycle and the proactive strategies implemented to mitigate them.

| Risk ID | Risk Description | Severity | Probability | Impact | Mitigation Strategy | Status |
| :---: | :--- | :---: | :---: | :--- | :--- | :---: |
| **R-01** | **Python Recursion Limit on Large Mazes**<br>Level 10 uses a $47 \times 26$ grid (1,222 cells). Recursive DFS maze carving would crash with `RecursionError`. | High | High | Game crashes during level transition | Implemented an iterative DFS stack carving algorithm with explicit loop frames, removing all recursion limits. | Mitigated |
| **R-02** | **Off-Grid Modulo Clipping**<br>Entity speeds (e.g. switching between 2, 4, 5, and 8 px/frame) could skip tile boundaries (`pixel % tile_size == 0`), causing entities to phase through walls and exit the maze. | High | High | Ghost/player flies off-screen permanently | Added coordinate rounding `round(pixel / tile_size) * tile_size` whenever state transitions or speed changes occur. | Mitigated |
| **R-03** | **Main Thread Freezing During Death**<br>Initial death sequence used `time.sleep(1)` inside the event loop, causing the OS window to show "Not Responding" and dropped inputs. | Medium | High | Degraded user experience and lost keyboard events | Separated countdown and transition states using non-blocking timestamp comparisons (`time.time() - start_time`). | Mitigated |
| **R-04** | **Corrupted High Scores & Config Injection**<br>Malformed JSON or corrupted score files crashing the game upon startup. | Medium | Medium | Inability to launch or persist high scores | Wrapped loading with Pydantic validation schemas, comment-stripping, and safe fallback defaults. | Mitigated |
| **R-05** | **Ghost Stacking / Visual Merging**<br>Multiple ghosts running the same BFS path over the same cell merge into a single visual sprite. | Low | High | Poor visual feedback during gameplay | Added mutual exclusion checks during turn selection: ghosts evaluate tiles occupied by other ghosts and divert if alternative legal moves exist. | Mitigated |
| **R-06** | **Missing Dependencies on Peer Machines**<br>Host evaluation environments lacking `pydantic` or `pygame-ce`. | High | Medium | Evaluation failure (`ModuleNotFoundError`) | Documented strict versions in `requirements.txt`, automated installation via `Makefile` (`make install`), and provided clear installation guides in `README.md`. | Mitigated |

