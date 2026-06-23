from dataclasses import dataclass
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
    """

    x: int
    y: int
    edible: bool = False


@dataclass
class GameConfig:
    """Configuração de um nível carregada do config.json.

    Attributes:
        width: Largura do labirinto.
        height: Altura do labirinto.
        lives: Número de vidas iniciais.
        pacgum_count: Número de pacgums por nível.
        points_per_pacgum: Pontos por pacgum comido.
        points_per_super_pacgum: Pontos por super-pacgum comido.
        points_per_ghost: Pontos por fantasma comido.
        level_max_time: Tempo máximo por nível em segundos.
        seed: Seed do labirinto (42 no nível 1, 0 nos seguintes).
        highscore_filename: Caminho para o ficheiro de highscores.
    """

    width: int = 15
    height: int = 15
    lives: int = 3
    pacgum_count: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
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
        score: Pontuação atual.
        lives: Vidas restantes.
        level: Nível atual (começa em 1).
        time_remaining: Segundos restantes no nível.
        status: Estado atual do jogo.
    """

    pacman_pos: tuple[int, int]
    ghosts: list[GhostState]
    pacgums: list[list[int]]
    score: int
    lives: int
    level: int
    time_remaining: float
    status: GameStatus
