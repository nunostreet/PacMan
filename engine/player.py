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
        """Tenta mover o Pacman na direção indicada.

        Args:
            direction: Direção do movimento.
            neighbors: Lista de adjacência do labirinto.

        Returns:
            True se o movimento foi válido, False se havia parede.
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
        """Retira uma vida ao Pacman e coloca-o no centro do mapa.

        Args:
            start_x: Posição horizontal inicial.
            start_y: Posição vertical inicial.
        """
        self.lives -= 1
        self.x = start_x
        self.y = start_y
