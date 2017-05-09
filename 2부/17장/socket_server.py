# -*- coding:cp949 -*-
import socket

HOST = '' #호스트를 지정하지 않으면 가능한 모든 인터페이스를 의미합니다.
PORT = 50007 #포트를 지정합니다.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1) #접속이 있을 때까지 기다립니다.
conn, addr = s.accept() #접속을 승인합니다.
print('Connected by', addr)
while True:
    data = conn.recv(1024)
    if not data: break
    conn.send(data) #받은 데이터를 그대로 클라이언트에 전송합니다.
conn.close()