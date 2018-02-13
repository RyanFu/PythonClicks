# encoding=utf-8
import aircv as ac
import cv2
import ImageGrab
import numpy
import os
import random
import thread
import time
import win32api
import socket
from getHandle import *
from mouseCtrl import *
from Tkinter import *
from tkinter import ttk 

gui = Tk()
gui.title('阴阳师脚本-2.5')
gui.geometry('250x450')
gui.iconbitmap('images/ssr.ico')
mode = IntVar()
if_full = IntVar()
mob = StringVar()
shut_time = StringVar()
_title = '阴阳师-网易游戏'

im_accept = cv2.imread('images/accept.png')
im_adventure = cv2.imread('images/adventure.png')
im_all = cv2.imread('images/all.png')
im_attack = cv2.imread('images/attack.png')
im_begin = cv2.imread('images/begin.png')
im_boss = cv2.imread('images/boss.png')
im_challenge = cv2.imread('images/challenge.png')
im_chest = cv2.imread('images/chest.png')
im_confirm = cv2.imread('images/confirm.png')
im_continue = cv2.imread('images/continue.png')
im_create = cv2.imread('images/create.png')
im_default = cv2.imread('images/default.png')
im_erkou = cv2.imread('images/erkou.png')
im_fight = cv2.imread('images/fight.png')
im_guishi = cv2.imread('images/guishi.png')
im_haifang = cv2.imread('images/haifang.png')
im_hall2team = cv2.imread('images/hall2team.png')
im_hard = cv2.imread('images/hard.png')
im_invite = cv2.imread('images/invite.png')
im_kill = cv2.imread('images/kill.png')
im_manual = cv2.imread('images/manual.png')
im_prepare = cv2.imread('images/prepare.png')
im_refresh = cv2.imread('images/refresh.png')
im_rihe = cv2.imread('images/rihe.png')
im_songwan = cv2.imread('images/songwan.png')
im_team = cv2.imread('images/team.png')
im_tiaotiao = cv2.imread('images/tiaotiao.png')
im_tick = cv2.imread('images/tick.png')
im_yaoqi = cv2.imread('images/yaoqi.png')


def poweroff():
    send_msg('$delay_shutdown')
    if shut_time.get()==u'半小时后':
        os.popen('shutdown -s -t 1800')
    elif shut_time.get()==u'一小时后':
        os.popen('shutdown -s -t 3600')
    elif shut_time.get()==u'两小时后':
        os.popen('shutdown -s -t 7200')
    elif shut_time.get()==u'三小时后':
        os.popen('shutdown -s -t 10800')
    elif shut_time.get()==u'四小时后':
        os.popen('shutdown -s -t 14400')
    elif shut_time.get()==u'六小时后':
        os.popen('shutdown -s -t 21600')
        

def cancel():
    send_msg('$shutdown_cancel')
    os.popen('shutdown -a')


def send_msg(str):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(str, ('193.112.10.74', 31189))
    s.close()    
    
    
def tellme():
    if mode.get() == 1:
        send_msg('$组队_御魂/觉醒')
    elif mode.get() == 2:
        send_msg('$组队_探索')
    elif mode.get() == 3:
        send_msg('$单刷_御/觉/斗鸡')
    elif mode.get() == 4:
        send_msg('$单刷_探索')  
    elif mode.get() == 5:
        if mob.get()==u'日和坊':
            send_msg('$妖气封印_日和坊')
        elif mob.get()==u'小松丸':
            send_msg('$妖气封印_小松丸')
        elif mob.get()==u'以上全部':
            send_msg('$妖气封印ALL')
        else:
            send_msg('$妖气封印Others')
    else:
        send_msg('$暂停')
        
        
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
        #print _str, u'被找到! 准确度为: ', _matchPos['confidence']
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


def im_find_click_offset(_img, confidence, _str, x, y):
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
        mouse_left_click_return(get_pos(_title)[0] + _matchPos['result'][0] + x,
                                get_pos(_title)[1] + _matchPos['result'][1] + y)
        return True
    return False

    
