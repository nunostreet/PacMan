from abc import ABC, abstractmethod
import pygame


class InterfaceScreen(ABC):
    """Base abstrata para ecrãs do tipo menu desenhados fora do jogo.

    As subclasses fornecem as suas próprias implementações de
    ``draw_screen`` e ``handle_events`` (por ex. menu principal,
    menu de pausa, ecrã de game over).
    """

    def __init__(self,
                 win: pygame.Surface,
                 width: int,
                 height: int):
        """Configura as constantes de layout partilhadas e a fonte do HUD.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", 12
        )
        self.HUD_HEIGHT = 40
        self.PADDING_BOTTOM = 20
        self.PADDING_WIDTH = 20
        self.quit = False

    @abstractmethod
    def draw_screen(self):
        """Desenha o conteúdo do ecrã na janela."""

    @abstractmethod
    def handle_events(self):
        """Processa os eventos pygame pendentes para este ecrã."""
