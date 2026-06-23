from mazegenerator import MazeGenerator  # type: ignore[import-untyped]


class MazeLoader:

    def load(self, width: int, height: int, seed: int):

        try:
            mg = MazeGenerator(
                size=(width, height),
                perfect=False,
                seed=seed
            )
        except Exception as e:
            print(f"Maze generation failed: {e}")

        maze_grid = mg.maze

        return maze_grid
