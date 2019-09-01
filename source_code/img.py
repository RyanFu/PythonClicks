# -*- coding:utf-8 -*-
import os
import cv2
import aircv
import numpy
import win32ui
import win32con
import win32gui
from PIL import Image

def draw_circle(imgsrc, positions, circle_radius, color, line_width):
	for pos in positions:
		circle_center_pos = (int(pos[0]), int(pos[1]))
		cv2.circle(imgsrc, circle_center_pos, circle_radius, color, line_width)
	cv2.imshow('show result', imgsrc)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

class ImageProcess:
	def __init__(self, hwnd=0):
		self.load_imgs()
		self.set_handle(hwnd)

	def set_handle(self, hwnd):
		self.hwnd = hwnd

	def load_imgs(self):
		self.imgs = {}
		res_path = 'resources/'
		for file in os.listdir(res_path):
			if file.split('.')[1] != 'png':
				continue
			tag = file.split('.')[0]
			# self.imgs[tag] = cv2.imread(res_path + file)  # 无法处理中文路径
			self.imgs[tag] = cv2.imdecode(numpy.fromfile(res_path + file, dtype=numpy.uint8),-1)

	def screen_shot(self):
		hwndDC = win32gui.GetWindowDC(self.hwnd)
		mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 创建设备描述表
		saveDC = mfcDC.CreateCompatibleDC()  # 创建内存设备描述表

		left, top, right, bott = win32gui.GetWindowRect(self.hwnd)
		width = (right-10) - (left+10)  # 根据具体窗口微调
		height = (bott-10) - (top+30)

		bitMap = win32ui.CreateBitmap()  # 创建位图对象
		bitMap.CreateCompatibleBitmap(mfcDC, width, height)
		saveDC.SelectObject(bitMap)
		saveDC.BitBlt((0, 0), (width, height), mfcDC, (10, 30), win32con.SRCCOPY)
		# bitMap.SaveBitmapFile(self.saveDC, 'screenshot.png')

		bmpinfo = bitMap.GetInfo()  # 获取位图信息
		bmpstr = bitMap.GetBitmapBits(True)
		img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

		# 释放内存
		win32gui.DeleteObject(bitMap.GetHandle())
		saveDC.DeleteDC()
		mfcDC.DeleteDC()
		win32gui.ReleaseDC(self.hwnd, hwndDC)

		return img

	def save_screenshot(self):
		img = self.screen_shot()
		img.save("screenshot.png")

	def find_img(self, part_name, accuracy=0.9):
		if not self.hwnd or win32gui.IsIconic(self.hwnd):  # 窗口不存在或最小化
			return None
		img = self.screen_shot()
		img_mat = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
		match = aircv.find_template(img_mat, self.imgs[part_name])
		if match is None:
			return None
		elif match['confidence'] < accuracy:
			# print(part_name, 'not exact, confidence is: ', match['confidence'])
			return None
		elif match['confidence'] >= accuracy:
			print(part_name + ' is found, accuracy: ', match['confidence'])
			return match['result']

	def find_all_imgs(self, part_name, accuracy=0.9):
		if not self.hwnd or win32gui.IsIconic(self.hwnd):  # 窗口不存在或最小化
			return None
		img = self.screen_shot()
		img_mat = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
		# img_mat = aircv.imread('screenshot.png')
		matches = aircv.find_all_template(img_mat, self.imgs[part_name])
		positions = []
		for match in matches:
			if match['confidence'] < accuracy:
				continue
			positions.append(match['result'])
		# draw_circle(img_mat, positions, 60, (20, 200, 20), 3)

		return positions


if __name__ == '__main__':
	import sys
	import ctypes
	import win32gui

	# if not ctypes.windll.shell32.IsUserAnAdmin():
	# 	"""若没有管理员权限，重新Shell带管理员权限的自身进程，然后Suicide"""
	# 	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
	# 	sys.exit()

	title = '阴阳师-网易游戏'
	hwnd = win32gui.FindWindow(None, title)
	# ##########################################################
	# ## win32gui.MoveWindow(hwnd, 384, 189, 1152, 679, True) ##
	# ##########################################################
	imp = ImageProcess(hwnd)

	matches = imp.find_all_imgs('组队大厅')

	print(matches)

