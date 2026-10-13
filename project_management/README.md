# Project Management Overview

This directory contains the project management documentation and evidence produced during the design, development, and testing of the **Pac-Man** project for the 42 curriculum.

## Table of Contents
1. [Team Organization & Roles](#team-organization--roles)
2. [Project Timeline & Tracking](timeline.md)
3. [Architecture & Technical Choices](choices.md)
4. [Risk Analysis & Mitigation](risks.md)
5. [Acceptance Test Plan & Bug Log](test_plan.md)
6. [Blocking Points & Resolution](retrospective.md)
7. [Visual Design Architecture](../t.excalidraw)

---

## Team Organization & Roles

### Contributors
- **`ohariss`** (Developer & Architecture)
- **`oissfoul`** (Developer & Game Mechanics)

### Responsibilities Matrix (RACI)

| Milestone / Component | `ohariss` | `oissfoul` |
| :--- | :---: | :---: |
| Maze Integration & Bitmask Decoding | Responsible | Accountable |
| Player Entity Movement & Animation | Accountable | Responsible |
| Collectibles (Gums & Super Gums Generation) | Accountable | Responsible |
| Ghost AI Targeting (BFS & Personalities) | Responsible | Responsible |
| Frightened Mode & Grid Snapping Physics | Responsible | Accountable |
| Engine Decoupling & Event Loop Architecture | Responsible | Consulted |
| Config & Highscore Schema Validation (Pydantic) | Responsible | Consulted |
| Cheat System & Peer-Review Shortcuts | Responsible | Responsible |
| Acceptance Testing & QA | Accountable | Responsible |

### Decision Making & Workflow
1. **Pair Programming & Code Review:** Complex algorithmic sections (DFS maze carving, BFS ghost pathfinding, and modulo alignment) were developed collaboratively with real-time testing.
2. **Feature Branching:** Experimental features were isolated into development branches (`main`, `oussama`) before rebasing and validating clean merges.
3. **Daily Standup / Sync:** Regular alignment on blocker identification, task distribution, and timeline calibration.

