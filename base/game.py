# coding=utf-8
import json
from abc import abstractmethod

import cv2
import numpy as np

from base import image
from base import mouse
from base import window


class Game:

    def __init__(self, game_name):
        self.game_name = game_name
        self.handle = window.find_handle_by_title_name(self.game_name)
        self.window_size = window.get_window_size(self.handle)
        self.cfg = self.load_config()

    def load_config(self):
        game2config = json.load(open('../config/game2config.json', 'r', encoding='utf-8'))
        config_name = game2config.get(self.game_name, None)
        if isinstance(config_name, str):
            if not config_name.endswith('.json'):
                config_name += '.json'
            return json.load(open('../config/{}'.format(config_name), 'r', encoding='utf-8'))
        return dict()

    def load_resources(self):
        pass

    @abstractmethod
    def sign_in(self):
        pass

    @abstractmethod
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
