# Project Management — Pac-Man

## Overview

This document covers the full project management approach for the Pac-Man project: team organisation, task division, timeline, key technical decisions, risk analysis, acceptance tests, and blocking points encountered during development.

The project was completed by a 2-person team working in parallel on clearly separated responsibilities: engine and UI & infrastructure.

---

## Team

| Member | Role |
|---|---|
| nstreet- | Game Engine — maze, player, ghosts, game logic, config, tests |
| pedde-al | UI & Infrastructure — renderer, HUD, game loop, input, menus, parser |

---

## How We Worked

Before writing any code, we defined who owned which files, what each class was responsible for, and the exact interface contract between the engine and the UI layer via `contracts.py`. This allowed both of us to work in parallel from the start without conflicts.

The key architectural decision was a strict **Model-View separation**: the engine files contain zero pygame and are fully testable without a window. The UI files read model state via `GameSnapshot` and render it — no game logic lives in the UI layer. This boundary made parallel development natural.

**Day-to-day workflow:**
- We used GitHub with separate branches — each person worked on their own branch and merged to main when stable.
- Technical decisions (AI approach, ghost speed, OOP structure) were discussed together before implementation.
- The shared contract (`contracts.py`) was the single source of truth between the two layers.

---

## Task Division

### nstreet- — Game Engine
- `contracts.py` — shared data types and interface protocol between engine and UI
- `engine/maze.py` — maze loading, adjacency list (neighbor graph), pacgum placement
- `engine/player.py` — player movement and wall validation
- `engine/ghost.py` — ghost AI (greedy Manhattan chase, flee, scatter/chase cycle, no-reverse rule, flee timer, respawn)
- `engine/game.py` — game loop logic, collision detection, level management, cheat mode, speed control
- `tests/` — unit tests for engine logic (not submitted)
- `pac-man.py` — entry point

### pedde-al — UI & Infrastructure
- `config/parser.py` — argument validation and JSON config loading
- `interface/app.py` — pygame initialisation and game loop
- `interface/game_screen.py` — maze and entity renderer
- `interface/` — all game screens (menu, pause, game over, victory, highscores)
- Input event handling and cheat mode keys
- Makefile

---

## Timeline

| Date | Who | Milestone |
|---|---|---|
| 2026-06-22 | nstreet- | First commit; config + contracts draft; gitignore |
| 2026-06-23 | nstreet- | Engine structure, contracts, maze loader, Makefile; player class; respawn logic; GameSnapshot with maze field |
| 2026-06-24 | nstreet- | Ghost class; ghost logic; GameConfig with levels and ghost_respawn_time |
| 2026-06-24 | pedde-al | Initial parsing; parse keys and default values |
| 2026-06-26 | nstreet- | PacmanGame with tick, level progression and ghost AI; PacmanGameProtocol; circular import fix |
| 2026-06-30 | pedde-al | First draft of UI interface; fix parsing |
| 2026-07-01 | pedde-al | Draw maze and start of setting positions |
| 2026-07-03 | pedde-al | Start of menu |
| 2026-07-06 | nstreet- | Cheat mode first draft; fix PacMan lives bug; README structure; flake8 adjustments; BFS refactor |
| 2026-07-06 | pedde-al | Menu, victory and game over screen; highscores and pacman sprite; finish UI of ghosts and pacman; pause menu |
| 2026-07-07 | nstreet- | Bug fix after game end |
| 2026-07-08 | nstreet- | Fix game speed bug; preparing main |
| 2026-07-12 | pedde-al | Fix game speed and smooth animations; HUD repositioning and cheat mode groundwork |
| 2026-07-13 | nstreet- | Ghost movement alpha; adding randomness to ghosts; cell collision fix; docstrings PT→EN |
| 2026-07-13 | pedde-al | Instructions menu; docstrings and flake8; syntax fixes; smooth animation |
| 2026-07-13 | Both | Merge feature/visualizer into main; final polish |

---

## Key Decisions

