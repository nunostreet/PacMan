from collections import deque
import random


class Ghost:
    """Represents a ghost in the game.

    Attributes:
        x: Current column.
        y: Current row.
        start_x: Spawn column (corner of the maze).
        start_y: Spawn row (corner of the maze).
        edible: True if the ghost can be eaten by Pacman.
        flee_timer: Seconds remaining in flee mode (0 = back to chase).
        respawn_timer: Seconds until the ghost comes back (0 = active).
    """

    def __init__(self, start_x: int, start_y: int) -> None:
        """Place the ghost at the given corner.

        Args:
            start_x: Starting column.
            start_y: Starting row.
        """
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.edible: bool = False
        self.respawn_timer: float = 0
        self.flee_timer: float = 0
        self._rng = random.Random()

    def move(
            self,
            neighbors: dict[tuple[int, int], list[tuple[int, int]]],
            pacman_pos: tuple[int, int]
            ) -> None:
        """Move the ghost one cell based on current mode.

        Args:
            neighbors: Maze adjacency list.
            pacman_pos: Current Pacman position as (x, y).
        """

        if self.respawn_timer > 0:
            return
        options = neighbors[(self.x, self.y)]
        if not options:
            return

        # find the neighbour closest and furthest from Pacman
        best_dist, worst_dist = 1000, 0
        move_away = options[0]
        for neighbor in options:
            distance = (
                abs(neighbor[0] - pacman_pos[0])
                + abs(neighbor[1] - pacman_pos[1])
            )
            if distance < best_dist:
                best_dist = distance
            if distance > worst_dist:
                worst_dist = distance
                move_away = neighbor

        if self.edible:
            # flee: 30% chance of random move to make ghosts catchable
            if self._rng.random() < 0.3:
                self.x, self.y = self._rng.choice(options)
            else:
                self.x, self.y = move_away
        elif self._rng.random() < 0.2:
            # chase: 20% random noise so ghosts are not perfect
            self.x, self.y = self._rng.choice(options)
        else:
            next_pos = self._bfs_next(neighbors, pacman_pos)
            if next_pos:
                self.x, self.y = next_pos

    def respawn(self, timer: float) -> None:
        """Mark the ghost as eaten and start the respawn timer.

        Args:
            timer: Seconds before the ghost comes back.
        """
        self.respawn_timer = timer
        self.edible = False

    def update(self, dt: float) -> None:
        """Tick the respawn and flee timers.

        Args:
            dt: Seconds since the last frame.
        """
        if self.respawn_timer > 0:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn_timer = 0.0
                self.x = self.start_x
                self.y = self.start_y
        if self.flee_timer > 0:
            self.flee_timer -= dt
            if self.flee_timer <= 0:
                self.flee_timer = 0.0
                self.edible = False

    def _bfs_next(
            self,
            neighbors: dict[tuple[int, int], list[tuple[int, int]]],
            pacman_pos: tuple[int, int]
            ) -> tuple[int, int] | None:
        """Return the first step of the shortest path to Pacman via BFS.

        Args:
            neighbors: Maze adjacency list.
            pacman_pos: Target position.

        Returns:
            First step toward Pacman, or None if unreachable.
        """
        start = (self.x, self.y)
        prev: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        queue: deque[tuple[int, int]] = deque([start])

        while queue:
            pos = queue.popleft()
            if pos == pacman_pos:
                break
            for neighbor in neighbors[pos]:
                if neighbor not in prev:
                    prev[neighbor] = pos
                    queue.append(neighbor)

        if pacman_pos not in prev:
            return None

        # reconstruct path backwards to find the first step
        step = pacman_pos
        while prev[step] != start:
            parent = prev[step]
            if parent is None:
                return None
            step = parent
        return step
