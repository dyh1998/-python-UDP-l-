from socket import *
import os,sys
'''
聊天室文件
服务端
by:dyh
'''
###用户退出并且告知所有的用户###
def do_logout(s,user,name):
	#删除列表中的用户
	del user[name]
	msg='\n'+name+'离开了聊天室'
	for i in user:
		s.sendto(msg.encode(),addr)
	return
def do_login(s,user,name,addr):
	#用户注册时对用户name进行检查
	if (name in user) or name=='管理员':
		s.sendto('该用户已存在'.encode(),addr)
		return 
	#用户name符合要求时发送OK给客户端提示其可以正常登陆
	#用户接收到信息以后对信息判断进行登陆操作
	s.sendto(b'OK',addr)
	msg='\n欢迎%s进入聊天室'%name
	#通知所有人
	for i in user:
		s.sendto(msg.encode(),user[i])
	#将用户插进字典
	user[name]=addr
	return

def do_chat(s,user,cmd):
	msg='\n%-4s:%s'%(cmd[1],' '.join(cmd[2:]))
	#将用户name发送给除了自己之外的所有人
	for i in user:
		if i!=cmd[1]:
			s.sendto(msg.encode(),user[i])
	return

#处理客户端请求
def do_child(s):
	#字典存储用户信息
	user={}
	#循环接收请求
	while True:
		msg,addr=s.recvfrom(1024)
		msg=msg.decode()
		cmd=msg.split('.')
		#根据不同请求做不同的事情
		if cmd[0]=='l':
			do_login(s,user,cmd[1],addr)
			s.sendto(b'OK',addr)
		elif cmd[0]=='m':
			do_chat(s,user,cmd)
		elif cmd[0]=='q':
			do_logout()
		else:
			s.sendto('请求错误'.encode(),addr)


#发送管理员消息
def do_parent(s,ADDR):
	while True:
		msg=input('管理员发消息：')
		msg='m.管理员:'+msg
		s.sendto(msg.encode(),ADDR)
	s.close()
	sys.exit(0)

def main():
	if len(sys.argv)<3:
		print('argv error,')
		return 
	HOST=sys.argv[1]
	PORT=int(sys.argv[2])
	ADDR=(HOST,PORT)

	#使用数据b报套接字
	s=socket(AF_INET,SOCK_DGRAM)
	#设置端口重用代码
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	s.bind(ADDR)

	#创建一级子进程
	pid1=os.fork()

	if pid1<0:
		print()
	elif pid1==0:
		print('child process')
		pid2=os.fork()
		if pid2<0:
			print("")
		elif pid2==0:
			do_child(s)
		else:
			#一级子进程退出，使二级子进程成为孤儿
			os._exit(0)
	else:
		#等待一级子进程的退出
		os.wait()
		do_parent(s,ADDR)

if __name__=='__main__':
	main()
