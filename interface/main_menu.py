from interface.option_menu import OptionMenu
import pygame


class MainMenu(OptionMenu):
    """Top-level menu with Start, Highscores, Instructions, Exit."""

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Initialise the main menu with its fixed option set.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.options = ["Start Game",
                        "View Highscores",
                        "Instructions",
                        "Exit"]
        self.selected_option = 0
