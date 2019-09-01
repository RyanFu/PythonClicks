import time
import win32api
import win32con


class Mouse:
	def __init__(self, hwnd=0):
		self.set_handle(hwnd)
		self.act = {
			'left_down': win32con.WM_LBUTTONDOWN,
			'left_up': win32con.WM_LBUTTONUP,
		}

	def set_handle(self, hwnd):
		self.hwnd = hwnd

	def warp_pos(self, pos):
		x = pos[0]
		y = pos[1]
		return win32api.MAKELONG(int(x), int(y))

	def click(self, pos):
		if not isinstance(pos, tuple) or len(pos)!=2: return  # make sure pos is (x, y)

		win32api.PostMessage(self.hwnd, self.act['left_down'], 0, self.warp_pos(pos))
		time.sleep(0.1)
		win32api.PostMessage(self.hwnd, self.act['left_up'], 0, self.warp_pos(pos))


if __name__ == '__main__':
	import sys
	import ctypes
	import win32gui

	if not ctypes.windll.shell32.IsUserAnAdmin():
		"""若没有管理员权限，重新Shell带管理员权限的自身进程，然后Suicide"""
		time.sleep(0.2)  # little lag in case of unexpected error
		ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
		sys.exit()

	title = '阴阳师-网易游戏'
	hwnd = win32gui.FindWindow(None, title)
	print(win32gui.IsIconic(hwnd))

	mouse = Mouse(hwnd)
	mouse.click((230.0, 579.5))
