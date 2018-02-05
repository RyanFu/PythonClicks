import win32api
import win32con
import time
from ctypes import *


class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]


def mouse_move(x, y):
    windll.user32.SetCursorPos(x, y)


def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)


def mouse_left_click(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def mouse_right_click(x=None, y=None):
    if not x is None and not y is None:
        mouse_move(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


def mouse_wheeldown():
    pass
    #win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -1) ############################
    #win32api.mouse_event/(win32con.MOUSEEVENTF_WHEEL, 1158, 518, -120)

	
#win32api.SetCursorPos((0, 0))
#time.sleep(2)
#m.move(500, 500)
#time.sleep(2)


