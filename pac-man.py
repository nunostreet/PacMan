import sys
import os

from config.parser import Parser
from engine.game import PacmanGame
from interface.app import APP


def main() -> int:
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    elif hasattr(sys, '_MEIPASS'):
        config_path = os.path.join(sys._MEIPASS, 'config', 'config.json')
    else:
        config_path = 'config/config.json'
    parser = Parser()
    config = parser.run_parsing(config_path)
    if config is None:
        return 1
    game = APP(PacmanGame(config), config)
    game.run_game()
    return 0


if __name__ == "__main__":
    sys.exit(main())
