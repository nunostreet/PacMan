from contracts import Direction


class Pacman:
    """Representa o jogador no jogo.

    Attributes:
        x: Posição horizontal atual.
        y: Posição vertical atual.
        lives: Número de vidas restantes.
    """

    def __init__(self, start_x: int, start_y: int, lives: int) -> None:
        """Inicializa o Pacman na posição e vidas indicadas.

        Args:
            start_x: Posição horizontal inicial.
            start_y: Posição vertical inicial.
            lives: Número de vidas iniciais.
        """
        self.x = start_x
        self.y = start_y
        self.lives = lives

    def move(
            self,
            direction: Direction,
            neighbors: dict[tuple[int, int], list[tuple[int, int]]]
            ) -> bool:

        if direction == Direction.UP:
            next_cell = (self.x, self.y - 1)
        elif direction == Direction.DOWN:
            next_cell = (self.x + 1, self.y)
        elif direction == Direction.LEFT:
            next_cell = (self.x, self.y + 1)
        elif direction == Direction.RIGHT:
            next_cell = (self.x - 1, self.y)

        if next_cell in neighbors[(self.x, self.y)]:
            self.x, self.y = next_cell
            return True
        return False
