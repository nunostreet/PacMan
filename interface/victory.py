import pygame
from interface.game_over import GameOver


class Victory(GameOver):
    """Ecrã mostrado quando o jogador ganha.

    Reutiliza a lógica de desenho e input de ``GameOver`` com um
    título diferente.
    """

    def __init__(self, win: pygame.Surface, width: int, height: int):
        """Inicializa o ecrã com o título "YOU WON".

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.title = "YOU WON"
