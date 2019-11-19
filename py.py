"""
poll_server.py  完成tcp并发
重点代码

思路分析:   创建监听套接字先进行监控
           产生新的套接字也加入到监控中
"""
from socket import *
from select import *

# 创建监听套接字
s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(3)

# 创建poll对象
p = poll()
p.register(s,POLLIN) # 将s设置关注

# 建立一个查找字典,用于通过文件描述符查找其对应的IO对象
# 跟关注的IO保持一致
fdmap = {s.fileno():s}

# 循环监控IO
while True:
    events = p.poll() # 阻塞等待IO发生
    print(events) # [(fileno,event)]
    for fd,event in events:
        # if结构区分哪个IO就绪 fd->fileno  event->IO类别
        if fd == s.fileno():
            c,addr = fdmap[fd].accept()
            print("Connect from",addr)
            p.register(c,POLLIN|POLLERR) # 关注客户端套接字
            fdmap[c.fileno()] = c  # 将其添加到查找字典
        # 通过按位与判断是否为POLLIN就绪
        elif event & POLLIN:
            data = fdmap[fd].recv(1024).decode()
            if not data:
                p.unregister(fd) # 取消关注
                fdmap[fd].close()
                del fdmap[fd]  # 从字典中移除
                continue
            print(data)
            fdmap[fd].send(b'OK')






