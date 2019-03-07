# 导入socket、sys 模块
import socket
import sys
import time
import win32clipboard as w    
import win32con


def getText():#读取剪切板  
    w.OpenClipboard()  
    d = w.GetClipboardData(win32con.CF_TEXT)  
    w.CloseClipboard()  
    return d


# 获取本地主机名
host = '192.168.0.109'

#设置端口号
port = 9999

while True:
	#创建 socket 对象
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 连接服务，指定主机和端口
	s.connect((host, port))

	#接收小于1024字节的数据
	msg = s.recv(1024)

	s.close()

	print(getText())
	
	time.sleep(1)
	