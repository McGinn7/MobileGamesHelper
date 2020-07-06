import random
import time

import win32con
import win32gui


def _w_param(x, y):
    return y << 16 | x


def click(handle, xy, noisy_offset=8):
    x, y = int(xy[0]), int(xy[1])
    if isinstance(noisy_offset, int):
        x += random.randint(-noisy_offset, noisy_offset)
        y += random.randint(-noisy_offset, noisy_offset)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, _w_param(x, y))
    time.sleep(0.1)
    win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, 0, _w_param(x, y))


def drag(handle, start_xy, end_xy, speed=20):
    x0, y0 = int(start_xy[0]), int(start_xy[1])
    x1, y1 = int(end_xy[0]), int(end_xy[1])
    win32gui.PostMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, _w_param(x, y))
    win32gui.SendMessage(handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON, _w_param(x, y))
    for i in range(speed):
        time.sleep(0.05)
        # TODO: refactor
        nx = x0 + int((x1 - x0) / speed * (i + 1))
        ny = y0 + int((y1 - y0) / speed * (i + 1))
        win32gui.PostMessage(handle, win32con.WM_MOUSEMOVE, win32con.MK_LBUTTON,
                             _w_param(nx, ny))
    time.sleep(0.05)
    win32gui.PostMessage(handle, win32con.WM_LBUTTONUP, 0, _w_param(x1, y1))


def scroll(handle):
    pass


def coordinate():
    [x, y] = win32gui.GetCursorPos()
    return x, y
