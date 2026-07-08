import pygame
from interface.interface_screen import InterfaceScreen


class GameOver(InterfaceScreen):

    def __init__(self, win: pygame.Surface, width: int, height: int):

        super().__init__(win, width, height)
        self.quit = False
        self.score = 0
        self.player_name = ""
        self.title = "GAME OVER"

    def draw_screen(self, score: int,):

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
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(content[i], text_rect)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    return self.player_name
                else:
                    if len(self.player_name) <= 10 and (
                        event.unicode.isalnum() or event.unicode == " "
                    ):
                        self.player_name += event.unicode
        return None
