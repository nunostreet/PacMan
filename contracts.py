from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    """Direções de movimento possíveis."""

    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GameStatus(Enum):
    """Estado atual do jogo."""

    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"


@dataclass
class GhostState:
    """Estado de um fantasma num dado momento.

    Attributes:
        x: Posição horizontal.
        y: Posição vertical.
        edible: True se o fantasma pode ser comido.
        active: False quando está em respawn (UI não deve desenhar).
    """

    x: int
    y: int
    edible: bool = False
    active: bool = True


@dataclass
class GameConfig:
    """Configuração do jogo carregada do config.json.

    Attributes:
        levels: Lista de tamanhos de labirinto por nível [(width, height), ...].
        lives: Número de vidas iniciais.
        pacgum_count: Número de pacgums por nível.
        points_per_pacgum: Pontos por pacgum comido.
        points_per_super_pacgum: Pontos por super-pacgum comido.
        points_per_ghost: Pontos por fantasma comido.
        ghost_respawn_time: Segundos até um fantasma comido reaparecer.
        level_max_time: Tempo máximo por nível em segundos.
        seed: Seed do labirinto do nível 1 (níveis seguintes usam seed=0).
        highscore_filename: Caminho para o ficheiro de highscores.
    """

    levels: list[tuple[int, int]] = field(default_factory=lambda: [
        (15, 11), (17, 13), (19, 15), (21, 15), (23, 17),
        (25, 17), (25, 19), (27, 19), (29, 21), (31, 21)
    ])
    lives: int = 3
    pacgum_count: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    ghost_respawn_time: float = 5.0
    level_max_time: int = 90
    seed: int = 42
    highscore_filename: str = "highscores.json"


@dataclass
class GameSnapshot:
    """Estado completo do jogo num dado momento, para a UI renderizar.

    Attributes:
        pacman_pos: Posição do Pacman (x, y).
        ghosts: Lista com o estado de cada fantasma.
        pacgums: Grelha com 0 (vazio), 1 (pacgum) ou 2 (super-pacgum).
        maze: Grelha de bitmask do labirinto (N=1, E=2, S=4, W=8)
            para desenhar paredes.
        score: Pontuação atual.
        lives: Vidas restantes.
        level: Nível atual (começa em 1).
        time_remaining: Segundos restantes no nível.
        level_max_time: Tempo máximo do nível em segundos (para a barra de HUD).
        status: Estado atual do jogo.
    """

    pacman_pos: tuple[int, int]
    ghosts: list[GhostState]
    pacgums: list[list[int]]
    maze: list[list[int]]
    score: int
    lives: int
    level: int
    time_remaining: float
    level_max_time: float
    status: GameStatus


from engine.game import PacmanGame  # noqa: E402
