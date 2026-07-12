from abc import ABC, abstractmethod
import pygame


class InterfaceScreen(ABC):

    def __init__(self,
                 win: pygame.Surface,
                 width: int,
                 height: int):

        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(None, 20)
        self.HUD_HEIGHT = 40
        self.PADDING_BOTTOM = 20
        self.PADDING_WIDTH = 20
        self.quit = False

    @abstractmethod
    def draw_screen(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass
