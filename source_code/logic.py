# -*- coding:utf-8 -*-
import os
import time
import win32gui
import threading
from mouse import Mouse
from img import ImageProcess

class logicThread(threading.Thread):
	def __init__(self, GUI, signal_Q):
		threading.Thread.__init__(self)
		self.label = GUI.lab
		self.signal_Q = signal_Q
		self.data = None
		self.state = True
		self.in_cycle = 255
		self.cycle_func = {
			0:self.general_assist,	1:self.team_instance, 2:self.single_adventure,
			3:self.pause, 4:self.yaoqi, 5:self.pause, 255:self.pause,
		}
		self.init_modules()

	def init_modules(self):
		self.window_class = None  # set None if you don't know exact
		self.window_class = 'Win32Window0'
		self.title = '阴阳师-网易游戏'
		self.hwnd = win32gui.FindWindow(self.window_class, self.title)
		self.mouse = Mouse(self.hwnd)
		self.imp = ImageProcess(self.hwnd)

	def deal_with_signal(self, signal):
		# print(signal)
		if signal['type'] == 'ChangeMode':
			self.in_cycle = signal['mode']
			self.data = signal

		if signal['type'] == 'ShutDown':
			os.popen('shutdown -s -t 7200')

		if signal['type'] == 'CancelShut':
			os.popen('shutdown -a')

		if signal['type'] == 'Resize':
			win32gui.MoveWindow(self.hwnd, 384, 189, 1152, 679, True)

	def run(self):  # 线程启动函数
		while(True):
			while(not self.signal_Q.empty()):
				# 监听信号队列:
				self.deal_with_signal(self.signal_Q.get())

			# tick频率平衡性能:
			time.sleep(0.5)

			if not self.check_hwnd():
				continue

			# 当前循环函数选择:
			self.cycle_func[self.in_cycle]()

	def terminate(self):
		os._exit(0)

	def check_hwnd(self):
		if not self.hwnd or win32gui.IsIconic(self.hwnd):
			return False
		return True

	def pause(self):
		pass

	def general_assist(self):
		for part_img in ['accept', 'attack', 'prepare', 'continue', 'challenge']:
			self.mouse.click(self.imp.find_img(part_img, 0.75))

	def team_instance(self):
		if self.imp.find_img('invite'):
			if self.data['if_full'] == 1:
				return
		for part_img in ['accept', 'all', 'begin', 'prepare', 'continue', 'tick', 'confirm', 'create']:
			pos = self.imp.find_img(part_img)
			if not pos: continue
			self.mouse.click(pos)
			return

	def single_adventure(self):
		for part_img in ['accept', 'adventure', 'prepare', 'continue', 'boss', 'kill', 'chest', 'hard28']:
			pos = self.imp.find_img(part_img)
			if not pos: continue

			self.mouse.click(pos)
			if part_img=='adventure':
				self.state = True
				print(self.state)
			if part_img=='boss':
				self.state = False
				print(self.state)
			if part_img=='chest':
				time.sleep(2)
				self.mouse.click((820, 500))

			return

		if not self.imp.find_img('kill', 0.8) and self.state:
			self.mouse.click((820, 500))

	def yaoqi(self):
		for part_img in ['erkou', 'guishi', 'haifang', 'rihe', 'songwan', 'tiaotiao']:
			pos = self.imp.find_img(part_img)
			if not pos: continue

			join_pos = (pos[0]+420, pos[1]+10)
			self.mouse.click(join_pos)
			return

		for part_img in ['refresh', 'hall2team', 'prepare', 'continue', 'tick', ]:
			pos = self.imp.find_img(part_img)
			if not pos: continue

			if part_img == 'hall2team':
				self.mouse.click(pos)
				time.sleep(1)
				self.mouse.click((576, 350))
				self.state = 'MakeTeam'
				return

			self.mouse.click(pos)
			return