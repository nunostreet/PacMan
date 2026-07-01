import pygame
from contracts import Direction
from engine.game import PacmanGame
from config.parser import Parser


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

    def draw_maze(self, grid: list[list[int]]):
        CELL_H = self.HEIGHT/len(grid)
        CELL_W = self.WIDTH/len(grid[0])
        for i in range(len(grid)):
            y = i * CELL_H
            for j in range(len(grid[i])):
                x = j * CELL_W
                pygame.draw.rect(self.WIN, 'black', (x, y, CELL_W, CELL_H))

                # parede norte
                if not (grid[i][j] & 1):
                    pygame.draw.line(self.WIN, 'white', (x, y), (x + CELL_W, y), 1)

                # parede este
                if not (grid[i][j] & 2):
                    pygame.draw.line(self.WIN, 'white', (x + CELL_W, y), (x + CELL_W, y + CELL_H), 1)

                # parede sul
                if not (grid[i][j] & 4):
                    pygame.draw.line(self.WIN, 'white', (x, y + CELL_H), (x + CELL_W, y + CELL_H), 1)

                # parede oeste
                if not (grid[i][j] & 8):
                    pygame.draw.line(self.WIN, 'white', (x, y), (x, y + CELL_H), 1)

    def draw_pacman(self, grid: list[list[int]], pacman_pos: tuple[int, int]):
        CELL_H = self.HEIGHT/len(grid)
        CELL_W = self.WIDTH/len(grid[0])
        x = pacman_pos[0] * CELL_W + (CELL_W/2)
        y = pacman_pos[1] * CELL_H + (CELL_H/2)
        pygame.draw.circle(self.WIN, 'blue', (x, y), 5)

    def run_game(self):
        while self.run:
            dt = self.timer.tick(self.fps)/1000
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
            grid = maze.maze
            pacman_pos = maze.pacman_pos
            self.draw_maze(grid)
            self.draw_pacman(grid, pacman_pos)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    config = Parser()
    parse = config.run_parsing()
    pacman = PacmanGame(parse)
    game = APP(pacman)
    game.run_game()
