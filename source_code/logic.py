# -*- coding:utf-8 -*-
import os
import time
import win32gui
import threading
from mouse import Mouse
from img import ImageProcess

SelfFieldBreak_posDICT = {
	0: (388, 100), 1: (700, 100), 2: (1000, 100),
	3: (388, 220), 4: (700, 220), 5: (1000, 220),
	6: (388, 340), 7: (700, 340), 8: (1000, 340),
}

GangFieldBreak_posDICT = {
	0: (12, 12), 1: (12, 12),
	2: (12, 12), 3: (12, 12),
	4: (12, 12), 5: (12, 12),
	6: (12, 12), 7: (12, 12),
}

class logicThread(threading.Thread):
	def __init__(self, signal_Q):
		threading.Thread.__init__(self)
		self.gui_label = None
		self.tkFrame = None
		self.signal_Q = signal_Q
		self.cycle_func = {
			0:self.general,	1:self.team_instance, 2:self.single_adventure,
			3:self.field_break, 4:self.yaoqi, 255:self.pause,
		}
		self.init_vars()
		self.init_modules()


	def init_vars(self):
		self.in_cycle = 255
		self.data = None
		self.state = ''
		self.tick_count = 0
		self.count_max = 0

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
			if not self.hwnd:
				self.hwnd = win32gui.FindWindow(self.window_class, self.title)
			win32gui.MoveWindow(self.hwnd, 150, 100, 1152, 679, True)

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
			self.dynamic_label(['扫描中   ', '扫描中.  ', '扫描中.. ', '扫描中...'])
			self.cycle_func[self.in_cycle]()

	def terminate(self):
		os._exit(0)

	def set_label(self, text):
		if self.tkFrame and not self.tkFrame.if_iconfy:
			self.gui_label['text'] = text

	def dynamic_label(self, text_array):
		self.count_max = len(text_array)
		self.tick_count += 1
		if self.tick_count >= self.count_max:
			self.tick_count = 0
		# print(self.tick_count)
		self.set_label(text_array[self.tick_count])

	def check_hwnd(self):
		if not self.hwnd or win32gui.IsIconic(self.hwnd):
			self.hwnd = win32gui.FindWindow(self.window_class, self.title)
			self.set_label('游戏窗口不存在或被最小化')
			return False
		return True

	def pause(self):
		self.set_label('暂停')

	def general(self):
		for part_img in ['点击屏幕继续', '准备', '接受组队邀请', '接受妖气封印', '确认', '挑战']:
			pos = self.imp.find_img(part_img, 0.75)
			if not pos: continue
			self.mouse.click(pos)
			self.set_label(part_img)
			break

	def team_instance(self):
		if self.imp.find_img('邀请'):
			if self.data['if_full'] == 1:
				return
		for part_img in ['组队选所有人', '开始战斗', '创建']:
			pos = self.imp.find_img(part_img)
			if not pos: continue
			self.mouse.click(pos)
			self.set_label(part_img)
			break

		self.general()

	def single_adventure(self):
		if self.state != 'OutAdventure':
			self.state = 'InAdventure'
		for part_img in ['接受组队邀请', '探索', '准备', '点击屏幕继续', 'boss', '小怪', '宝箱', '第二十八章']:
			pos = self.imp.find_img(part_img)
			if not pos: continue
			self.mouse.click(pos)
			self.set_label(part_img)

			if part_img=='探索':
				self.state = 'InAdventure'
			if part_img=='boss':
				self.state = 'OutAdventure'
			if part_img=='宝箱':
				self.set_label(part_img)
				time.sleep(2)
				self.mouse.click((820, 500))

			return

		if not self.imp.find_img('小怪', 0.8) and self.state=='InAdventure':
			self.set_label('点地板移动...')
			self.mouse.click((820, 500))

	def yaoqi(self):
		for part_img in ['二口女', '鬼使黑', '海坊主', '日和坊', '小松丸', '跳跳哥哥']:
			pos = self.imp.find_img(part_img)
			if not pos: continue
			join_pos = (pos[0]+420, pos[1]+10)
			self.mouse.click(join_pos)
			self.set_label(part_img)
			return

		for part_img in ['刷新', '组队大厅', '准备', '点击屏幕继续', '接受妖气封印', ]:
			pos = self.imp.find_img(part_img)
			if not pos: continue
			if part_img == '组队大厅':
				self.mouse.click(pos)
				time.sleep(1)
				self.mouse.click((576, 350))
				self.state = 'MakeTeam'
				return
			self.mouse.click(pos)
			self.set_label(part_img)
			return

	def field_break(self):
		self.state = 'General'
		if self.imp.find_img('个人防守记录', 0.95):
			self.state = 'SelfFieldBreak'
		if self.imp.find_img('寮突破记录', 0.95):
			self.state = 'GangFieldBreak'

		if self.state == 'SelfFieldBreak':
			if self.imp.find_img('突破失败', 0.98):
				self.mouse.click((930, 480))
				time.sleep(1.5)
				self.mouse.click((675, 380))
				return
			for i in range(0, 9):
				self.mouse.click(SelfFieldBreak_posDICT[i])
				attack_pos = self.imp.find_img('进攻')
				if attack_pos:
					self.mouse.click(attack_pos)
					self.set_label('攻击第'+str(i)+'个结界')
					self.state = 'General'
					break
				time.sleep(0.3)

		if self.state == 'GangFieldBreak':
			for i in range(0, 8):
				self.mouse.click(GangFieldBreak_posDICT[i])
				attack_pos = self.imp.find_img('进攻')
				if attack_pos:
					self.mouse.click(attack_pos)
					self.state = 'General'
					break
				time.sleep(0.3)

		if self.state == 'General':
			self.general()
