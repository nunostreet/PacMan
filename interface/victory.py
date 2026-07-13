import pygame
from interface.game_over import GameOver


class Victory(GameOver):
    """Screen shown when the player wins.

    Reuses the drawing and input logic from GameOver with a different title.
    """

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Initialise the victory screen with the title "YOU WON".

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.title = "YOU WON"
