from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class Direction(Enum):
    """Player movement directions."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GameStatus(Enum):
    """Current state of the game."""

    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"


@dataclass
class GhostState:
    """Snapshot of a single ghost at a given moment.

    Attributes:
        x: Column position.
        y: Row position.
        edible: True if the ghost can be eaten by Pacman.
        active: False while the ghost is respawning (UI should not draw it).
        flashing: True when flee mode is nearly over (UI should flash).
    """

    x: int
    y: int
    edible: bool = False
    active: bool = True
    flashing: bool = False


@dataclass
class GameConfig:
    """Game configuration loaded from config.json.

    Attributes:
        levels: List of maze sizes per level as (width, height) tuples.
        lives: Starting number of lives.
        pacgum: Number of pacgums to place per level.
        points_per_pacgum: Points awarded for eating a pacgum.
        points_per_super_pacgum: Points awarded for eating a super-pacgum.
        points_per_ghost: Points awarded for eating a ghost.
        ghost_respawn_time: Seconds before an eaten ghost comes back.
        level_max_time: Time limit per level in seconds.
        seed: Maze seed for level 1 (subsequent levels use seed=0).
        highscore_filename: Path to the highscores JSON file.
    """

    levels: list[tuple[int, int]] = field(default_factory=lambda: [
        (15, 11), (17, 13), (19, 15), (21, 15), (23, 17),
        (25, 17), (25, 19), (27, 19), (29, 21), (31, 21)
    ])
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    ghost_respawn_time: float = 5.0
    level_max_time: int = 90
    seed: int = 42
    highscore_filename: str = "highscores.json"


@dataclass
class GameSnapshot:
    """Full game state at a given moment, for the UI to render.

    Attributes:
        pacman_pos: Pacman position as (x, y).
        ghosts: State of each ghost.
        pacgums: Grid where 0=empty, 1=pacgum, 2=super-pacgum.
        maze: Bitmask grid (N=1, E=2, S=4, W=8) for drawing walls.
        score: Current score.
        lives: Remaining lives.
        level: Current level (starts at 1).
        time_remaining: Seconds left in the level.
        level_max_time: Total time allowed per level.
        status: Current game status.
        cheat_used: True if any cheat was activated (invalidates highscore).
        move_alpha: Pacman's progress between cells (0.0=just moved,
            ~1.0=about to move). Used by the UI to interpolate position.
        ghost_move_alpha: Same as move_alpha but for ghosts, based on
            their own movement interval.
    """

    pacman_pos: tuple[int, int]
    ghosts: list[GhostState]
    pacgums: list[list[int]]
    maze: list[list[int]]
    score: int
    lives: int
    level: int
    time_remaining: float
    level_max_time: float
    status: GameStatus
    cheat_used: bool
    move_alpha: float
    ghost_move_alpha: float


class PacmanGameProtocol(Protocol):
    """Public interface of PacmanGame, used by the UI
    to avoid circular imports.
    """

    def tick(
            self, direction: Direction | None, dt: float
    ) -> GameSnapshot: ...

    def set_frozen_ghosts(self, value: bool) -> None: ...

    def set_invincible(self, value: bool) -> None: ...

    def add_lives(self, count: int = 1) -> None: ...

    def skip_level(self) -> None: ...

    def go_back_level(self) -> None: ...
