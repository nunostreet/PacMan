import pygame
from engine.game import PacmanGame
from contracts import Direction, GameStatus
from interface.game_over import GameOver
from interface.victory import Victory
from interface.game_screen import GameScreen
from interface.main_menu import MainMenu
from interface.highscores import Highscores
from interface.pause_menu import PauseMenu
from interface.instructions import Instructions
from enum import Enum
from contracts import GameConfig


class AppStatus(Enum):
    """Estado atual da app."""

    MENU = "MENU"
    GAME = "GAME"
    EXIT = "EXIT"
    HIGHSCORES = "HIGHSCORES"
    INSTRUCTIONS = "INSTRUCTIONS"
    PAUSED = "PAUSED"


class APP:
    """Controlador principal da aplicação que executa o loop do jogo Pac-Man.

    Possui a janela do pygame e gere as transições entre ecrãs
    (menu, jogo, pausa, highscores, game over e vitória) com base
    no ``AppStatus`` atual.
    """

    def __init__(self, game: PacmanGame, config: GameConfig):
        """Inicializa o pygame e cria todos os ecrãs usados pela aplicação.

        Args:
            game: A instância do motor do jogo Pac-Man que gere o jogo.
            config: Valores de configuração usados para montar o jogo e
                os seus ecrãs.
        """
        pygame.init()
        self.game = game
        self.config = config
        self.WIDTH, self.HEIGHT = 900, 800
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.run = True
        self.direction = None
        self._invincible = False
        self._frozen = False
        self.game_screen = GameScreen(self.WIN, self.WIDTH, self.HEIGHT)
        self.menu = MainMenu(self.WIN, self.WIDTH, self.HEIGHT)
        self.pause_menu = PauseMenu(self.WIN, self.WIDTH, self.HEIGHT)
        self.instructions = Instructions(self.WIN, self.WIDTH, self.HEIGHT)
        self.game_over = GameOver(self.WIN, self.WIDTH, self.HEIGHT)
        self.victory = Victory(self.WIN, self.WIDTH, self.HEIGHT)
        self.highscores = Highscores(
            config.highscore_filename, self.WIN, self.WIDTH, self.HEIGHT
        )
        self.app_status = AppStatus.MENU

    def run_game(self):
        """Executa o loop principal da aplicação até que esta seja fechada.

        Desenha repetidamente o ecrã correspondente ao ``AppStatus``
        atual, processa os eventos de input e avança o estado do jogo,
        até que ``self.run`` se torne ``False``.
        """
        self.highscores.load()
        while self.run:

            if self.app_status == AppStatus.MENU:
                self.WIN.fill("black")
                self.timer.tick(self.fps)
                self.menu.draw_screen()
                event = self.menu.handle_events()

                if event == 0:
                    self.game = PacmanGame(self.config)
                    self.app_status = AppStatus.GAME

                elif event == 1:
                    self.app_status = AppStatus.HIGHSCORES

                elif event == 2:
                    self.app_status = AppStatus.INSTRUCTIONS

                elif event == 3:
                    self.app_status = AppStatus.EXIT

            if self.app_status == AppStatus.HIGHSCORES:
                self.WIN.fill("black")
                self.timer.tick(self.fps)
                self.highscores.draw()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key in (
                            pygame.K_ESCAPE,
                            pygame.K_BACKSPACE,
                        ):
                            self.app_status = AppStatus.MENU

            if self.app_status == AppStatus.INSTRUCTIONS:
                self.WIN.fill("black")
                self.timer.tick(self.fps)
                self.instructions.draw_screen()
                self.instructions.handle_events()

            if self.app_status == AppStatus.EXIT:
                self.run = False

            if self.app_status == AppStatus.PAUSED:
                self.WIN.fill("black")
                self.timer.tick(self.fps)
                self.pause_menu.draw_screen()
                event = self.pause_menu.handle_events()
                if event == 0:
                    self.app_status = AppStatus.GAME

                elif event == 1:
                    self.app_status = AppStatus.MENU

            if self.app_status == AppStatus.GAME:
                dt = self.timer.tick(self.fps) / 1000
                self.WIN.fill("black")

                maze = self.game.tick(self.direction, dt)
                if maze.status == GameStatus.PLAYING:
                    self.game_screen.draw(maze, self.direction)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_w:
                                self.direction = Direction.UP
                            if event.key == pygame.K_s:
                                self.direction = Direction.DOWN
                            if event.key == pygame.K_a:
                                self.direction = Direction.LEFT
                            if event.key == pygame.K_d:
                                self.direction = Direction.RIGHT
                            if event.key == pygame.K_ESCAPE:
                                self.app_status = AppStatus.PAUSED
                            if event.key == pygame.K_i:
                                self._invincible = not self._invincible
                                self.game.set_invincible(self._invincible)
                            if event.key == pygame.K_f:
                                self._frozen = not self._frozen
                                self.game.set_frozen_ghosts(self._frozen)
                            if event.key == pygame.K_l:
                                self.game.skip_level()
                            if event.key == pygame.K_b:
                                self.game.go_back_level()
                            if event.key in (
                                pygame.K_PLUS,
                                pygame.K_KP_PLUS,
                            ):
                                self.game.add_lives()

                if maze.status == GameStatus.GAME_OVER:
                    self.game_over.draw_screen(maze.score)
                    player_name = self.game_over.handle_events()
                    if player_name:
                        self.app_status = AppStatus.MENU
                        self.game_over.player_name = ""
                        if not maze.cheat_used:
                            self.highscores.add(player_name, maze.score)
                            self.highscores.save()

                if maze.status == GameStatus.WIN:
                    self.victory.draw_screen(maze.score)
                    player_name = self.victory.handle_events()
                    if player_name:
                        self.app_status = AppStatus.MENU
                        self.victory.player_name = ""
                        if not maze.cheat_used:
                            self.highscores.add(player_name, maze.score)
                            self.highscores.save()

            pygame.display.flip()
        pygame.quit()
