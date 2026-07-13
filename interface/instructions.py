from interface.interface_screen import InterfaceScreen
import pygame


class Instructions(InterfaceScreen):
    """Ecrã estático que mostra os controlos e regras do jogo."""

    def __init__(self, win, width, height):
        """Inicializa o ecrã de instruções.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        super().__init__(win, width, height)
        self.lines = [
            "CONTROLS",
            "W/A/S/D or Arrows - Move",
            "ESC - Pause",
            "",
            "CHEATS",
            "I - Invincibility",
            "F - Freeze Ghosts",
            "L - Skip Level",
            "B - Go Back Level",
            "+ - Add Life",
            "",
            "Press ESC to go back",
        ]

    def draw_screen(self):
        """Desenha as instruções centradas no ecrã."""

        for i, line in enumerate(self.lines):
            text = self.font.render(line, True, 'white')
            text_rect = text.get_rect()
            text_rect.center = (self.WIDTH // 2, 80 + i * 40)
            self.WIN.blit(text, text_rect)

    def handle_events(self):
        """Processa eventos — ESC volta ao menu."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return None
