import sys

from config.parser import Parser
from engine.game import PacmanGame
from interface.app import APP


def main() -> int:
    parser = Parser()
    config = parser.run_parsing()
    if config is None:
        return 1
    game = APP(PacmanGame(config), config)
    game.run_game()
    return 0


if __name__ == "__main__":
    sys.exit(main())
