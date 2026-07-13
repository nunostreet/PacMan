from contracts import Direction


class Pacman:
    """Represents the player.

    Attributes:
        x: Current column.
        y: Current row.
        lives: Remaining lives.
    """

    def __init__(self, start_x: int, start_y: int, lives: int) -> None:
        """Set starting position and lives.

        Args:
            start_x: Starting column.
            start_y: Starting row.
            lives: Number of starting lives.
        """
        self.x = start_x
        self.y = start_y
        self.lives = lives

    def move(
            self,
            direction: Direction,
            neighbors: dict[tuple[int, int], list[tuple[int, int]]]
            ) -> bool:
        """Try to move in the given direction.

        Args:
            direction: Desired direction.
            neighbors: Adjacency list of the maze.

        Returns:
            True if the move was valid, False if blocked by a wall.
        """
        if direction == Direction.UP:
            next_cell = (self.x, self.y - 1)
        elif direction == Direction.DOWN:
            next_cell = (self.x, self.y + 1)
        elif direction == Direction.LEFT:
            next_cell = (self.x - 1, self.y)
        else:
            next_cell = (self.x + 1, self.y)

        if next_cell in neighbors[(self.x, self.y)]:
            self.x, self.y = next_cell
            return True
        return False

    def respawn(self, start_x: int, start_y: int) -> None:
        """Lose a life and return to the starting position.

        Args:
            start_x: Respawn column.
            start_y: Respawn row.
        """
        self.lives -= 1
        self.x = start_x
        self.y = start_y
