from socket import socket

a=input('请输入ip：')
b=input('请输入端口：')
s=socket()
a=str(a)
b=int(b)
s.connect((a,b))
c=s.recv(102400000)
print(c)