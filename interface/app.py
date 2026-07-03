import pygame
from engine.game import PacmanGame
from contracts import Direction, GameStatus
from interface.game_screen import GameScreen


class APP:

    def __init__(self, game: PacmanGame):
        pygame.init()
        self.game = game
        self.WIDTH, self.HEIGHT = 900, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.run = True
        self.game_screen = GameScreen(self.WIN, self.WIDTH, self.HEIGHT)

    def run_game(self):
        while self.run:
            dt = self.timer.tick(self.fps) / 1000
            direction = None
            self.WIN.fill("black")

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

            maze = self.game.tick(direction, dt)

            if maze.status == GameStatus.PLAYING:
                self.game_screen.draw(maze)
            elif maze.status == GameStatus.PAUSED
                self.game_pause.
            elif maze.status == GameStatus.WIN
                self.game_pause.
            elif maze.status == GameStatus.LEVEL_COMPLETE:
                self.game_pause.
            elif maze.status == GameStatus.GAME_OVER:
                self.game_pause.

            pygame.display.flip()
        pygame.quit()
