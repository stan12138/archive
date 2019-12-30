"""
再次尝试重新设计Filer的服务器
author: stan
date: 2019.12.27 17:20
"""
import socket
import time
import sys
import selectors

import signal

import threading

import lib


"""
client的这种设计有问题？ 为什么没有及时触发接收事件, 好像就是因为WRITE事件，去掉就好了
"""

class Client :

    def __init__(self, ip, port) :

        self._addr = (ip, port)
        self._client = self.__generate_client()

        self.__selector = selectors.DefaultSelector()

        events = selectors.EVENT_READ #| selectors.EVENT_WRITE
        self.messenger = lib.Messenger(self.__selector, self._client, self._addr)
        self.__selector.register(self._client, events, data=self.messenger)

        self._lock = threading.Lock()

        signal.signal(signal.SIGINT, self.__interrupt_handler)

    def __interrupt_handler(self, sig, frame): 
        """
        捕捉到ctr-c
        定义处理方式为关闭所有socket
        private
        """
        print("get stop signal......")

        self.__selector.unregister(self._client)
        self._client.close()

        print("close work done, bye~~~")
        sys.exit(0)

    def __generate_client(self) :
        """
        生成，配置一个TCP客户端
        private
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(self._addr)

        return sock

    def _listen(self) :
        """
        持续监听
        外部可以调用
        不要override
        """
        while True: 
            events = self.__selector.select(timeout=1)

            for key, mask in events:
                message = key.data
                if mask & selectors.EVENT_WRITE:
                    self.process_write(message)
                if mask & selectors.EVENT_READ :
                    message.process_read()
                    self.process_read(message)

    def process_write(self, message_of_mine): 
        """
        废弃
        """
        # print("process input")

        data = input(">> ")

        message_of_mine.send({"type":"message"}, data.encode("utf-8"))

    def process_read(self, message): 
        """
        如何处理接收到的信息
        子类重载这个方法实现对于消息的处理
        """
        print("recv:", message.header, message.content)
        message.send(message.header, message.content)


    def run(self): 
        """
        示范性自定义方法
        """
        listen_thread = threading.Thread(target=self._listen, daemon=True)

        listen_thread.start()

        while True: 
            pass

if __name__ == '__main__':
    
    client = Client("127.0.0.1", 63335)
    client.run()