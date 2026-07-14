from contracts import (
    GameConfig, GameStatus, GameSnapshot,
    Direction, GhostState
)
from .maze import MazeLoader
from .player import Pacman
from .ghost import Ghost


class PacmanGame:
    """Main game logic for Pac-Man.

    Advances the game state each frame and exposes it via GameSnapshot.
    No pygame dependency — the UI consumes this class through tick().

    Attributes:
        _config: Game configuration.
        _maze: Current maze with adjacency list and pacgum grid.
        _pacman: Player state.
        _ghosts: List of the 4 ghosts.
        _score: Accumulated score.
        _level: Current level (starts at 1).
        _time_remaining: Seconds left in the level.
        _status: Current game status.
        _pacman_timer: Time accumulator for Pacman movement speed.
        _ghost_timer: Time accumulator for ghost movement speed.
        _pacman_interval: Seconds between each Pacman move.
        _ghost_interval: Seconds between each ghost move in chase mode.
        _ghost_flee_interval: Seconds between each ghost move in flee mode
            (slower than chase).
        _active_ghost_interval: The interval currently in use — equals
            _ghost_interval in chase and _ghost_flee_interval in flee.
            Used to compute ghost_move_alpha in the snapshot.
    """

    def __init__(self, config: GameConfig) -> None:
        """Set up the game with the given configuration.

        Args:
            config: Configuration loaded from config.json.
        """
        self._config = config
        width, height = self._config.levels[0]
        self._width = width
        self._height = height
        self._maze = MazeLoader()
        self._maze.load(width, height, config.seed, config.pacgum)
        self._pacman = Pacman(width // 2, height // 2, config.lives)
        self._ghosts = [
            Ghost(0, 0),
            Ghost(width - 1, 0),
            Ghost(0, height - 1),
            Ghost(width - 1, height - 1),
        ]
        self._score = 0
        self._level = 1
        self._update_speed()
        self._time_remaining = float(config.level_max_time)
        self._status = GameStatus.PLAYING
        self._frozen_ghosts = False
        self._invincible = False
        self._cheat_used = False
        self._pacman_timer: float = 0.0
        self._pacman_penalty: float = 0.0
        self._respawn_timer: float = 0.0
        self._ghost_timer: float = 0.0
        self._pacman_interval: float = 0.25
        self._ghost_interval: float = 0.30
        self._ghost_flee_interval: float = 0.45
        self._active_ghost_interval: float = self._ghost_interval
        self._scatter_mode: bool = True
        self._scatter_timer: float = 7.0
        self._scatter_phase: int = 0
        # durations alternating scatter / chase
        # https://pacman.holenet.info/#Chapter_4
        self._scatter_durations: list[float] = [
            7.0, 20.0, 7.0, 20.0, 5.0, 20.0, 5.0
        ]
        self._update_speed()

    def tick(self, direction: Direction | None, dt: float) -> GameSnapshot:
        """Advance the game state by one frame.

        Args:
            direction: Player input direction, or None if no input.
            dt: Seconds since the last frame.

        Returns:
            Current game state for the UI to render.
        """

        # freeze the game once it ends
        if self._status != GameStatus.PLAYING:
            return self._build_snapshot()

        self._time_remaining -= dt
        self._ghost_timer += dt
        if self._pacman_penalty > 0:
            self._pacman_penalty = max(0.0, self._pacman_penalty - dt)
        else:
            self._pacman_timer += dt

        # check if pacman is dead
        if self._respawn_timer > 0:
            self._respawn_timer = max(0.0, self._respawn_timer - dt)

        # only move when the accumulator hits the interval
        pacman_can_move = self._pacman_timer >= self._pacman_interval
        if pacman_can_move:
            self._pacman_timer = 0.0

        # ghosts move slower while in flee mode
        ghosts_flee = any(g.edible for g in self._ghosts)
        ghost_interval = (
            self._ghost_flee_interval if ghosts_flee else self._ghost_interval
        )
        self._active_ghost_interval = ghost_interval
        ghosts_can_move = self._ghost_timer >= ghost_interval
        if ghosts_can_move:
            self._ghost_timer = 0.0

        if pacman_can_move and direction is not None:
            self._pacman.move(direction, self._maze.neighbors)

        px, py = self._pacman.x, self._pacman.y
        # only interact once Pacman is visually halfway into the cell
        mid_cell = self._pacman_timer / self._pacman_interval >= 0.5

        if mid_cell:
            cell = self._maze.pacgums[py][px]
            if cell == 1:
                self._score += self._config.points_per_pacgum
                self._maze.pacgums[py][px] = 0
                self._pacman_penalty += 0.017
            if cell == 2:
                self._score += self._config.points_per_super_pacgum
                self._maze.pacgums[py][px] = 0
                # super-pacgum: all ghosts enter flee mode
                for ghost in self._ghosts:
                    ghost.edible = True
                    ghost.flee_timer = self._config.ghost_flee_time

        if not any(g.edible for g in self._ghosts):
            self._scatter_timer -= dt
            if self._scatter_timer <= 0:
                self._scatter_phase += 1
                if self._scatter_phase < len(self._scatter_durations):
                    self._scatter_timer = (
                        self._scatter_durations[self._scatter_phase]
                    )
                    self._scatter_mode = self._scatter_phase % 2 == 0
                else:
                    self._scatter_mode = False
                    self._scatter_timer = float('inf')

        for ghost in self._ghosts:
            if self._frozen_ghosts:
                continue
            if ghosts_can_move:
                ghost.move(self._maze.neighbors, (px, py), self._scatter_mode)
            ghost.update(dt)

        # collision: ghost active in the same cell as Pacman
        for ghost in self._ghosts:
            if (
                mid_cell
                and ghost.respawn_timer <= 0
                and self._respawn_timer <= 0
                and (px, py) == (ghost.x, ghost.y)
            ):
                if ghost.edible:
                    self._score += self._config.points_per_ghost
                    ghost.respawn(self._config.ghost_respawn_time)
                elif self._invincible:
                    continue
                else:
                    if self._pacman.lives <= 1:
                        self._status = GameStatus.GAME_OVER
                    else:
                        self._pacman.respawn(
                            self._width // 2, self._height // 2
                        )
                        self._respawn_timer = 2.0
                        # update px, py to avoid double collision in same frame
                        px, py = self._pacman.x, self._pacman.y

        if all(cell == 0 for row in self._maze.pacgums for cell in row):
            if self._level >= len(self._config.levels):
                self._status = GameStatus.WIN
            else:
                self._level += 1
                self._load_level()

        if self._time_remaining <= 0:
            self._status = GameStatus.GAME_OVER

        return self._build_snapshot()

    def _build_snapshot(self) -> GameSnapshot:
        """Build and return a GameSnapshot with the current game state.

        Returns:
            GameSnapshot with positions, ghost states, pacgums,
            score, and interpolation factors for the UI.
        """
        return GameSnapshot(
            pacman_pos=(self._pacman.x, self._pacman.y),
            ghosts=[
                GhostState(
                    g.x, g.y, g.edible,
                    active=g.respawn_timer <= 0,
                    flashing=g.edible and g.flee_timer < 2.0,
                )
                for g in self._ghosts
            ],
            pacgums=self._maze.pacgums,
            maze=self._maze.maze_grid,
            score=self._score,
            lives=self._pacman.lives,
            level=self._level,
            time_remaining=self._time_remaining,
            level_max_time=self._config.level_max_time,
            status=self._status,
            cheat_used=self._cheat_used,
            move_alpha=self._pacman_timer / self._pacman_interval,
            ghost_move_alpha=self._ghost_timer / self._active_ghost_interval,
        )

    def _load_level(self) -> None:
        """Load the maze and reset entities for the current level."""
        width, height = self._config.levels[self._level - 1]
        self._width = width
        self._height = height
        seed = self._config.seed if self._level == 1 else 0
        self._maze.load(width, height, seed, self._config.pacgum)
        self._pacman.x = width // 2
        self._pacman.y = height // 2
        self._ghosts = [
            Ghost(0, 0),
            Ghost(width - 1, 0),
            Ghost(0, height - 1),
            Ghost(width - 1, height - 1),
        ]
        self._time_remaining = float(self._config.level_max_time)
        self._status = GameStatus.PLAYING
        self._update_speed()

    def _update_speed(self) -> None:
        base_pacman = 0.25
        base_ghosts = 0.30
        if self._level >= 5:
            self._pacman_interval = base_pacman
            self._ghost_interval = base_ghosts
        elif 1 < self._level < 5:
            self._pacman_interval = base_pacman / 0.9
            self._ghost_interval = base_ghosts / 0.85
        else:
            self._pacman_interval = base_pacman / 0.8
            self._ghost_interval = base_ghosts / 0.75

    # ----- CHEAT MODE ------

    def set_frozen_ghosts(self, value: bool) -> None:
        """Freeze or unfreeze all ghosts.

        Args:
            value: True to freeze, False to resume movement.
        """
        self._frozen_ghosts = value
        self._cheat_used = True

    def set_invincible(self, value: bool) -> None:
        """Toggle Pacman invincibility.

        Args:
            value: True to enable, False to disable.
        """
        self._invincible = value
        self._cheat_used = True

    def add_lives(self, count: int = 1) -> None:
        """Add lives to the player."""
        self._pacman.lives = min(self._pacman.lives + count, 7)
        self._cheat_used = True

    def skip_level(self) -> None:
        """Skip to the next level, or trigger WIN if on the last one."""
        self._cheat_used = True
        if self._level >= len(self._config.levels):
            self._status = GameStatus.WIN
        else:
            self._level += 1
            self._load_level()

    def go_back_level(self) -> None:
        """Go back one level if possible."""
        if self._level > 1:
            self._level -= 1
            self._load_level()
            self._cheat_used = True

        # highscore should be invalidated when any cheat is used
