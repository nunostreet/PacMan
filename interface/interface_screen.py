from abc import ABC, abstractmethod
from typing import Any
import pygame


class InterfaceScreen(ABC):
    """Abstract base for menu-style screens drawn outside the game loop.

    Subclasses implement draw_screen and handle_events (e.g. main menu,
    pause menu, game over screen).
    """

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Set up shared layout constants and the HUD font.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
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
    def draw_screen(self) -> None:
        """Draw the screen content onto the window."""

    @abstractmethod
    def handle_events(self) -> Any:
        """Process pending pygame events for this screen."""
