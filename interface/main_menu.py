from interface.option_menu import OptionMenu
import pygame


class MainMenu(OptionMenu):
    """O menu de topo com Start, Highscores, Instructions, Exit."""

    def __init__(self, win: pygame.Surface, width: int, height: int):
        """Inicializa o menu principal com o seu conjunto fixo de opções.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.options = ["Start Game",
                        "View Highscores",
                        "Instructions",
                        "Exit"]
        self.selected_option = 0
