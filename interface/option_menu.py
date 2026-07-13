from abc import ABC
from interface.interface_screen import InterfaceScreen
import pygame


class OptionMenu(InterfaceScreen, ABC):
    """A scrollable list of text options.

    Subclasses fill self.options with their menu entries
    (e.g. MainMenu, PauseMenu).
    """

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Initialise the menu with an empty option list.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.options: list[str] = []
        self.selected_option = 0

    def draw_screen(self) -> None:
        """Draw all options, highlighting the currently selected one."""
        for i in range(len(self.options)):
            if i == self.selected_option:
                op = self.font.render(self.options[i], True, 'yellow')
            else:
                op = self.font.render(self.options[i], True, 'white')
            y = (i + 1) * (self.HEIGHT / (len(self.options) + 1))
            text_rect = op.get_rect()
            text_rect.center = (self.WIDTH // 2, int(y))
            self.WIN.blit(op, text_rect)

    def handle_events(self) -> int | None:
        """Process input to navigate and select options.

        W/S move the selection up/down; Enter confirms the current selection.

        Returns:
            Index of the selected option if Enter was pressed, otherwise None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if self.selected_option != 0:
                        self.selected_option -= 1
                if event.key == pygame.K_s:
                    if self.selected_option != len(self.options) - 1:
                        self.selected_option += 1
                if event.key == pygame.K_RETURN:
                    return self.selected_option
        return None
