"""
再次尝试重新设计Filer的服务器
author: stan
date: 2019.12.27 17:20
"""
import socket
import time
import sys
import selectors

import threading

import lib


class Client :

    def __init__(self, ip, port) :

        self.addr = (ip, port)
        self.client = self.generate_client()

        self.selector = selectors.DefaultSelector()

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = lib.Messenger(self.selector, self.client, self.addr)
        self.selector.register(self.client, events, data=message)

        self._lock = threading.Lock()

    def generate_client(self) :

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(self.addr)

        return sock

    def run(self) :

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


    def process_write(self, message_of_mine): 
        # print("process input")
        data = input(">> ")

        message_of_mine.send({"type":"message"}, data.encode("utf-8"))

    def process_read(self, message): 
        print("recv:", message.header, message.content)

if __name__ == '__main__':
    
    client = Client("127.0.0.1", 63335)
    client.run()