| Decision | Reason |
|---|---|
| `contracts.py` as shared interface | Strict separation between engine and UI — neither layer imports from the other directly. `PacmanGameProtocol` avoids circular imports. |
| Adjacency list (neighbor graph) for wall validation | Precomputed once at maze load for O(1) movement checks per tick — no repeated bitmask reads during gameplay. |
| Greedy Manhattan for ghost chase | Ghosts pick the open neighbour with the smallest Manhattan distance to Pacman. Simpler than BFS and sufficient given mazes are small; the no-reverse rule prevents oscillation. |
| Greedy Manhattan (inverted) for ghost flee | Ghosts pick the open neighbour with the largest Manhattan distance from Pacman. 30% random noise is added to make them catchable rather than perfectly evasive. |
| No-reverse rule on ghosts | Ghosts cannot move back to the cell they just came from. Without this, ghosts oscillate between two adjacent cells when both options have equal distance to the target. |
| Scatter/chase cycle | Ghosts alternate between chasing Pacman and retreating to their spawn corner. Replicates the original Pac-Man feel and gives the player breathing room during scatter phases. |
| Speed accumulator (`_pacman_timer`, `_ghost_timer`) | Decouples entity speed from frame rate. Pacman and ghosts each have independent intervals (0.25s and 0.30s), so they move at different speeds regardless of FPS. |
| `move_alpha` in GameSnapshot | Exposes the sub-cell progress to the UI for smooth interpolation between cells. The UI uses it to lerp sprite positions rather than snapping cell-to-cell. |
| `flee_timer` on Ghost | Without it, ghosts stay edible indefinitely after a super-pacgum — making them harmless forever. The timer resets `edible` to False after a fixed duration. |
| `_status` guard at top of `tick()` | Without it, the engine keeps processing collisions and movement after GAME_OVER, allowing multiple ghosts to drain all lives in a single frame. |
| `px, py` local copy in tick() | Prevents mid-loop position changes from affecting subsequent checks in the same frame. Updated explicitly after respawn to avoid double-collision. |
| `random.Random()` instance | Project rules prohibit using the global `random` module directly. Each entity that needs randomness holds its own `Random()` instance. |
| `contextlib.redirect_stdout` for MazeGenerator | The third-party package prints to stdout. Capturing and logging it as a warning keeps the output clean without modifying the package. |

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| mazegenerator not installed on evaluator machine | High | High | Package bundled as `.whl` in repo; `make install` handles it locally |
| Game run without config argument | High | Medium | Parser validates argument count and extension before loading; prints usage message |
| Collisions bug | Medium | Medium | The original pacman checks for pixel collisions. We've adopted a different approach where we move pacman once he has travelled more than 60% to the next cell. This can sometimes cause a bug where pacman and a ghost collide but nothing happens. We've refined the move_alpha threshold to minimize this. |
| Multiple ghost collisions draining lives instantly | Medium | High | Pacman becomes "untargetable" for 2 seconds after respawn. |

---

## Acceptance Test Plan

| Feature | How to test | Expected result |
|---|---|---|
| Argument validation | Run `python3 pac-man.py` with no args | Error message printed, exit 1 |
| Argument validation | Run with `.cub` extension | "must be a .json file" printed, exit 1 |
| Maze generation | Launch any level | Maze appears, player starts in centre |
| Player movement | WASD keys | Player moves through corridors, cannot cross walls |
| Pacgum collection | Walk over dots | Score +10 per pacgum, dots disappear |
| Super-pacgum | Walk over corner dot | Score +50, all ghosts enter flee mode |
| Ghost flee duration | Eat super-pacgum | Ghosts return to chase after ~5 seconds |
| Eat ghost | Touch edible ghost | Score +200, ghost respawns at corner after delay |
| Lose life | Touch non-edible ghost | Life counter decreases, player respawns in centre |
| Game over | Lose all lives | Game over screen with final score |
| Level complete | Eat all pacgums | Next level loads automatically |
| Win game | Complete all 10 levels | Victory screen shown |
| Pause | ESC during gameplay | Game pauses, pause menu shown |
| Highscore | Complete a game | Score saved and shown in highscores screen |
| Cheat — invincible | Activate invincible | Ghosts cannot kill player; highscore invalidated |
| Cheat — freeze ghosts | Activate freeze | Ghosts stop moving; highscore invalidated |
| Cheat — level skip | Activate skip | Advances to next level; highscore invalidated |
| Cheat — extra life | Activate add life | Life counter increases; highscore invalidated |
| Lint | `make lint` | No flake8 or mypy errors |
| Tests | `make test` | All tests pass |

---

## Blocking Points

| Issue | When | Resolution |
|---|---|---|
| `MazeGenerator` printing to stdout | Engine development | Captured with `contextlib.redirect_stdout` and logged as warning |
| Circular import between `contracts.py` and `engine/game.py` | Defining shared interface | Replaced direct import with `PacmanGameProtocol` (typing.Protocol) |
| mypy "source file found twice" | Lint setup | Removed root `__init__.py`; added `__init__.py` to package directories |
| pytest `ModuleNotFoundError` for engine | Test setup | Added `pytest.ini` with `pythonpath = .` and empty `conftest.py` at root |
| Ghost bitmask direction — `if not (cell & 1)` vs `if (cell & 1)` | Code review | Verified empirically: bit=0 means open passage. `not (cell & 1)` is correct. |
| Game ending in under 2 seconds | Integration | Two causes: (1) `dt` passed in ms not seconds — fixed on UI side with `/ 1000`; (2) missing `_status` guard in `tick()` allowing multi-ghost collision in single frame |
| Ghost too fast at all frame rates | Integration | Added speed accumulator (`_pacman_timer`, `_ghost_timer`) — movement rate now independent of FPS |
| Ghosts stay edible forever after super-pacgum | Ghost AI | Added `flee_timer` — decremented in `update()`, resets `edible` when it reaches 0 |
| Ghosts impossible to catch in flee mode | Ghost AI | Flee used perfect Manhattan — always picked furthest neighbor. Fixed by adding 30% random noise. |
