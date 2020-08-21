"""
dict 服务端

* 接收客户端请求
* 进行请求处理
* 向客户端发送结果
"""

from socket import *
from multiprocessing import Process
import signal,sys
from dict_db import *
from time import sleep

HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

# 提前建立数据链接
db = Database()

# 处理注册信息
def do_register(connfd,name,passwd):
    if db.register(name,passwd):
        connfd.send(b"YES")
    else:
        connfd.send(b"NO")

# 处理登录信息
def do_login(connfd,name,passwd):
    if db.login(name,passwd):
        connfd.send(b"YES")
    else:
        connfd.send(b"NO")

# 处理查询单词
def do_query(connfd,name,word):
    # 插入历史记录
    db.insert_history(name,word)

    # 查询单词得到解释
    mean = db.query(word) # 查到了--> xxxx  或者 None
    if mean:
        data = "%s : %s"%(word,mean)
        connfd.send(data.encode())
    else:
        connfd.send("没有该单词".encode())

# 历史记录查询
def do_history(connfd,name):
    # data-># ((name,word,time),(name,word,time),(name,word,time))
    data = db.history(name)
    for i in data:
        # i ---> (name,word,time)
        msg = "%s      %s       %s"%i
        connfd.send(msg.encode())  #发送历史记录
        sleep(0.1) # 粘包处理
    connfd.send(b'##')

# 具体处理客户端请求
def handle(connfd):
    db.cursor() # 每个子进程独立有自己的游标
    # 总分模式 --> 一个地方负责接收请求,根据请求进行任务分发
    while True:
        data = connfd.recv(1024).decode()
        tmp = data.split(' ')
        if not data or tmp[0] == "E":
            connfd.close()
            db.cur.close()
            return
        elif tmp[0] == 'R':
            # tmp --> [R name passwd]
            do_register(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'L':
            # tmp --> [L name passwd]
            do_login(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'Q':
            # tmp --> [Q name word]
            do_query(connfd,tmp[1],tmp[2])
        elif tmp[0] == 'H':
            # tmp --> [H name]
            do_history(connfd,tmp[1])

# 搭建基本网络结构模型,启动服务
def main():
    #  创建TCP套接字
    sockfd = socket()
    sockfd.bind(ADDR)
    sockfd.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 循环等待客户端链接
    print("Listen the port %d"%PORT)
    while True:
        try:
            c,addr = sockfd.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sockfd.close()
            db.close()
            sys.exit("服务端退出")

        # 为客户端创建子进程
        p = Process(target=handle,args=(c,))
        p.daemon = True
        p.start()

if __name__ == '__main__':
    main()   # 启动程序