from interface.interface_screen import InterfaceScreen
import pygame


class Instructions(InterfaceScreen):
    """Static screen showing game controls and rules."""

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Initialise the instructions screen.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.lines = [
            "CONTROLS",
            "W/A/S/D - Move",
            "ESC - Pause",
            "",
            "CHEATS",
            "I - Invincibility",
            "F - Freeze Ghosts",
            "L - Skip Level",
            "B - Go Back Level",
            "M - Add Life",
            "",
            "Press ESC to go back",
        ]

    def draw_screen(self) -> None:
        """Draw instructions centred on screen."""
        for i, line in enumerate(self.lines):
            text = self.font.render(line, True, 'white')
            text_rect = text.get_rect()
            text_rect.center = (self.WIDTH // 2, 80 + i * 40)
            self.WIN.blit(text, text_rect)

    def handle_events(self) -> bool | None:
        """Process events — ESC returns to the menu.

        Returns:
            True if the user pressed ESC, otherwise None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return None
