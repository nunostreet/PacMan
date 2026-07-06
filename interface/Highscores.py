import pygame
import json


class Highscores:

    def __init__(
        self, filename: str, win: pygame.Surface, width: int, height: int
    ):
        self.file = filename
        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(None, 20)
        self.top_players: list[dict] = []

    def load(self):
        try:
            with open(self.file, "r") as f:
                fields: dict[str, int] = json.load(f)
                self.top_players = fields
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON syntax: {e}")
        except FileNotFoundError:
            return self.top_players

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.top_players, f, ensure_ascii=False)

    def add(self, name: str, score: int):
        player = {"name": name, "score": score}
        self.top_players.append(player)
        new_top = sorted(
            self.top_players, key=lambda player: player["score"], reverse=True
        )
        self.top_players = new_top[:10]

    def draw(self):
        for i in range(len(self.top_players)):
            player = self.top_players[i]
            play = self.font.render(
                f"{i + 1}: {player['name']} - {player['score']}", True, "white"
            )
            y = (i + 1) * (self.HEIGHT / (len(self.top_players) + 1))
            text_rect = play.get_rect()
            text_rect.center = (self.WIDTH // 2, y)
            self.WIN.blit(play, text_rect)
