# -*- coding:utf-8 -*-
import os
import re
import tkinter
from SysTrayIcon import SysTrayIcon
from tooltip import CreateToolTip
from tkinter import ttk, Button, Radiobutton, Label, Checkbutton, Entry


class MainGUI(ttk.Frame):
	def __init__(self, parent, signal_Q=None):
		self.root = parent
		self.signal_Q = signal_Q

		# self.root.bind("<Unmap>", lambda event: self.minimize() if self.root.state() == 'iconic' else False)
		self.register_functions()
		self.init_vars()
		self.init_gui()
		self.init_layout()
		self.init_tooltips()

	def init_vars(self):
		self.title = '痒痒鼠'
		self.resizable = False
		self.size = '255x333'
		self.icon = 'resources/ssr.ico'
		self.hover = 'I\'m hiding here'
		self.mode = tkinter.IntVar(value=255)
		self.if_full = tkinter.IntVar(value=1)
		self.mob = tkinter.StringVar()
		self.shut_var = tkinter.StringVar()

	def resize(self):
		signal = {
			'type': 'Resize'
		}
		self.signal_Q.put(signal)

	def multi_open(self):
		signal = {
			'type': 'MultiOpen'
		}
		self.signal_Q.put(signal)

	def minimize(self):
		self.root.withdraw()
		self.root.if_iconfy = True
		self.sysTrayIcon.show_icon()

	def change_mode(self, *args):
		signal = {
			'type': 'ChangeMode',
			'mode': self.mode.get(),
			'if_full': self.if_full.get(),
			'mob': self.mob.get(),
		}
		self.signal_Q.put(signal)

	def change_fullteam(self):
		self.full_chk['text'] = '等满员' if self.if_full.get()==1 else '不等满员'
		self.change_mode()

	def shutdown(self, *args):
		if self.shut_var.get() == '':
			self.shut_var.set('5')
		self.shut_time['state'] = 'disable'
		self.shut_btn['state'] = 'disable'
		signal = {
			'type': 'ShutDown',
			'shut_time': self.shut_time.get(),
		}
		# print(signal)
		self.signal_Q.put(signal)

	def cancel_shut(self):
		self.shut_time['state'] = 'normal'
		self.shut_btn['state'] = 'normal'
		self.shut_time.selection_range(0, 9)
		signal = {
			'type': 'CancelShut',
		}
		self.signal_Q.put(signal)

	def init_gui(self):
		self.root.title(self.title)
		self.root.geometry(self.size)
		if not self.resizable: self.root.resizable(0, 0)
		if os.path.isfile(self.icon): self.root.iconbitmap(self.icon)

		self.sysTrayIcon = SysTrayIcon(self.icon, self.hover, on_quit=lambda: self.root.destroy(), gui=self.root)

		self.lab = Label(self.root, text="初始化...", font='幼圆 -16', fg="brown")

		self.resize_btn = Button(self.root, text='还原分辨率', bg='#c0d6e4', command=self.resize, font='幼圆 -14')

		self.multi_btn = Button(self.root, text='多开初始化', bg='#c0d6e4', command=self.multi_open, font='幼圆 -14')

		self.hide_btn = Button(self.root, text='隐藏至托盘', bg='#c0d6e4', command=self.minimize, font='幼圆 -14')

		self.radio_0 = Radiobutton(self.root, text='通用(哪里要点点哪里)', value=0, variable=self.mode, borderwidth=4,
			indicatoron=0, command=self.change_mode, font='幼圆 -14', bg='#cccccc', selectcolor='#87e7bb')

		self.radio_1 = Radiobutton(self.root, text='组队刷本', value=1, variable=self.mode, borderwidth=4,
			indicatoron=0, command=self.change_mode, font='幼圆 -14', bg='#cccccc', selectcolor='#87e7bb')

		self.radio_2 = Radiobutton(self.root, text='单刷_探索', value=2, variable=self.mode, borderwidth=4,
			indicatoron=0, command=self.change_mode, font='幼圆 -14', bg='#cccccc', selectcolor='#87e7bb')

		self.radio_3 = Radiobutton(self.root, text='结界突破', value=3, variable=self.mode, borderwidth=4, #state = 'disabled',
			indicatoron=0, command=self.change_mode, font='幼圆 -14', bg='#cccccc', selectcolor='#87e7bb')

		self.radio_4 = Radiobutton(self.root, text='妖气封印', value=4, variable=self.mode, borderwidth=4,
			indicatoron=0, command=self.change_mode, font='幼圆 -14', bg='#cccccc', selectcolor='#87e7bb')

		self.radio_255 = Radiobutton(self.root, text='[暂停]', value=255, variable=self.mode, borderwidth=5,
			indicatoron=0, command=self.change_mode, font='幼圆 -16', bg='#cccccc', selectcolor='#e6b8af')

		self.full_chk = Checkbutton(self.root, text='等满员', variable=self.if_full, borderwidth=2,
			indicatoron=0, command=self.change_fullteam, font='幼圆 -13', bg='#c0d6e4', selectcolor='#ccd7ff')

		self.mob_list = ttk.Combobox(self.root, textvariable=self.mob, font='幼圆 -13')
		self.mob_list["values"] = ('日和坊','海坊主', '鬼使黑', '跳跳哥哥', '小松丸', '二口女', '以上全部')
		self.mob_list.bind("<<ComboboxSelected>>", self.change_mode)
		self.mob_list["state"] = "readonly"
		self.mob_list.current(0)

		self.shut_time = Entry(self.root, textvariable=self.shut_var, validate='key', vcmd=(self.register_func[0],'%P'))
		self.shut_time.bind('<Return>', self.shutdown)

		self.shut_label = Label(self.root, text="分钟后", font='幼圆 -14')

		self.shut_btn = Button(self.root, text='关机', borderwidth=3, bg='#fdc9d9', command=self.shutdown, font='幼圆 -14')
		self.cacel_btn = Button(self.root, text='取消', borderwidth=3, bg='#cccccc', command=self.cancel_shut, font='幼圆 -14')

		self.author = Label(self.root, text="-- developed by iclosed  ", height=2, width=22, fg="blue")

	def init_layout(self):
		self.lab.place(relx=0.15, rely=0.07, relwidth=0.75, relheight=0.1)
		self.resize_btn.place(relx=0.01, rely=0.01, relwidth=0.30, relheight=0.07)
		self.multi_btn.place(relx=0.35, rely=0.01, relwidth=0.30, relheight=0.07)
		self.hide_btn.place(relx=0.69, rely=0.01, relwidth=0.30, relheight=0.07)
		self.radio_0.place(relx=0.2, rely=0.18, relwidth=0.6, relheight=0.1)
		self.radio_1.place(relx=0.2, rely=0.3, relwidth=0.38, relheight=0.1)
		self.full_chk.place(relx=0.58, rely=0.3, relwidth=0.22, relheight=0.1)
		self.radio_2.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.1)
		self.radio_3.place(relx=0.2, rely=0.5, relwidth=0.6, relheight=0.1)
		self.mob_list.place(relx=0.2, rely=0.6, relwidth=0.31, relheight=0.1)
		self.radio_4.place(relx=0.51, rely=0.6, relwidth=0.29, relheight=0.1)
		self.radio_255.place(relx=0.2, rely=0.71, relwidth=0.6, relheight=0.1)
		self.shut_time.place(relx=0.2, rely=0.83, relwidth=0.12, relheight=0.08)
		self.shut_label.place(relx=0.33, rely=0.83, relwidth=0.16, relheight=0.08)
		self.shut_btn.place(relx=0.51, rely=0.83, relwidth=0.15, relheight=0.08)
		self.cacel_btn.place(relx=0.66, rely=0.83, relwidth=0.14, relheight=0.08)
		self.author.place(relx=0.35, rely=0.93, relwidth=0.7, relheight=0.07)

	def register_functions(self):
		self.register_func = []
		self.register_func.append(self.root.register(self.input_check_0))

	def input_check_0(self, content):
		"""Make sure input number is 1~999"""
		pattern = r"[1-9]\d{0,2}$"
		if re.match(pattern, content) or len(content)==0:
			return True
		else:
			return False

	def init_tooltips(self):
		CreateToolTip(self.resize_btn, '改变了游戏窗口默认大小时使用，否则无法正确识别图片。')
		CreateToolTip(self.multi_btn, '如果启动脚本之后打开了新的游戏窗口请点击这个按钮。')
		CreateToolTip(self.hide_btn, '将脚本界面最小化到系统托盘。')

if __name__ == '__main__':
	import queue
	test_queue = queue.Queue()

	mainFrame = tkinter.Tk()
	MainGUI(mainFrame, test_queue)
	mainFrame.mainloop()





