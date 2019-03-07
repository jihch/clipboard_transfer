import socket
import win32clipboard as w
import win32con

def setText(data):#写入剪切板  
    w.OpenClipboard()  
    w.EmptyClipboard()  
    w.SetClipboardText(data, win32con.CF_UNICODETEXT)
    w.CloseClipboard()

BUF_SIZE = 1024

host = '192.168.0.109'

port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))

server.listen(1) #接收的连接数

client, address = server.accept() #因为设置了接收连接数为1，所以不需要放在循环中接收

while True: #循环收发数据包，长连接
    data = client.recv(BUF_SIZE)
    print(type(data))
    setText(data.decode('UTF-8','strict'))
    