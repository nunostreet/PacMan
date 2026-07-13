from interface.option_menu import OptionMenu


class PauseMenu(OptionMenu):
    """O menu de pausa do jogo com as opções Continue e Exit."""

    def __init__(self, win, width, height):
        """Inicializa o menu de pausa com o seu conjunto fixo de opções.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.options = ["Continue Game",
                        "Exit"]
        self.selected_option = 0
