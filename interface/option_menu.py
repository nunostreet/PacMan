from abc import ABC
from interface.interface_screen import InterfaceScreen
import pygame


class OptionMenu(InterfaceScreen, ABC):
    """Uma lista de opções de texto selecionável e percorrível.

    As subclasses preenchem ``self.options`` com as suas entradas de
    menu (por ex. ``MainMenu``, ``PauseMenu``).
    """

    def __init__(self, win: pygame.Surface, width: int, height: int):
        """Inicializa o menu com uma lista de opções vazia.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.options = []
        self.selected_option = 0

    def draw_screen(self):
        """Desenha todas as opções, destacando a atualmente selecionada."""
        for i in range(len(self.options)):
            if i == self.selected_option:
                op = self.font.render(self.options[i], True, 'yellow')
            else:
                op = self.font.render(self.options[i], True, 'white')
            y = (i + 1) * (self.HEIGHT / (len(self.options) + 1))
            text_rect = op.get_rect()
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(op, text_rect)

    def handle_events(self):
        """Processa eventos de input para navegar e selecionar opções.

        W/S movem a seleção para cima/baixo (limitada aos limites da
        lista) e o Enter confirma a seleção atual.

        Returns:
            O índice da opção selecionada se o Enter foi premido,
            caso contrário ``None``.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.selected_option != 0:
                        self.selected_option -= 1
                if event.key == pygame.K_s:
                    if self.selected_option != len(self.options) - 1:
                        self.selected_option += 1
                if event.key == pygame.K_RETURN:
                    return self.selected_option
        return None
