from socket import *
import os,sys,signal
'''
聊天室文件
客户端
by:dyh
'''
#发送消息
def do_child(s,name,addr):
	while True:
		text=input("say:")
		if text=='quit':
			msg="q."+name
			s.sendto(msg.encode(),addr)
			#从子进程种杀掉父进程
			os.kill(os.getppid(),signal.SIGKILL)
			sys.exit('已退出！')
		else:
			msg='m.'+'%s.%s'%(name,text)
			s.sendto(msg.encode(),addr)
#收消息		
def do_parent(s):
	while True:
		msg,addr=s.recvfrom(1024)
		msg=msg.decode()
		msg=msg[:-1]
		print(msg+"\nsay:",end='')

def main():
	if len(sys.argv)<3:
		print('argv error,')
		return 
	HOST=sys.argv[1]
	PORT=int(sys.argv[2])
	ADDR=(HOST,PORT)

	#使用数据报套接字
	s=socket(AF_INET,SOCK_DGRAM)

	while True:
		name=input("请输入姓名:")
		msg='l.'+name
		s.sendto(msg.encode(),ADDR)
		data,addr=s.recvfrom(1024)
		if data.decode()=='OK':
			print('###进入聊天室###')
			break
		else:
			print(data.decode())

	pid=os.fork()

	if pid<0:
		print(' ')
	elif pid==0:
		do_child(s,name,ADDR)
	else:
		#等待一级子进程的退出
		do_parent(s)

if __name__=='__main__':
	main()