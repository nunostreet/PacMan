import contextlib
import io
import logging
import random

from mazegenerator import MazeGenerator

logger = logging.getLogger(__name__)


class MazeLoader:

    def __init__(self) -> None:
        self.neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self.pacgums: list[list[int]] = []
        self.maze_grid: list[list[int]] = []
        self.width: int = 0
        self.height: int = 0
        self._rng = random.Random()

    def load(
            self,
            width: int,
            height: int,
            seed: int,
            pacgum_count: int
            ) -> bool:

        try:
            # redirect MazeGenerator stdout to logger to keep output clean
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mg = MazeGenerator(
                    size=(width, height),
                    perfect=False,
                    seed=seed
                )
            output = buf.getvalue()
            if output:
                logger.warning("MazeGenerator output: %s", output.strip())
            maze_grid = mg.maze

            self.width = width
            self.height = height
            self.maze_grid = maze_grid
            self.neighbors = self._build_neighbors(maze_grid)
            self.pacgums = self._gen_pacgums(maze_grid, pacgum_count)

            return True

        except Exception as e:
            logger.error("Maze generation failed: %s", e)
            return False

    def _build_neighbors(
            self,
            maze_grid: list[list[int]]
            ) -> dict[tuple[int, int], list[tuple[int, int]]]:

        neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {}

        for y in range(self.height):
            for x in range(self.width):
                cell = maze_grid[y][x]
                valid = []
                # bit=0 means the wall is open (passage exists)
                if not (cell & 1):
                    valid.append((x, y - 1))
                if not (cell & 2):
                    valid.append((x + 1, y))
                if not (cell & 4):
                    valid.append((x, y + 1))
                if not (cell & 8):
                    valid.append((x - 1, y))
                neighbors[(x, y)] = valid

        return neighbors

    def _gen_pacgums(
            self,
            maze_grid: list[list[int]],
            pacgum_count: int
            ) -> list[list[int]]:

        # super-pacgums go in the four corners
        corners = {
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1)
        }

        grid = [[0] * self.width for _ in range(self.height)]
        for (x, y) in corners:
            grid[y][x] = 2

        valid_cells = []
        for y in range(self.height):
            for x in range(self.width):
                cell = maze_grid[y][x]
                if cell != 15 and (x, y) not in corners:
                    valid_cells.append((x, y))

        self._rng.shuffle(valid_cells)
        chosen = valid_cells[:pacgum_count]

        for (x, y) in chosen:
            grid[y][x] = 1

        return grid
