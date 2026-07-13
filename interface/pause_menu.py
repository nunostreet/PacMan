import pygame
from interface.option_menu import OptionMenu


class PauseMenu(OptionMenu):
    """In-game pause menu with Continue Game and Main Menu options."""

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Initialise the pause menu with its fixed option set.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.options = ["Continue Game",
                        "Main Menu"]
        self.selected_option = 0
