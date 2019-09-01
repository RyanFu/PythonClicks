# -*- coding:utf-8 -*-
from mouse import Mouse
from img import ImageProcess


class Window:
	def __init__(self, hwnd):
		self.hwnd = hwnd
		self.mouse = Mouse(hwnd)
		self.imp = ImageProcess(hwnd)

	def click(self, pos):
		self.mouse.click(pos)

	def find_img(self, img_name, accuracy=0.9):
		return self.imp.find_img(img_name, accuracy)

	def find_all_imgs(self, img_name, accuracy=0.9):
		return self.imp.find_all_imgs(img_name, accuracy)



if __name__ == '__main__':
	import sys
	import time
	import ctypes
	import win32gui

	if not ctypes.windll.shell32.IsUserAnAdmin():
		"""若没有管理员权限，重新Shell带管理员权限的自身进程，然后Suicide"""
		time.sleep(0.2)  # little lag in case of unexpected error
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
		sys.exit()

	title = '阴阳师-网易游戏'
	hwnd = win32gui.FindWindow(None, title)

	window = Window(hwnd)
	matches = window.find_all_imgs('组队大厅')
	print(matches)
	window.click((230.0, 579.5))

