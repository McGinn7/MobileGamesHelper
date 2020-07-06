import numpy as np
import win32con
import win32gui
import win32ui

from PIL import Image


def get_window_coordinate(handle):
    return win32gui.GetWindowRect(handle)


def get_window_size(handle):
    left, top, right, bottom = get_window_coordinate(handle)
    width = abs(left - right)
    height = abs(top - bottom)
    return width, height


def prtscn(handle):
    w, h = get_window_size(handle)
    # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hwnd_dc = win32gui.GetWindowDC(handle)
    # 创建设备描述表
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    # 创建内存设备描述表
    save_dc = mfc_dc.CreateCompatibleDC()
    # 创建位图对象
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(save_bitmap)
    # 截图至内存设备描述表
    img_dc = mfc_dc
    mem_dc = save_dc
    mem_dc.BitBlt((0, 0), (w, h), img_dc, (0, 0), win32con.SRCCOPY)
    bmp_info = save_bitmap.GetInfo()
    bmp_str = save_bitmap.GetBitmapBits(True)
    # 生成图像
    im = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'RGBA', 0, 1)
    im = np.array(im)
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(handle, hwnd_dc)
    return im


# TODO: refactor
def find_handle_by_title_name(title_name):
    handles = []
    win32gui.EnumWindows(lambda _hwnd, result: result.append([_hwnd,
                                                              win32gui.GetClassName(_hwnd),
                                                              win32gui.GetWindowText(_hwnd)])
                         , handles)
    handle = None
    for (_hwnd, class_name, win_title) in handles:
        is_target = True
        for key_word in [title_name]:
            if key_word not in win_title:
                is_target = False
                break
        if is_target:
            handle = _hwnd
            break
    return handle
