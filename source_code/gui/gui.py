#coding=utf-8
from Tkinter import *
import thread
import time

master = Tk()
master.title('hello')
master.geometry('200x200')
mode = IntVar()


def scan():
    while(1):
        if mode.get() == 1:
            print '11111'
        elif mode.get() == 2:
            print '22222'
        elif mode.get() == 3:
            print '33333'
        else:
            pass
        time.sleep(1)


def func():
    print(mode.get())


MODES = [
    ('    apple    ', 1),
    ('    banna    ', 2),
    ('     cat     ', 3),
    ('     stop    ', 256)
]
for name, val in MODES:
    Radiobutton(master, text=name, value=val, variable=mode, command=func, indicatoron=0).pack()

thread.start_new_thread(scan,())
mainloop()

