import pygame
from contracts import Direction
from engine.game import PacmanGame


class APP:

    def __init__(self, game: PacmanGame):
        pygame.init()
        self.game = game
        self.WIDTH, self.HEIGHT = 900, 500
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.fps = 60
        self.run = True

    def run_game(self):
        while self.run:
            dt = self.timer.tick(self.fps)/1000
            direction = None
            self.WIN.fill("black")

            CELL = 10
            for i in range(0, 5):
                y = i * CELL
                for j in range(0, 5):
                    x = j * CELL
                    pygame.draw.rect(self.WIN, 'white', (x, y, 5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        direction = Direction.UP
                    if event.key == pygame.K_s:
                        direction = Direction.DOWN
                    if event.key == pygame.K_a:
                        direction = Direction.LEFT
                    if event.key == pygame.K_d:
                        direction = Direction.RIGHT
            self.game.tick(direction, dt)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = APP()
    game.run_game()
