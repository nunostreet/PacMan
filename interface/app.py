import pygame
from engine.game import PacmanGame
from contracts import Direction, GameStatus
from interface.GameOver import GameOver
from interface.Victory import Victory
from interface.GameScreen import GameScreen
from interface.MainMenu import MainMenu
from enum import Enum
from config.parser import Parser
from contracts import GameConfig


class AppStatus(Enum):
    """Estado atual da app."""

    MENU = "MENU"
    GAME = "GAME"
    EXIT = "EXIT"


class APP:

    def __init__(self, game: PacmanGame, config: GameConfig):
        pygame.init()
        self.game = game
        self.config = config
        self.WIDTH, self.HEIGHT = 900, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.run = True
        self.game_screen = GameScreen(self.WIN, self.WIDTH, self.HEIGHT)
        self.menu = MainMenu(self.WIN, self.WIDTH, self.HEIGHT)
        self.game_over = GameOver(self.WIN, self.WIDTH, self.HEIGHT)
        self.victory = Victory(self.WIN, self.WIDTH, self.HEIGHT)
        self.app_status = AppStatus.MENU

    def run_game(self):

        while self.run:
            if self.app_status == AppStatus.MENU:
                self.WIN.fill("black")
                dt = self.timer.tick(self.fps) / 1000
                self.menu.draw_screen()
                event = self.menu.handle_events()
                if event == 0:
                    self.game = PacmanGame(self.config)
                    self.app_status = AppStatus.GAME
                elif event == 3:
                    self.app_status = AppStatus.EXIT

            if self.app_status == AppStatus.EXIT:
                self.run = False

            if self.app_status == AppStatus.GAME:
                dt = self.timer.tick(self.fps) / 1000
                direction = None
                self.WIN.fill("black")
                maze = self.game.tick(direction, dt)

                if maze.status == GameStatus.PLAYING:

                    self.game_screen.draw(maze)

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

                if maze.status == GameStatus.GAME_OVER:
                    self.game_over.draw_screen(maze.score)
                    player_name = self.game_over.handle_events()
                    if player_name:
                        self.app_status = AppStatus.MENU
                        self.game_over.player_name = ""

                if maze.status == GameStatus.WIN:
                    self.victory.draw_screen(maze.score)
                    player_name = self.victory.handle_events()
                    if player_name:
                        self.app_status = AppStatus.MENU
                        self.victory.player_name = ""

            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    config = Parser()
    parse = config.run_parsing()
    pacman = PacmanGame(parse)
    game = APP(pacman, parse)
    game.run_game()
