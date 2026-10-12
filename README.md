*This project has been created as part of the 42 curriculum by ohariss, oissfoul.*

# Pac-Man

## Description

This project is a recreation of the classic **Pac-Man** arcade game developed in Python using Pygame. The game features procedurally generated and braided mazes with an embedded "42" logo in the center, authentic ghost AI behaviors (Chase, Frightened, and Eaten states), collectible dots and power pellets, dynamic scoreboards, and multi-level progression across 10 distinct difficulty stages.

The goal is to navigate the maze, collect all pac-gums and super pac-gums, evade four ghosts each possessing unique targeting personalities, and achieve the highest possible score before time or lives run out.

---

## Instructions

### Prerequisites & Installation

The project requires Python 3.10+ and the dependencies listed in `requirements.txt` (such as `pygame` or `pygame-ce` and `pydantic`).

Install dependencies using `pip`:
```bash
pip install -r requirements.txt
```
Or with the provided Makefile:
```bash
make install
```

### Execution

Run the game with the default configuration (`config.json`):
```bash
python3 pac-man.py
```
Or specify a custom configuration file:
```bash
python3 pac-man.py config.json
```
Using the `Makefile`:
```bash
make run
```

### Training Interface & Configuration Export

If using an automated training or simulation environment:
- **Run the training interface:**
  ```bash
  bash run.sh
  ```
- **Exporting configurations:** The training interface or level generator can output level configuration files containing grid dimensions, seeds, obstacle placements, and timers.

### Submission Requirements
- **10 exported configuration files (one per level)** must be placed at the root of the repository (`level1.json`, `level2.json`, ..., `level10.json` or `config.json` defining all 10 stages).
- Ensure all dependencies, assets, and source directories remain organized as specified.

---

## Game Controls & Features

### Controls
- **Arrow Keys / WASD:** Move Pac-Man (Up, Down, Left, Right).
- **P / Escape:** Pause / resume the game.
- **Return / Enter:** Submit player name for high scores.

### Ghost Personalities
- 🔴 **Blinky (Red):** Direct pursuer; continuously computes the shortest BFS path directly to Pac-Man.
- 🩷 **Pinky (Pink):** Ambush predator; targets 4 tiles ahead of Pac-Man's current direction.
- 🩵 **Inky (Cyan):** Flanker; coordinates angles to approach Pac-Man from behind.
- 🟠 **Clyde (Orange):** Roamer; pursues Pac-Man when far away, but retreats to its home corner when close.

---

## Resources

### References & Documentation
- **Pygame Documentation:** https://www.pygame.org/docs/
- **Pac-Man Dossier (Jamey Pittman):** Detailed reference on original arcade logic, ghost targeting tiles, and frightened behavior mechanics.
- **Maze Generation Algorithms:** Jamis Buck's guides on recursive back-tracking, braid mazes, and loop creation to prevent dead ends.
- **Computer Networking Concepts Studied:**
  - **TCP/IP Addressing & CIDR:** Understanding IPv4/IPv6 structure, private vs. public address allocation, and subnetting.
  - **Subnet Masks:** Defining network and host portions of IP addresses, calculation of network IDs and broadcast addresses.
  - **Default Gateways:** Mechanism for routing inter-subnet and outbound internet traffic.
  - **Routers vs. Switches:** Layer 2 collision domains and MAC forwarding versus Layer 3 packet routing and IP routing tables.
  - **OSI Model & TCP/IP Stack:** The 7-layer architecture (Physical, Data Link, Network, Transport, Session, Presentation, Application) and packet encapsulation/decapsulation across communication boundaries.

### AI Usage Description
AI assistance was used throughout development as a collaborative pair-programming partner: explaining BFS algorithm and Pygame mechanics, reviewing, and debugging hand-written code. All code in this repository was written, tested, and is understood by the authors.
