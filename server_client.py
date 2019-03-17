import socket
import win32clipboard as cb
import win32con as con
import time
import _thread

dict = {'time': time.time(), 'text': ''}

def setText(data):#写入剪切板
    cb.OpenClipboard()
    cb.EmptyClipboard()
    cb.SetClipboardText(data, con.CF_UNICODETEXT)
    cb.CloseClipboard()
    
def getText():#读取剪切板
    clipboarddata = ""
    cb.OpenClipboard()
    x = cb.CountClipboardFormats()
    if x == con.CF_UNICODETEXT:
        clipboarddata = cb.GetClipboardData(con.CF_UNICODETEXT)
    elif x == con.CF_OEMTEXT:
        clipboarddata = cb.GetClipboardData(con.CF_OEMTEXT)
    elif x == con.CF_TEXT:
        clipboarddata = cb.GetClipboardData(con.CF_TEXT)
    cb.CloseClipboard()
    return clipboarddata
    
def serverRun(host, port):
    BUF_SIZE = 1024
    global dict
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(200)#接收的连接数
    
    while True:#循环收发数据包，长连接
        client, address = server.accept()#因为设置了接收连接数为1，所以不需要放在循环中接收
        data = client.recv(BUF_SIZE)
        client.close()
        text = data.decode('UTF-8', 'strict')
        print("recv data %s from %s:" % (text, address))
        if text.strip() != '':
            new_dict = eval(text)
            if new_dict['time'] > dict['time'] and new_dict['text'] != dict['text']:
                dict = new_dict
                setText(new_dict['text'])
    
#client 是发送方，短连接，一次完整的传输过程，发送方 输出流 发送完 并 关闭
def clientRun(serverhost, serverport):
    global dict
    
    while True:
        time.sleep(1) #如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点
        text = getText()
        print("in while true, %s" % text)
        now = time.time()
        print ("text:%s, now:%f" % (text, now))
        print ("dict[text]:%s, dict[time]:%f" % (dict['text'], dict['time']))
        
        if (text.strip() != '' and dict['text'] != text and now > dict['time']):
            print("in if")
            dict['text'] = text
            dict['time'] = now
            strdict = str(dict)
            print("before socket.socket")
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((serverhost, serverport))
                print("after client connect")
                client.send(strdict.encode("UTF-8"))
                print("after client.send")
                client.close()
                print('send data %s to %s' % (strdict, serverhost) )
            except:
                print("can't connect server")
                continue
        
        
    
# 创建两个线程
try:
   _thread.start_new_thread( serverRun, ("192.168.0.109", 9999) )
   print("server is activated")
   _thread.start_new_thread( clientRun, ("192.168.0.107", 9998) )
   print("client is activated")
except:
   print ("Error: 无法启动线程")

while 1:
   pass


