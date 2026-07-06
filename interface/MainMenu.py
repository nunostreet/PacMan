import pygame
from interface.InterfaceScreen import InterfaceScreen


class MainMenu(InterfaceScreen):

    def __init__(self, win: pygame.Surface, width: int, height: int):
        super().__init__(win, width, height)
        self.options = ["Start Game",
                        "View Highscores",
                        "Instructions",
                        "Exit"]
        self.selected_option = 0

    def draw_screen(self):
        for i in range(len(self.options)):
            if i == self.selected_option:
                op = self.font.render(self.options[i], True, 'blue')
            else:
                op = self.font.render(self.options[i], True, 'white')
            y = (i + 1) * (self.HEIGHT / (len(self.options) + 1))
            text_rect = op.get_rect()
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(op, text_rect)

    def handle_events(self):

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
