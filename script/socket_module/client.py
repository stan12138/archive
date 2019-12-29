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

        self.addr = (ip, port)
        self.client = self._generate_client()

        self.selector = selectors.DefaultSelector()

        events = selectors.EVENT_READ #| selectors.EVENT_WRITE
        self.messenger = lib.Messenger(self.selector, self.client, self.addr)
        self.selector.register(self.client, events, data=self.messenger)

        self._lock = threading.Lock()

        signal.signal(signal.SIGINT, self._interrupt_handler)

    def _interrupt_handler(self, sig, frame): 
        """
        ctr-c捕捉
        """
        print("get stop signal......")

        self.selector.unregister(self.client)
        self.client.close()

        print("close work done, bye~~~")
        sys.exit(0)

    def _generate_client(self) :

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(self.addr)

        return sock

    def _listen(self) :

        while True: 
            events = self.selector.select(timeout=1)

            for key, mask in events:
                # print(key.data, mask&selectors.EVENT_READ)
                message = key.data
                if mask & selectors.EVENT_WRITE:
                    self.process_write(message)
                if mask & selectors.EVENT_READ :
                    message.process_read()
                    self.process_read(message)

    def run(self): 
        listen_thread = threading.Thread(target=self._listen, daemon=True)

        listen_thread.start()

        while True: 
            pass


    def process_write(self, message_of_mine): 
        # print("process input")
        data = input(">> ")

        message_of_mine.send({"type":"message"}, data.encode("utf-8"))

    def process_read(self, message): 
        print("recv:", message.header, message.content)
        message.send(message.header, message.content)

if __name__ == '__main__':
    
    client = Client("127.0.0.1", 63335)
    client.run()