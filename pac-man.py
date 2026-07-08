from config.parser import Parser



def main() -> int:
	"""
	Run the application and return a process exit code.0
	"""

	try:
		config = Parser()
		if config is None:
			return 1
    	parse = config.run_parsing()
		
    pacman = PacmanGame(parse)
    game = APP(pacman, parse)
    game.run_game()