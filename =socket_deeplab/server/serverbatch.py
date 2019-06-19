# -*- coding: utf-8 -*-

import socket
import time
import sys
# sys.path.insert(0,"/home/swf/swfcode/gan/pytorch-CycleGAN-and-pix2pix-master/")
from inference_softmax import create_model, batch_inference

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#IPV4,TCP协议
#sock.bind(('219.224.168.43',54377))#绑定ip和端口，bind接受的是一个元组
sock.bind(('0.0.0.0',54377))#绑定ip和端口，bind接受的是一个元组
sock.listen(5)#设置监听，其值阻塞队列长度，一共可以有5+1个客户端和服务器连接
a=[x for x in range(40960,41160)]
# a1 = str(a)
print("start server")
opt, model = create_model()
# model.input("")
# model.test()
while True:
    # a=[x + 1 for x in a]
    # s=str(a)#将数据转化为String
    connection, address = sock.accept()#等待客户请求
    print("client ip is:",address)#打印客户端地址
    buf = connection.recv(40960)#接收数据,并存入buf
    save_path = batch_inference(model, opt, (buf).decode("utf-8"))
    print (save_path)
    # print buf
    connection.sendall(bytes(save_path.encode('utf-8')))
    # print(s)
    connection.close()#关闭连接
    time.sleep(1)
sock.close()#关闭服务器