def threadscan():
    while(1):
        if get_handle(_title) == 0:
            lab.config(text='请打开阴阳师电脑客户端!')
            continue
        if mode.get() == 1:
            lab.config(text='扫描中...')
            if im_find(im_invite, 0.9, '“邀请”'):
                if if_full.get() == 1:
                    continue
            im_find_click(im_all, 0.8, '“所有人”')
            im_find_click(im_default, 0.8, '“默认邀请队友”')
            im_find_click(im_begin, 0.8, '“开始战斗”')
            im_find_click(im_prepare, 0.9, '“准备”')
            im_find_click(im_continue, 0.7, '“点击屏幕继续”')
            im_find_click(im_tick, 0.9, '“同意继续”')
            im_find_click(im_confirm, 0.8, '“确定”')
            im_find_click(im_create, 0.8, '“创建”')
            im_find_click(im_accept, 0.9, '“接受”')
            
        elif mode.get() == 2:
            lab.config(text="扫描中...")
            im_find_click(im_prepare, 0.9, '“准备”')
            im_find_click(im_continue, 0.6, '“点击屏幕继续”')
            im_find_click(im_team, 0.7, '“组队”')
            im_find_click(im_hard, 0.8, '“困难章节”')
            im_find_click(im_boss, 0.9, '“头目”')
            im_find_click(im_tick, 0.9, '“同意继续”')
            im_find_click(im_accept, 0.9, '“接受”')
            im_find_click(im_chest, 0.8, '“宝箱”')
            if not im_find_click(im_kill, 0.9, '“小怪”'):
                mouse_left_click_return(get_pos(_title)[0] + 820, get_pos(_title)[1] + 500)
        
        elif mode.get() == 3:
            lab.config(text="扫描中...")
            im_find_click(im_prepare, 0.9, '“准备”')
            im_find_click(im_continue, 0.7, '“点击屏幕继续”')
            im_find_click(im_challenge, 0.7, '“挑战”')
            im_find_click(im_fight, 0.8, '“战”')
            im_find_click(im_manual, 0.7, '“手动->自动”')
            im_find_click(im_attack, 0.7, '“进攻”')
            im_find_click(im_accept, 0.9, '“接受”')
        
        elif mode.get() == 4:
            lab.config(text="扫描中...")
            im_find_click(im_prepare, 0.9, '“准备”')
            im_find_click(im_continue, 0.7, '“点击屏幕继续”')
            im_find_click(im_adventure, 0.7, '“探索”')
            im_find_click(im_hard, 0.8, '“困难章节”')
            im_find_click(im_boss, 0.9, '“头目”')
            im_find_click(im_accept, 0.9, '“接受”')
            im_find_click(im_chest, 0.8, '“宝箱”')
            if not im_find_click(im_kill, 0.9, '“小怪”'):
                mouse_left_click_return(get_pos(_title)[0] + 820, get_pos(_title)[1] + 500)
        
        elif mode.get() == 5:
            lab.config(text="扫描中...")
            if mob.get()==u'日和坊':
                im_find_click_offset(im_rihe, 0.7, '“日和坊”', 420, 10)
            elif mob.get()==u'海坊主':
                im_find_click_offset(im_haifang, 0.7, '“海坊主”', 420, 10)
            elif mob.get()==u'鬼使黑':
                im_find_click_offset(im_guishi, 0.7, '“鬼使黑”', 420, 10)
            elif mob.get()==u'跳跳哥哥':
                im_find_click_offset(im_tiaotiao, 0.7, '“跳跳哥哥”', 415, 10)
            elif mob.get()==u'小松丸':
                im_find_click_offset(im_songwan, 0.7, '“小松丸”', 420, 10)    
            elif mob.get()==u'二口女':
                im_find_click_offset(im_erkou, 0.7, '“二口女”', 420, 10)
            elif mob.get()==u'以上全部':
                im_find_click_offset(im_rihe, 0.7, '“日和坊”', 420, 10)
                im_find_click_offset(im_haifang, 0.7, '“海坊主”', 420, 10)
                im_find_click_offset(im_guishi, 0.7, '“鬼使黑”', 420, 10)
                im_find_click_offset(im_tiaotiao, 0.7, '“跳跳哥哥”', 415, 10)
                im_find_click_offset(im_songwan, 0.7, '“小松丸”', 420, 10)
                im_find_click_offset(im_erkou, 0.7, '“二口女”', 420, 10)
            im_find_click(im_refresh, 0.7, '“刷新”')
            im_find_click(im_prepare, 0.9, '“准备”')
            im_find_click(im_continue, 0.7, '“点击屏幕继续”')
            if im_find(im_hall2team, 0.7, '“组队大厅”'):
                time.sleep(2)
                if im_find_click(im_hall2team, 0.7, '“组队大厅”'):
                    time.sleep(random.uniform(0.7, 1.1))
                    mouse_drag(get_pos(_title)[0] + 200, get_pos(_title)[1] + 500, \
                                get_pos(_title)[0] + 200, get_pos(_title)[1] + 400)
                    time.sleep(random.uniform(0.5, 0.6))
                    im_find_click(im_yaoqi, 0.9, u'“妖气封印”')
            
        else:
            lab.config(text="选择任一模式以开始..")
        time.sleep(random.uniform(0.5, 0.7))

        
