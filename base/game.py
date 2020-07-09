# coding=utf-8
import json
import os
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
        self.resources = dict()
        self.load_resources(self.cfg.get('resource_dir'), self.resources)

    def load_config(self):
        game2config = json.load(open('../config/game2config.json', 'r', encoding='utf-8'))
        config_name = game2config.get(self.game_name, None)
        if isinstance(config_name, str):
            if not config_name.endswith('.json'):
                config_name += '.json'
            return json.load(open('../config/{}'.format(config_name), 'r', encoding='utf-8'))
        return dict()

    def load_resources(self, path, _resources, depth=0):
        for dof in os.listdir(path):
            path_dof = os.path.join(path, dof)
            if os.path.isdir(path_dof):
                _resources[dof] = dict()
                self.load_resources(path_dof, _resources[dof], depth + 1)
            else:
                filename = dof.split('.')[0]
                abp_dof = os.path.abspath(path_dof)
                _resources[filename] = abp_dof

    @abstractmethod
    def sign_in(self):
        pass

    @abstractmethod
    def sign_out(self):
        pass

    def _detect_position(self, param, retry_time=2):
        if isinstance(param, str):
            im = cv2.imread(param)
            param = image.resize(im, self.cfg.get('resource_background_resolution', [1920, 1080]), self.window_size)
        if isinstance(param, np.ndarray):
            for _ in range(retry_time):
                position = image.detect_img_template(param, window.prtscn(self.handle),
                                                     self.cfg.get("template_threshold", 0.8))
                if position:
                    return position
        return []

    def click(self, param, retry_time=2):
        if isinstance(param, str):
            param = self._detect_position(param)
            if not param:
                return
        if isinstance(param, tuple) or isinstance(param, list):
            mouse.click(self.handle, param, self.cfg.get('click_offset', 8))

    def drag(self, param, end_xy):
        if isinstance(param, str):
            param = self._detect_position(param)
            if not param:
                return
        if isinstance(param, tuple) or isinstance(param, list):
            mouse.drag(self.handle, param, end_xy, self.cfg.get('drag_speed', 20))

    def backward(self):
        pass

    def forward(self):
        pass
