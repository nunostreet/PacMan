import pygame
import json


class Highscores:
    """Loads, updates, persists, and draws the top-10 list."""

    def __init__(
        self, filename: str, win: pygame.Surface, width: int, height: int
    ) -> None:
        """Set up the highscores screen and the backing file.

        Args:
            filename: Path to the JSON file that stores scores.
            win: Pygame surface to draw on.
            width: Window width in pixels.
            height: Window height in pixels.
        """
        self.file = filename
        self.WIN = win
        self.WIDTH = width
        self.HEIGHT = height
        self.font = pygame.font.Font(
            "assets/fonts/PressStart2P-Regular.ttf", 12
        )
        self.top_players: list[dict] = []

    def load(self) -> None:
        """Load top_players from the highscores JSON file."""
        try:
            with open(self.file, "r") as f:
                fields: list[dict] = json.load(f)
                self.top_players = fields
        except json.JSONDecodeError as e:
            print(f"Warning: invalid highscore file, starting empty: {e}")
            self.top_players = []
        except FileNotFoundError:
            self.top_players = []

    def save(self) -> None:
        """Write the current top_players list to the JSON file."""
        with open(self.file, "w") as f:
            json.dump(self.top_players, f, ensure_ascii=False)

    def add(self, name: str, score: int) -> None:
        """Insert a new score and keep only the top 10, sorted descending.

        Args:
            name: Player name.
            score: Player score.
        """
        player = {"name": name, "score": score}
        self.top_players.append(player)
        new_top = sorted(
            self.top_players, key=lambda player: player["score"], reverse=True
        )
        self.top_players = new_top[:10]

    def draw(self) -> None:
        """Draw the sorted list of top players and their scores."""
        for i in range(len(self.top_players)):
            player = self.top_players[i]
            play = self.font.render(
                f"{i + 1}: {player['name']} - {player['score']}", True, "white"
            )
            y = (i + 1) * (self.HEIGHT / (len(self.top_players) + 1))
            text_rect = play.get_rect()
            text_rect.center = (self.WIDTH // 2, int(y))
            self.WIN.blit(play, text_rect)
