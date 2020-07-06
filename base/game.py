from .window import *


class Game:

    def __init__(self, game_name):
        self.handle = find_handle_by_title_name(game_name)
        self.size = get_window_size(self.handle)

    def load_resources(self):
        pass

    def sign_in(self):
        pass

    def sign_out(self):
        pass

    def click(self):
        pass

    def drag(self):
        pass

    def back(self):
        pass

    def forward(self):
        pass
