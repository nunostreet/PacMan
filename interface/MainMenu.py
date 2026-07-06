from interface.OptionMenu import OptionMenu
import pygame


class MainMenu(OptionMenu):

    def __init__(self, win: pygame.Surface, width: int, height: int):
        super().__init__(win, width, height)
        self.options = ["Start Game",
                        "View Highscores",
                        "Instructions",
                        "Exit"]
        self.selected_option = 0
