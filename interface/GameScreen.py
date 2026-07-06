import pygame
from contracts import GhostState, GameSnapshot, GameStatus, Direction


class GameScreen:

    def __init__(self, win: pygame.Surface, width: int, height: int):
        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(None, 20)
        self.HUD_HEIGHT = 40
        self.PADDING_BOTTOM = 20
        self.PADDING_WIDTH = 20
        self.frame = 0
        self.last_direction = Direction.RIGHT
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
        self.pacman_down = [
            pygame.image.load("assets/pacman-art/pacman-down/1.png"),
            pygame.image.load("assets/pacman-art/pacman-down/2.png"),
            pygame.image.load("assets/pacman-art/pacman-down/3.png"),
        ]
        self.pacman_up = [
            pygame.image.load("assets/pacman-art/pacman-up/1.png"),
            pygame.image.load("assets/pacman-art/pacman-up/2.png"),
            pygame.image.load("assets/pacman-art/pacman-up/3.png"),
        ]
        self.pacman_sprites = {
            Direction.RIGHT: self.pacman_right,
            Direction.LEFT: self.pacman_left,
            Direction.UP: self.pacman_up,
            Direction.DOWN: self.pacman_down,
        }

    def calculate_cell(self, grid: list[list[int]]):
        CELL_H = (
            self.HEIGHT - self.HUD_HEIGHT - self.PADDING_BOTTOM
        ) / len(grid)
        CELL_W = (self.WIDTH - self.PADDING_WIDTH) / len(grid[0])
        return CELL_H, CELL_W

    def draw_maze(self, grid: list[list[int]]):
        CELL_H, CELL_W = self.calculate_cell(grid)
        for i in range(len(grid)):
            y = i * CELL_H + self.HUD_HEIGHT
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
    ):
        if direction is not None:
            self.last_direction = direction

        sprites = self.pacman_sprites[self.last_direction]
        sprite = sprites[self.frame]
        CELL_H, CELL_W = self.calculate_cell(grid)
        pacman = pygame.transform.scale(sprite, (CELL_W, CELL_H))

        x = pacman_pos[0] * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
        y = pacman_pos[1] * CELL_H + self.HUD_HEIGHT + (CELL_H/2)

        pac = pacman.get_rect()
        pac.center = (x, y)
        self.WIN.blit(pacman, pac)

        if self.frame < 2:
            self.frame += 1
        elif self.frame == 2:
            self.frame = 0

    def draw_ghosts(self, grid: list[list[int]], ghosts: list[GhostState]):

        CELL_H, CELL_W = self.calculate_cell(grid)
        for ghost in ghosts:
            if ghost.active:
                x = ghost.x * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
                y = ghost.y * CELL_H + self.HUD_HEIGHT + (CELL_H/2)
                if ghost.edible:
                    pygame.draw.circle(self.WIN, 'yellow', (x, y), 5)
                else:
                    pygame.draw.circle(self.WIN, 'red', (x, y), 5)

    def draw_pacgums(self, grid: list[list[int]], snapshot: GameSnapshot):

        CELL_H, CELL_W = self.calculate_cell(grid)
        pacgums = snapshot.pacgums
        for i in range(len(pacgums)):
            y = i * CELL_H + + self.HUD_HEIGHT + (CELL_H/2)
            for j in range(len(pacgums[i])):
                x = j * CELL_W + (self.PADDING_WIDTH/2) + (CELL_W/2)
                if pacgums[i][j] == 0:
                    continue
                if pacgums[i][j] == 1:
                    pygame.draw.circle(self.WIN, 'white', (x, y), 2)
                if pacgums[i][j] == 2:
                    pygame.draw.circle(self.WIN, 'white', (x, y), 4)

    def draw_hud(self, snapshot: GameSnapshot):

        score = self.font.render(f"Score: {snapshot.score}", True, 'white')
        self.WIN.blit(score, (0, 0))
        lives = self.font.render(f"Lives: {snapshot.lives}", True, 'white')
        self.WIN.blit(lives, (100, 0))
        level = self.font.render(f"Level: {snapshot.level}", True, 'white')
        self.WIN.blit(level, (200, 0))
        time = self.font.render(
            f"Time Remaining: {snapshot.time_remaining:.2f}", True, 'white'
        )
        self.WIN.blit(time, (300, 0))

    def detect_status(self, status: GameStatus):

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
        grid = snapshot.maze
        self.draw_maze(grid)
        self.draw_pacgums(grid, snapshot)
        self.draw_pacman(grid, snapshot.pacman_pos, direction)
        self.draw_ghosts(grid, snapshot.ghosts)
        self.draw_hud(snapshot)
