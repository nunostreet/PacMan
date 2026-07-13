import pygame
import json


class Highscores:
    """Carrega, atualiza, persiste e desenha a lista do top-10."""

    def __init__(
        self, filename: str, win: pygame.Surface, width: int, height: int
    ):
        """Configura o ecrã de highscores e o ficheiro que os armazena.

        Args:
            filename: Caminho do ficheiro JSON que guarda as pontuações.
            win: A superfície do pygame onde o ecrã é desenhado.
            width: Largura da janela em pixels.
            height: Altura da janela em pixels.
        """
        self.file = filename
        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(None, 20)
        self.top_players: list[dict] = []

    def load(self):
        """Carrega ``top_players`` a partir do ficheiro JSON de highscores.

        Raises:
            Exception: Se o ficheiro contiver JSON inválido.

        Returns:
            A lista ``top_players`` atual se o ficheiro ainda não
            existir, caso contrário ``None``.
        """
        try:
            with open(self.file, "r") as f:
                fields: dict[str, int] = json.load(f)
                self.top_players = fields
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON syntax: {e}")
        except FileNotFoundError:
            return self.top_players

    def save(self):
        """Escreve a lista ``top_players`` atual no ficheiro JSON."""
        with open(self.file, "w") as f:
            json.dump(self.top_players, f, ensure_ascii=False)

    def add(self, name: str, score: int):
        """Insere uma nova pontuação e mantém só o top 10, ordenado desc.

        Args:
            name: O nome do jogador.
            score: A pontuação do jogador.
        """
        player = {"name": name, "score": score}
        self.top_players.append(player)
        new_top = sorted(
            self.top_players, key=lambda player: player["score"], reverse=True
        )
        self.top_players = new_top[:10]

    def draw(self):
        """Desenha a lista ordenada dos melhores jogadores e pontuações."""
        for i in range(len(self.top_players)):
            player = self.top_players[i]
            play = self.font.render(
                f"{i + 1}: {player['name']} - {player['score']}", True, "white"
            )
            y = (i + 1) * (self.HEIGHT / (len(self.top_players) + 1))
            text_rect = play.get_rect()
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(play, text_rect)
