import ctypes
import sys
import time
from abc import ABC

from base.game import Game


class PCR(Game, ABC):

    def __init__(self, game_name):
        super().__init__(game_name)

    def simple_loop(self, loop_time=1):
        # check current page is challenge?
        button_challenge = self._detect_position(self.resources.get('page_key', dict()).get('challenge', None))
        if not button_challenge:
            return
        button_start_fight = self.forward('start_fight', button_challenge)
        if not button_start_fight:
            return
        self.forward('challenge_end', button_start_fight)
        for i in range(loop_time - 1):
            button_next_step = self._detect_position(self.resources.get('button', dict()).get('next_step', None))
            if not button_next_step:
                return
            button_challenge_again = self.forward('challenge_again', button_next_step)
            if not button_challenge_again:
                return
            if not self.forward('checkpoint_again', button_challenge_again):
                return
            button_ok = self._detect_position(self.resources.get('button', dict()).get('ok', None))
            if not button_ok:
                return
            self.forward('challenge_end', button_ok)

        while True:
            print('oo loop')
            time.sleep(2)


def main():
    pcr = PCR('公主连结')
    pcr.simple_loop(3)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    try:
        main()
    except Exception as e:
        pass
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
