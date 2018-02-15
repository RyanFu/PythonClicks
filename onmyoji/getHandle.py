# coding=utf-8
import win32gui
import win32con
import time
import ctypes


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


def isIconic(s):
    h = get_handle(s)
    return win32gui.IsIconic(h)


def window_size(s):
    
    h = get_handle(s)
    left, right, top, bottom = get_pos(s)
    win32gui.SetWindowPos(h, None, left, top,right-left, bottom-top, win32con.SWP_NOSENDCHANGING|win32con.SWP_SHOWWINDOW)


#_text = "任务管理器"
#window_size(_text)
