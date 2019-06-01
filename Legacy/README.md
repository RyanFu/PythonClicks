# PythonClicks
基于Python而写的一个自动点击脚本

---

## 使用手册
### 0x00 窗口获取和鼠标控制
依赖库：
* win32api
* win32con
* win32gui
* ctpyes 

调试source_code/win32api/下的*mouseCtrl.py*和*getHandle.py*使之可以正常运行
*注：点击事件需要管理员权限*

### 0x01 图像处理
依赖库：
* cv2
* aircv
* ImageGrab
* numpy 

调试source_code/img_process/下的*img_find_aircv.py*使之可以正常运行

### 0x02 具体实现
结合前三段程序可以轻松的进行游戏中图像的查询和点击，具体一个实现例子见 *onmyoji/_run.py*

### 0x03 关于管理员权限
由于win10对安全做了很多改进，所以需要先进行管理员权限获取：

	%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

这行代码用于打开一个管理员权限的shell，可以在后面继续添加执行代码。

更新的方法：在程序中添加代码获取管理员权限:
    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

参考 source_code/getadmin.py

### 0x04 打包成exe执行
安装pyinstaller

>>pyinstaller.exe (-options) ***.py

	-options
	
	-F 打包成一个文件（运行速度略慢）
	-w 不弹出控制台
	-i 图标

有了这个打包没有装过python环境的机器也能跑啦

### 0x05 GUI开发
*from Tkinter import *

使用Tkinter开发图形界面

简单的示例：

	# -*- coding: UTF-8 -*-

	from Tkinter import *           # 导入 Tkinter 库
	root = Tk()                     # 创建窗口对象的背景色
									# 创建两个列表
	li     = ['C','python','php','html','SQL','java']
	movie  = ['CSS','jQuery','Bootstrap']
	listb  = Listbox(root)          #  创建两个列表组件
	listb2 = Listbox(root)
	for item in li:                 # 第一个小部件插入数据
		listb.insert(0,item)

	for item in movie:              # 第二个小部件插入数据
		listb2.insert(0,item)

	listb.pack()                    # 将小部件放置到主窗口中
	listb2.pack()
	root.mainloop()                 # 进入消息循环

本项目使用Radiobutton切换脚本状态

在开发GUI的过程中又遇到了一个问题，就是GUi绘制完成后需要进入mainloop循环，

用于使GUI能够与用户交互，这样的话，本来代码中的循环就不能实现了。

开始打算用中断或者轮询来解决，但是没查到太多资料，吃饭的时候想了一下可以用多线程解决

### 0x06 Python多线程
这里也只简单的放一个示例代码：

	# -*- coding: UTF-8 -*-
	 
	import thread
	import time
	 
	# 为线程定义一个函数
	def print_time( threadName, delay):
	   count = 0
	   while count < 5:
		  time.sleep(delay)
		  count += 1
		  print "%s: %s" % ( threadName, time.ctime(time.time()) )
	 
	# 创建两个线程
	try:
	   thread.start_new_thread( print_time, ("Thread-1", 2, ) )
	   thread.start_new_thread( print_time, ("Thread-2", 4, ) )
	except:
	   print "Error: unable to start thread"
	 
	while 1:
	   pass
	
简单易懂，Python就是这么好用！

### 0x07 项目结束
这个脚本写的短短续续，之前开发到能自己用就没管了。后来想好东西要分享，就加上了后半段的开发，

并将逻辑重新理了一下，是脚本更加易读。
