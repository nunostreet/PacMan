from contracts import (
    GameConfig, GameStatus, GameSnapshot,
    Direction, GhostState
)
from .maze import MazeLoader
from .player import Pacman
from .ghost import Ghost


class PacmanGame:
    """Lógica principal do jogo Pac-Man.

    Gere o estado do jogo a cada frame e expõe-o via GameSnapshot.
    Não tem dependências gráficas — a UI consome esta classe via tick().

    Attributes:
        _config: Configuração do jogo.
        _maze: Labirinto atual com vizinhos e pacgums.
        _pacman: Estado do jogador.
        _ghosts: Lista dos 4 fantasmas.
        _score: Pontuação acumulada.
        _level: Nível atual (começa em 1).
        _time_remaining: Segundos restantes no nível.
        _status: Estado atual do jogo.
    """

    def __init__(self, config: GameConfig) -> None:
        """Inicializa o jogo com a configuração fornecida.

        Args:
            config: Configuração carregada do config.json.
        """
        self._config = config
        width, height = self._config.levels[0]
        self._width = width
        self._height = height
        self._maze = MazeLoader()
        self._maze.load(width, height, config.seed, config.pacgum_count)
        self._pacman = Pacman(width // 2, height // 2, config.lives)
        self._ghosts = [
            Ghost(0, 0),
            Ghost(width - 1, 0),
            Ghost(0, height - 1),
            Ghost(width - 1, height - 1),
        ]
        self._score = 0
        self._level = 1
        self._time_remaining = float(config.level_max_time)
        self._status = GameStatus.PLAYING
        self._frozen_ghosts = False
        self._invincible = False
        self._cheat_used = False

    def tick(self, direction: Direction | None, dt: float) -> GameSnapshot:
        """Avança o estado do jogo um frame.

        Args:
            direction: Direção do jogador, ou None se não houve input.
            dt: Tempo em segundos desde o último frame.

        Returns:
            Estado atual do jogo para a UI renderizar.
        """

        self._time_remaining -= dt
        if direction is not None:
            self._pacman.move(direction, self._maze.neighbors)

        px, py = self._pacman.x, self._pacman.y
        cell = self._maze.pacgums[py][px]
        if cell == 1:
            self._score += self._config.points_per_pacgum
            self._maze.pacgums[py][px] = 0
        if cell == 2:
            self._score += self._config.points_per_super_pacgum
            self._maze.pacgums[py][px] = 0
            for ghost in self._ghosts:
                ghost.edible = True

        for ghost in self._ghosts:
            if self._frozen_ghosts:
                continue
            ghost.move(self._maze.neighbors, (px, py))
            ghost.update(dt)

        for ghost in self._ghosts:
            if ghost.respawn_timer == 0 and (px, py) == (ghost.x, ghost.y):
                if ghost.edible:
                    self._score += self._config.points_per_ghost
                    ghost.respawn(self._config.ghost_respawn_time)
                elif self._invincible:
                    continue
                else:
                    if self._pacman.lives <= 1:
                        self._status = GameStatus.GAME_OVER
                    else:
                        self._pacman.respawn(
                            self._width // 2, self._height // 2
                        )
                        px, py = self._pacman.x, self._pacman.y

        if all(cell == 0 for row in self._maze.pacgums for cell in row):
            if self._level >= len(self._config.levels):
                self._status = GameStatus.WIN
            else:
                self._level += 1
                self._load_level()

        if self._time_remaining <= 0:
            self._status = GameStatus.GAME_OVER

        return GameSnapshot(
            pacman_pos=(self._pacman.x, self._pacman.y),
            ghosts=[
                GhostState(g.x, g.y, g.edible, g.respawn_timer == 0)
                for g in self._ghosts
            ],
            pacgums=self._maze.pacgums,
            maze=self._maze.maze_grid,
            score=self._score,
            lives=self._pacman.lives,
            level=self._level,
            time_remaining=self._time_remaining,
            level_max_time=self._config.level_max_time,
            status=self._status,
            cheat_used=self._cheat_used
        )

    def _load_level(self) -> None:
        """Carrega o labirinto e repõe entidades para o nível atual."""
        width, height = self._config.levels[self._level - 1]
        self._width = width
        self._height = height
        seed = self._config.seed if self._level == 1 else 0
        self._maze.load(width, height, seed, self._config.pacgum_count)
        self._pacman.x = width // 2
        self._pacman.y = height // 2
        self._ghosts = [
            Ghost(0, 0),
            Ghost(width - 1, 0),
            Ghost(0, height - 1),
            Ghost(width - 1, height - 1),
        ]
        self._time_remaining = float(self._config.level_max_time)
        self._status = GameStatus.PLAYING

    # ----- CHEAT MODE FEATURES ------

    def set_frozen_ghosts(self, value: bool) -> None:
        """Ativa ou desativa o freeze dos fantasmas.

        Args:
            value: True para congelar, False para retomar movimento.
        """
        self._frozen_ghosts = value
        self._cheat_used = True

    def set_invincible(self, value: bool) -> None:
        """Ativa ou desativa a invencibilidade do Pacman.

        Args:
            value: True para invencível, False para normal.
        """
        self._invincible = value
        self._cheat_used = True

    def add_lives(self, count: int = 1) -> None:
        """Adiciona 1 vida ao jogador."""
        self._pacman.lives += count
        self._cheat_used = True

    def skip_level(self) -> None:
        """Salta 1 nível se ainda for possível."""
        self._cheat_used = True
        if self._level >= len(self._config.levels):
            self._status = GameStatus.WIN
        else:
            self._level += 1
            self._load_level()

    def go_back_level(self) -> None:
        """Volta 1 nível se ainda for possível."""
        if self._level > 1:
            self._level -= 1
            self._load_level()
            self._cheat_used = True

        # COMENTÁRIO PARA O PEDRO --> INVALIDAR HIGH SCORE
        # QUANDO ALGUMA CHEAT FOR ATIVADA
