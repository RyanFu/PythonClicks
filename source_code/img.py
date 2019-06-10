import os
import cv2
import aircv
import numpy
import win32ui
import win32con
import win32gui
from PIL import Image


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
			self.imgs[tag] = cv2.imread(res_path + file)

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

	def find_img(self, part_name, accuracy=0.8):
		if not self.hwnd or win32gui.IsIconic(self.hwnd):  # 窗口不存在或最小化
			return None
		img = self.screen_shot()
		if not img:
			return None
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
	# print(imp.find_img('hall2team'))

