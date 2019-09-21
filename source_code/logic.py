# -*- coding:utf-8 -*-
import os
import time
import win32gui
import threading
from mouse import Mouse
from img import ImageProcess
from window import Window

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

def hwnd_callback(hwnd, list):
    # classname = win32gui.GetClassName(hwnd)
    window_text = win32gui.GetWindowText(hwnd)
    if window_text == '阴阳师-网易游戏':
        list.append(hwnd)


class logicThread(threading.Thread):
	def __init__(self, signal_Q):
		threading.Thread.__init__(self)
		self.gui_label = None
		self.tkFrame = None
		self.windows = []
		self.signal_Q = signal_Q
		self.cycle_func = {
			0:self.general,	1:self.team_instance, 2:self.single_adventure,
			3:self.field_break, 4:self.yaoqi, 255:self.pause,
		}
		self.init_vars()
		self.init_windows()

	def init_vars(self):
		self.sleep_rate = 0.5
		self.in_cycle = 255
		self.data = None
		self.state = ''
		self.tick_count = 0
		self.count_max = 0

	def init_windows(self):
		hwnds = []
		self.windows = []
		win32gui.EnumWindows(hwnd_callback, hwnds)
		for hwnd in hwnds:
			self.windows.append(Window(hwnd))
		# print(self.windows)
		self.set_label('多窗口初始化成功')

	def deal_with_signal(self, signal):
		# print(signal)
		if signal['type'] == 'ChangeMode':
			self.in_cycle = signal['mode']
			self.data = signal

		if signal['type'] == 'ShutDown':
			shut_time = int(signal['shut_time'])
			sec = shut_time*60
			popen_cmd = 'shutdown -s -t ' + str(sec)
			os.popen(popen_cmd)

		if signal['type'] == 'CancelShut':
			os.popen('shutdown -a')

		if signal['type'] == 'MultiOpen':
			self.init_windows()

		if signal['type'] == 'Resize':
			for win in self.windows:
				win32gui.MoveWindow(win.hwnd, 150, 100, 1152, 679, True)


	def run(self):  # 线程启动函数
		while(True):
			while(not self.signal_Q.empty()):
				# 监听信号队列:
				self.deal_with_signal(self.signal_Q.get())

			# tick频率平衡性能:
			time.sleep(self.sleep_rate)

			# if not self.check_hwnd():
				# continue

			# 当前循环函数选择:
			self.dynamic_label(['扫描中   ', '扫描中.  ', '扫描中.. ', '扫描中...'])
			for win in self.windows:
				self.cycle_func[self.in_cycle](win)

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

	# def check_hwnd(self):
	# 	if not self.hwnd or win32gui.IsIconic(self.hwnd):
	# 		self.hwnd = win32gui.FindWindow(self.window_class, self.title)
	# 		self.set_label('游戏窗口不存在或被最小化')
	# 		return False
	# 	return True


	# ---------------------------------主逻辑循环函数------------------------------------------
	def pause(self, *args):
		self.set_label('暂停')

	def general(self, win):
		for part_img in ['点击屏幕继续', '准备', '接受组队邀请', '接受妖气封印', '确认', '挑战', '活动单人']:
			pos = win.find_img(part_img, 0.8)
			if not pos: continue
			win.click(pos)
			self.set_label(part_img)
			break

	def team_instance(self, win):
		# invites = win.find_all_imgs('邀请')
		# if len(invites) == 2:
		# 	return
		# if len(invites)==1 and self.data['if_full']==1:
		# 	return
		for part_img in ['组队挑战']:
			pos = win.find_img(part_img)
			if not pos: continue
			win.click(pos)
			self.set_label(part_img)
			break

		self.general(win)

	def single_adventure(self, win):
		if self.state != 'OutAdventure':
			self.state = 'InAdventure'
		for part_img in ['接受组队邀请', '探索', '准备', '点击屏幕继续', 'boss', '小怪', '宝箱', '第二十八章']:
			pos = win.find_img(part_img)
			if not pos: continue
			win.click(pos)
			self.set_label(part_img)

			if part_img=='探索':
				self.state = 'InAdventure'
			if part_img=='boss':
				self.state = 'OutAdventure'
			if part_img=='宝箱':
				self.set_label(part_img)
				time.sleep(2)
				win.click((820, 500))

			return

		if not win.find_img('小怪', 0.8) and self.state=='InAdventure':
			self.set_label('点地板移动...')
			win.click((820, 500))

	def yaoqi(self, win):
		for part_img in ['二口女', '鬼使黑', '海坊主', '日和坊', '小松丸', '跳跳哥哥']:
			pos = win.find_img(part_img)
			if not pos: continue
			join_pos = (pos[0]+420, pos[1]+10)
			win.click(join_pos)
			self.set_label(part_img)
			return

		for part_img in ['准备', '点击屏幕继续', '接受妖气封印', '组队大厅', '刷新', '开始战斗', '加入']:
			pos = win.find_img(part_img)
			if not pos: continue
			win.click(pos)
			self.set_label(part_img)
			return


	def field_break(self, win):
		if win.find_img('个人防守记录', 0.95):
			if win.find_img('突破失败', 0.8):
				self.set_label('突破失败')
				win.click((930, 480))
				time.sleep(1.5)
				win.click((675, 380))
				return
			for i in range(0, 9):
				self.set_label('点击第'+str(i)+'个结界')
				win.click(SelfFieldBreak_posDICT[i])
				time.sleep(0.56)
				attack_pos = win.find_img('进攻')
				if attack_pos:
					win.click(attack_pos)
					self.set_label('攻击第'+str(i)+'个结界')
					break

		elif win.find_img('寮突破记录', 0.95):
			for i in range(0, 8):
				win.click(GangFieldBreak_posDICT[i])
				attack_pos = win.find_img('进攻')
				if attack_pos:
					win.click(attack_pos)
					break
				time.sleep(0.3)

		else:
			self.general(win)