########################################################################
lab = Label(gui, text="initializing...", font='幼圆 -14 bold', fg="brown")
lab.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.1)

Radiobutton(gui, text='组队_御魂/觉醒', value=1, variable=mode, borderwidth=4, indicatoron=0, command=tellme, \
font='幼圆 -14', height=2, width=7, bg='grey').place(relx=0.2, rely=0.15, relwidth=0.43, relheight=0.1)
Checkbutton(gui, text='满员', variable=if_full, font='幼圆 -13').place(\
relx=0.63, rely=0.15, relwidth=0.17, relheight=0.1)

Radiobutton(gui, text='组队_探索', value=2, variable=mode, borderwidth=4, indicatoron=0, command=tellme, \
font='幼圆 -14', height=2, width=7, bg='grey').place(relx=0.2, rely=0.25, relwidth=0.6, relheight=0.1)

Radiobutton(gui, text='单刷_御/觉/斗鸡', value=3, variable=mode, borderwidth=4, indicatoron=0, command=tellme, \
font='幼圆 -14', height=2, width=7, bg='grey').place(relx=0.2, rely=0.35, relwidth=0.6, relheight=0.1)

Radiobutton(gui, text='单刷_探索', value=4, variable=mode, borderwidth=4, indicatoron=0, command=tellme, \
font='幼圆 -14', height=2, width=7, bg='grey').place(relx=0.2, rely=0.45, relwidth=0.6, relheight=0.1)

combo = ttk.Combobox(gui, textvariable=mob, font='幼圆 -13')  
combo["values"] = ('日和坊','海坊主', '鬼使黑', '跳跳哥哥', '小松丸', '二口女', '以上全部')
combo["state"] = "readonly" 
combo.current(0)
combo.place(relx=0.2, rely=0.55, relwidth=0.31, relheight=0.1)

Radiobutton(gui, text='妖气封印', value=5, variable=mode, borderwidth=4, indicatoron=0, command=tellme, \
font='幼圆 -14', height=2, width=7, bg='grey').place(relx=0.51, rely=0.55, relwidth=0.29, relheight=0.1)

Radiobutton(gui, text='[暂停]', value=256, variable=mode, borderwidth=7, indicatoron=0, command=tellme, \
font='幼圆 -16', height=2, width=7, bg='grey').place(relx=0.2, rely=0.66, relwidth=0.6, relheight=0.1)

shutd = ttk.Combobox(gui, textvariable=shut_time, font='幼圆 -14')  
shutd["values"] = ('半小时后','一小时后', '两小时后', '三小时后', '四小时后', '六小时后')  
shutd["state"] = "readonly" 
shutd.current(0)
shutd.place(relx=0.2, rely=0.78, relwidth=0.31, relheight=0.08)
Button(gui, text='关机', borderwidth=3, bg='#8B636C', command=poweroff, font='幼圆 -14'\
).place(relx=0.51, rely=0.78, relwidth=0.15, relheight=0.08)
Button(gui, text='取消', borderwidth=3, command=cancel, font='幼圆 -14'\
).place(relx=0.67, rely=0.78, relwidth=0.13, relheight=0.08)

Label(gui, text="-- developed by iclosed  ", \
height=2, width=22, fg="blue").place(relx=0.3, rely=0.9, relwidth=0.7, relheight=0.07)

thread.start_new_thread(threadscan, ())
mainloop()
