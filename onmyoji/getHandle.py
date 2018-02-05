# coding=utf-8
import win32gui
import win32con
import time


def utf8_gbk(s):
    return s.decode('utf-8').encode('gbk')


def get_handle(s):
    title = s
    title = utf8_gbk(title)
    handle = win32gui.FindWindow(None, title)
    return handle


def set_front(s):
    h = get_handle(s)
    if h != 0:
        win32gui.SetForegroundWindow(h)


def set_back(s):
    h = get_handle(s)
    if h != 0:
        win32gui.SetBkMode(h, win32con.TRANSPARENT)


def get_pos(s):
    h = get_handle(s)
    left, top, right, bottom = win32gui.GetWindowRect(h)
    return left, top, right, bottom


_text = "阴阳师-网易游戏"

#set_front(_text)
#time.sleep(2)
#set_back(_text)


