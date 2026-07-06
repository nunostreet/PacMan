import pygame
from interface.GameOver import GameOver


class Victory(GameOver):

    def __init__(self, win: pygame.Surface, width: int, height: int):

        super().__init__(win, width, height)
        self.title = "YOU WON"
