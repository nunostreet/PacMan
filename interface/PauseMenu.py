from interface.OptionMenu import OptionMenu


class PauseMenu(OptionMenu):

    def __init__(self, win, width, height):
        super().__init__(win, width, height)
        self.options = ["Continue Game",
                        "Exit"]
        self.selected_option = 0
