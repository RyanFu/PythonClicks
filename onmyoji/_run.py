# encoding=utf-8
import cv2
import aircv as ac
import ImageGrab
import time
import numpy
import win32api
import thread
from Tkinter import *
from getHandle import *
from mouseCtrl import *

gui = Tk()
gui.title('阴阳师脚本-1.0')
gui.geometry('260x350')
mode = IntVar()
if_full = IntVar()
sleep_time = 0.4
_title = '阴阳师-网易游戏'
MODES = [(' 组队御魂觉醒  ', 1),
         ('   单刷探索    ', 2),
         (' 单刷御魂觉醒  ', 3),
         ('    暂停     ', 256)]

im_adventure = cv2.imread('images/adventure.png')
im_all = cv2.imread('images/all.png')
im_begin = cv2.imread('images/begin.png')
im_boss = cv2.imread('images/boss.png')
im_challenge = cv2.imread('images/challenge.png')
im_chest = cv2.imread('images/chest.png')
im_confirm = cv2.imread('images/confirm.png')
im_continue = cv2.imread('images/continue.png')
im_create = cv2.imread('images/create.png')
im_default = cv2.imread('images/default.png')
im_hard = cv2.imread('images/hard.png')
im_invite = cv2.imread('images/invite.png')
im_kill = cv2.imread('images/kill.png')
im_prepare = cv2.imread('images/prepare.png')
im_tick = cv2.imread('images/tick.png')


def grab_screen():
    pos = get_pos(_title)
    bbox = (pos[0]+8, pos[1], pos[2]-8, pos[3]-8)
    img = ImageGrab.grab(bbox)
    mat = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
    return mat


def im_find(_img, confidence, _str):
    if get_pos(_title)[0]<0 and get_pos(_title)[1]<0 and get_pos(_title)[2]<0 and get_pos(_title)[3]<0:
        lab.config(text='窗口被最小化,无法扫描!')
        return
    _imsrc = grab_screen()
    _matchPos = ac.find_template(_imsrc, _img)
    if _matchPos is None:
        pass
    elif _matchPos['confidence'] < confidence:
        #print _str, 'found but not exact, confidence is: ', _matchPos['confidence']
        pass
    elif _matchPos['confidence'] >= confidence:
        print _str, u'被找到! 准确度为: ', _matchPos['confidence']
        return True
    return False


def im_find_click(_img, confidence, _str):
    if get_pos(_title)[0]<0 and get_pos(_title)[1]<0 and get_pos(_title)[2]<0 and get_pos(_title)[3]<0:
        lab.config(text='窗口被最小化,无法扫描!')
        return
    _imsrc = grab_screen()
    _matchPos = ac.find_template(_imsrc, _img)
    if _matchPos is None:
        pass
    elif _matchPos['confidence'] < confidence:
        #print _str, 'found but not exact, confidence is: ', _matchPos['confidence']
        pass
    elif _matchPos['confidence'] >= confidence:
        lab.config(text=_str)
        #print _str, u'被找到并点击了一次 !  准确度为: ', _matchPos['confidence']
        mouse_left_click_return(get_pos(_title)[0] + _matchPos['result'][0],
                                get_pos(_title)[1] + _matchPos['result'][1])
        return True
    return False

def threadscan():
    while(1):
        if get_handle(_title) == 0:
            lab.config(text='请打开阴阳师电脑客户端!')
            continue
        if mode.get() == 1:
            lab.config(text='扫描中...')
            if im_find(im_invite, 0.65, '“邀请”'):
                time.sleep(sleep_time)
                if if_full.get() == 1:
                    continue
            im_find_click(im_all, 0.99, '“所有人”')
            im_find_click(im_default, 0.99, '“默认邀请队友”')
            im_find_click(im_begin, 0.99, '“开始战斗”')
            im_find_click(im_prepare, 0.80, '“准备”')
            im_find_click(im_continue, 0.60, '“点击屏幕继续”')
            im_find_click(im_tick, 0.99, '“钩钩”')
            im_find_click(im_confirm, 0.99, '“确定”')
            im_find_click(im_create, 0.99, '“创建”')
        elif mode.get() == 2:
            lab.config(text="扫描中...")
            im_find_click(im_prepare, 0.6, '“准备”')
            im_find_click(im_continue, 0.6, '“点击屏幕继续”')
            im_find_click(im_adventure, 0.7, '“探索”')
            im_find_click(im_hard, 0.8, '“困难章节”')
            im_find_click(im_boss, 0.6, '“头目”')
            if im_find_click(im_chest, 0.8, '“宝箱”'):
                time.sleep(3)
                mouse_left_click_return(get_pos(_title)[0] + 100, get_pos(_title)[1] + 100)
            if not im_find_click(im_kill, 0.6, '“小怪”'):
                mouse_left_click_return(get_pos(_title)[0] + 610, get_pos(_title)[1] + 370)
                pass
        elif mode.get() == 3:
            lab.config(text="扫描中...")
            im_find_click(im_prepare, 0.6, '“准备”')
            im_find_click(im_continue, 0.6, '“点击屏幕继续”')
            im_find_click(im_challenge, 0.6, '“挑战”')
        else:
            lab.config(text="<暂停>")
        time.sleep(sleep_time)


lab = Label(gui, text="initializing...", height=5, width=40, fg="brown")
lab.pack()
Checkbutton(gui, text='是否等待满员', variable=if_full).pack()
for name, val in MODES:
    Radiobutton(gui, text=name, value=val, variable=mode, indicatoron=0, height=2, width=15, bg='grey').pack()
Label(gui, text="-- developed by iclosed  ", height=2, width=22, fg="blue").pack(side=RIGHT)
thread.start_new_thread(threadscan, ())

mainloop()
