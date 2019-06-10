# -*- coding:utf-8 -*-
import sys
import time
import queue
import ctypes
import tkinter
from gui import MainGUI
from logic import logicThread


if not ctypes.windll.shell32.IsUserAnAdmin():
	"""若没有管理员权限，重新Shell带管理员权限的自身进程，然后Suicide"""
	time.sleep(0.2)  # little lag in case of unexpected error
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
	sys.exit()

"""信号队列，用于GUI线程和逻辑线程之间通信"""
signal_Q = queue.Queue()

"""GUI主线程，mainloop()之后阻塞"""
mainFrame = tkinter.Tk()
GUI = MainGUI(mainFrame, signal_Q)

"""逻辑线程，处理具体运行时逻辑"""
thread1 = logicThread(signal_Q)
thread1.gui_label = GUI.lab
thread1.tkFrame = mainFrame
thread1.start()

mainFrame.mainloop()
thread1.terminate()
# end
