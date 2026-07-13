import pygame
from interface.interface_screen import InterfaceScreen


class GameOver(InterfaceScreen):
    """Screen shown when the player loses.

    Also used as a base class for Victory, which just changes the title.
    """

    def __init__(self, win: pygame.Surface, width: int, height: int) -> None:
        """Set up the screen with a default score and player name.

        Args:
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        super().__init__(win, width, height)
        self.quit = False
        self.score = 0
        self.player_name = ""
        self.title = "GAME OVER"

    def draw_screen(self, score: int = 0) -> None:
        """Draw the title, final score, and current name input.

        Args:
            score: Final player score to display.
        """
        content = []
        game = self.font.render(f"{self.title}", True, 'white')
        content.append(game)
        sco = self.font.render(f"Final Score: {score}", True, 'white')
        content.append(sco)
        name = self.font.render(
            f"Player Name: {self.player_name}", True, 'white')
        content.append(name)
        for i in range(len(content)):
            y = (i + 1) * (self.HEIGHT / (len(content) + 1))
            text_rect = content[i].get_rect()
            text_rect.center = (self.WIDTH // 2, int(y))
            self.WIN.blit(content[i], text_rect)

    def handle_events(self) -> str | None:
        """Process input to edit and submit the player name.

        Handles app close, backspace, alphanumeric/space input (up to 10
        chars), and Enter to submit.

        Returns:
            The entered player name if Enter was pressed, otherwise None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        return self.player_name
                else:
                    if len(self.player_name) < 10 and (
                        event.unicode.isalnum() or event.unicode == " "
                    ):
                        self.player_name += event.unicode
        return None
