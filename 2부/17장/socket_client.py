# -*- coding:cp949 -*-
import socket

HOST = '127.0.0.1' #localhost
PORT = 50007 #서버와 같은 포트를 사용합니다.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓 생성
s.connect((HOST, PORT))
s.send(b'Hello, python') #문자를 보냅니다.
data = s.recv(1024) #서버로부터 정보를 받습니다.
s.close()
print('Received', repr(data))