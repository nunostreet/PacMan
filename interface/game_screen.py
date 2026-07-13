import pygame
from contracts import GhostState, GameSnapshot, GameStatus, Direction


class GameScreen:
    """Desenha uma única frame de jogo numa janela do pygame.

    Guarda os sprites carregados e as posições da frame anterior do
    Pac-Man e dos fantasmas, usadas para calcular um movimento
    suave entre células da grelha através de ``move_alpha``.
    """

    def __init__(self, win: pygame.Surface, width: int, height: int):
        """Carrega fontes e sprites e configura as constantes do HUD.

        Args:
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
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
        self.frame = 0
        self.last_direction = Direction.RIGHT
        self._load_sprites()
        self.prev_pacman_pos: tuple[int, int] = (0, 0)
        self.prev_ghost_pos: list[tuple[int, int]] = [
            (0, 0), (0, 0), (0, 0), (0, 0)
        ]
        self.pacman_grid_pos: tuple[int, int] = (0, 0)
        self.ghost_grid_pos: list[tuple[int, int]] = [
            (0, 0), (0, 0), (0, 0), (0, 0)
        ]
        self.prev_pacman_alpha: float = 0.0
        self.prev_ghost_alpha: float = 0.0

    def _load_sprites(self) -> None:
        """Carrega do disco as imagens do Pac-Man, fantasmas e HUD."""
        self.pacman_right = [
            pygame.image.load("assets/pacman-art/pacman-right/1.png"),
            pygame.image.load("assets/pacman-art/pacman-right/2.png"),
            pygame.image.load("assets/pacman-art/pacman-right/3.png"),
        ]
        self.pacman_left = [
            pygame.image.load("assets/pacman-art/pacman-left/1.png"),
            pygame.image.load("assets/pacman-art/pacman-left/2.png"),
            pygame.image.load("assets/pacman-art/pacman-left/3.png"),
        ]
        self.pacman_up = [
            pygame.image.load("assets/pacman-art/pacman-up/1.png"),
            pygame.image.load("assets/pacman-art/pacman-up/2.png"),
            pygame.image.load("assets/pacman-art/pacman-up/3.png"),
        ]
        self.pacman_down = [
            pygame.image.load("assets/pacman-art/pacman-down/1.png"),
            pygame.image.load("assets/pacman-art/pacman-down/2.png"),
            pygame.image.load("assets/pacman-art/pacman-down/3.png"),
        ]
        self.pacman_sprites = {
            Direction.RIGHT: self.pacman_right,
            Direction.LEFT: self.pacman_left,
            Direction.UP: self.pacman_up,
            Direction.DOWN: self.pacman_down,
        }
        self.ghost_sprites = {
            0: pygame.image.load("assets/pacman-art/ghosts/blinky.png"),
            1: pygame.image.load("assets/pacman-art/ghosts/pinky.png"),
            2: pygame.image.load("assets/pacman-art/ghosts/inky.png"),
            3: pygame.image.load("assets/pacman-art/ghosts/clyde.png"),
        }
        self.ghost_edible = pygame.image.load(
            "assets/pacman-art/ghosts/blue_ghost.png"
        )
        self.life_icon = pygame.image.load(
            "assets/pacman-art/other/apple.png"
        )

    def calculate_cell(self, grid: list[list[int]]):
        """Calcula o tamanho em pixels de uma única célula do labirinto.

        Args:
            grid: A grelha do labirinto, usada para obter linhas e colunas.

        Returns:
            Um tuplo ``(cell_height, cell_width)`` em pixels.
        """
        CELL_H = (
            self.HEIGHT - self.HUD_HEIGHT - self.PADDING_BOTTOM
        ) / len(grid)
        CELL_W = (self.WIDTH - self.PADDING_WIDTH) / len(grid[0])
        return CELL_H, CELL_W

    def draw_maze(self, grid: list[list[int]]):
        """Desenha o fundo das células do labirinto e as suas paredes.

        As paredes de cada célula são codificadas como uma bitmask
        (1=norte, 2=este, 4=sul, 8=oeste) e desenhadas como linhas
        brancas individuais.

        Args:
            grid: A grelha do labirinto com a bitmask de paredes de
                cada célula.
        """
        CELL_H, CELL_W = self.calculate_cell(grid)
        for i in range(len(grid)):
            y = i * CELL_H
            for j in range(len(grid[i])):
                x = j * CELL_W + self.PADDING_WIDTH/2
                pygame.draw.rect(self.WIN, 'black', (x, y, CELL_W, CELL_H))

                # parede norte
                if (grid[i][j] & 1):
                    pygame.draw.line(
                        self.WIN, 'white', (x, y), (x + CELL_W, y), 1
                    )

                # parede este
                if (grid[i][j] & 2):
                    pygame.draw.line(
                        self.WIN, 'white',
                        (x + CELL_W, y), (x + CELL_W, y + CELL_H), 1
                    )

                # parede sul
                if (grid[i][j] & 4):
                    pygame.draw.line(
                        self.WIN, 'white',
                        (x, y + CELL_H), (x + CELL_W, y + CELL_H), 1
                    )

                # parede oeste
                if (grid[i][j] & 8):
                    pygame.draw.line(
                        self.WIN, 'white', (x, y), (x, y + CELL_H), 1
                    )

    def draw_pacman(
        self,
        grid: list[list[int]],
        pacman_pos: tuple[int, int],
        direction: Direction,
        move_alpha: float
    ):
        """Desenha o Pac-Man, animado e interpolado até à sua nova célula.

        Args:
            grid: A grelha do labirinto, usada para calcular as
                dimensões das células.
            pacman_pos: A posição atual do Pac-Man na grelha,
                ``(col, row)``.
            direction: A direção atual do Pac-Man, ou ``None`` para
                manter a última direção conhecida.
            move_alpha: Fator de interpolação em ``[0, 1]`` entre a
                posição anterior e a atual na grelha, usado para
                suavizar o movimento entre frames.
        """
        if direction is not None:
            self.last_direction = direction

        self.frame = int(move_alpha * 3) % 3
        sprites = self.pacman_sprites[self.last_direction]
        sprite = sprites[self.frame]
        CELL_H, CELL_W = self.calculate_cell(grid)
        pacman = pygame.transform.scale(sprite, (CELL_W * 0.5, CELL_H * 0.5))

        if pacman_pos != self.pacman_grid_pos:
            dx = abs(pacman_pos[0] - self.pacman_grid_pos[0])
            dy = abs(pacman_pos[1] - self.pacman_grid_pos[1])
            if dx + dy <= 1:
                self.prev_pacman_pos = self.pacman_grid_pos
            else:
                self.prev_pacman_pos = pacman_pos
            self.pacman_grid_pos = pacman_pos
        elif move_alpha < self.prev_pacman_alpha:
            # O ciclo de movimento reiniciou (alpha voltou a ~0) mas a
            # célula não mudou: o movimento foi bloqueado (ex: parede).
            # Fica parado na posição atual em vez de saltar de volta à
            # célula anterior.
            self.prev_pacman_pos = pacman_pos
        self.prev_pacman_alpha = move_alpha

        prev_x = (
            self.prev_pacman_pos[0] * CELL_W
            + (self.PADDING_WIDTH / 2) + (CELL_W / 2)
        )
        prev_y = self.prev_pacman_pos[1] * CELL_H + (CELL_H/2)
        curr_x = pacman_pos[0] * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
        curr_y = pacman_pos[1] * CELL_H + (CELL_H/2)

        x = prev_x + (curr_x - prev_x) * move_alpha
        y = prev_y + (curr_y - prev_y) * move_alpha

        pac = pacman.get_rect()
        pac.center = (x, y)
        self.WIN.blit(pacman, pac)

    def draw_ghosts(
        self,
        grid: list[list[int]],
        ghosts: list[GhostState],
        move_alpha: float,
    ):
        """Desenha cada fantasma ativo, interpolado até à sua nova célula.

        Os fantasmas comestíveis são desenhados com o sprite
        "blue ghost"; os restantes fantasmas ativos usam o seu
        próprio sprite, indexado pela posição.

        Args:
            grid: A grelha do labirinto, usada para calcular as
                dimensões das células.
            ghosts: O estado atual de cada fantasma.
            move_alpha: Fator de interpolação em ``[0, 1]`` entre a
                posição anterior e a atual na grelha (calculado com o
                intervalo de movimento dos fantasmas), usado para
                suavizar o movimento entre frames.
        """
        CELL_H, CELL_W = self.calculate_cell(grid)

        for i, ghost in enumerate(ghosts):
            if ghost.active:

                if (ghost.x, ghost.y) != self.ghost_grid_pos[i]:
                    dx = abs(ghost.x - self.ghost_grid_pos[i][0])
                    dy = abs(ghost.y - self.ghost_grid_pos[i][1])
                    if dx + dy <= 1:
                        self.prev_ghost_pos[i] = self.ghost_grid_pos[i]
                    else:
                        self.prev_ghost_pos[i] = (ghost.x, ghost.y)
                    self.ghost_grid_pos[i] = (ghost.x, ghost.y)

                elif move_alpha < self.prev_ghost_alpha:
                    # Ciclo de movimento reiniciou sem a célula mudar
                    # (ex: fantasmas congelados pela cheat). Fica
                    # parado em vez de saltar para a célula anterior.
                    self.prev_ghost_pos[i] = (ghost.x, ghost.y)

                prev_x = (
                    self.prev_ghost_pos[i][0] * CELL_W
                    + (self.PADDING_WIDTH / 2) + (CELL_W / 2)
                )
                prev_y = self.prev_ghost_pos[i][1] * CELL_H + (CELL_H/2)
                curr_x = ghost.x * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
                curr_y = ghost.y * CELL_H + (CELL_H/2)

                x = prev_x + (curr_x - prev_x) * move_alpha
                y = prev_y + (curr_y - prev_y) * move_alpha
                if ghost.edible:
                    gh = pygame.transform.scale(
                        self.ghost_edible, (CELL_W * 0.5, CELL_H * 0.5)
                    )
                    gh_rect = gh.get_rect()
                    gh_rect.center = (x, y)
                    self.WIN.blit(gh, gh_rect)
                else:
                    gh = pygame.transform.scale(
                        self.ghost_sprites[i], (CELL_W * 0.5, CELL_H * 0.5)
                    )
                    gh_rect = gh.get_rect()
                    gh_rect.center = (x, y)
                    self.WIN.blit(gh, gh_rect)
            else:
                # Fantasma em respawn: mantém as posições sincronizadas
                # para não interpolar de forma estranha quando reaparecer.
                self.prev_ghost_pos[i] = (ghost.x, ghost.y)
                self.ghost_grid_pos[i] = (ghost.x, ghost.y)

        self.prev_ghost_alpha = move_alpha

    def draw_pacgums(self, grid: list[list[int]], snapshot: GameSnapshot):
        """Desenha as pac-gums (pontos e power pellets) no labirinto.

        Args:
            grid: A grelha do labirinto, usada para calcular as
                dimensões das células.
            snapshot: Snapshot atual do jogo com a disposição das
                pacgums, onde cada célula é 0 (nenhuma), 1 (ponto)
                ou 2 (pellet).
        """
        CELL_H, CELL_W = self.calculate_cell(grid)
        pacgums = snapshot.pacgums
        for i in range(len(pacgums)):
            y = i * CELL_H + (CELL_H/2)
            for j in range(len(pacgums[i])):
                x = j * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
                if pacgums[i][j] == 0:
                    continue
                if pacgums[i][j] == 1:
                    pygame.draw.circle(self.WIN, 'white', (x, y), 2)
                if pacgums[i][j] == 2:
                    pygame.draw.circle(self.WIN, 'white', (x, y), 4)

    def draw_hud(self, snapshot: GameSnapshot):
        """Desenha o HUD: pontuação, vidas, nível e cronómetro.

        Args:
            snapshot: Snapshot atual do jogo com a pontuação, vidas,
                nível, tempo restante e flag de cheat mode a apresentar.
        """
        score = self.font.render(f"Score: {snapshot.score}", True, 'white')
        self.WIN.blit(score, (0, self.HEIGHT - self.HUD_HEIGHT + 10))

        for i in range(snapshot.lives):
            icon = pygame.transform.scale(self.life_icon, (20, 20))
            self.WIN.blit(
                icon, (100 + i * 25, self.HEIGHT - self.HUD_HEIGHT + 10)
            )

        level = self.font.render(f"Level: {snapshot.level}", True, 'white')
        self.WIN.blit(level, (200, self.HEIGHT - self.HUD_HEIGHT + 10))

        time = self.font.render(
            f"Time Remaining: {snapshot.time_remaining:.2f}", True, 'white'
        )
        self.WIN.blit(time, (300, self.HEIGHT - self.HUD_HEIGHT + 10))

        if snapshot.cheat_used:
            cheat = self.font.render("CHEAT MODE", True, 'red')
            self.WIN.blit(cheat, (600, self.HEIGHT - self.HUD_HEIGHT + 10))

    def detect_status(self, status: GameStatus):
        """Desenha uma mensagem centrada de vitória/derrota.

        Args:
            status: O estado atual do jogo a que se deve reagir.
        """
        if status == GameStatus.GAME_OVER:
            lost = self.font.render("YOU LOST!", True, 'white')
            text_rect = lost.get_rect()
            text_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
            self.WIN.blit(lost, text_rect)

        if status == GameStatus.WIN:
            won = self.font.render("YOU WON!", True, 'white')
            text_rect = won.get_rect()
            text_rect.center = (self.WIDTH // 2, self.HEIGHT // 2)
            self.WIN.blit(won, text_rect)

    def draw(self, snapshot: GameSnapshot, direction: Direction):
        """Desenha uma frame completa: labirinto, pacgums, sprites e HUD.

        Args:
            snapshot: Snapshot atual do jogo a renderizar.
            direction: A direção atual do Pac-Man.
        """
        grid = snapshot.maze
        self.draw_maze(grid)
        self.draw_pacgums(grid, snapshot)
        self.draw_pacman(
            grid, snapshot.pacman_pos, direction, snapshot.move_alpha
        )
        self.draw_ghosts(grid, snapshot.ghosts, snapshot.ghost_move_alpha)
        self.draw_hud(snapshot)
