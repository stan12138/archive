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
服务器在某些运行阶段，是无法使用ctrl-c关闭的
ctrl-c会被延迟到其余阶段
考虑一下是不是要使用多线程运行，也方便广播
"""


class Server :

    def __init__(self, ip, port) :

        self.addr = (ip, port)
        self.server = self.generate_server()

        self.selector = selectors.DefaultSelector()

        self.selector.register(self.server, selectors.EVENT_READ, data=None)

        self.messenger = []

        self._lock = threading.Lock()

        signal.signal(signal.SIGINT, self.interrupt_handler)

    def interrupt_handler(self, sig, frame): 
        print("get stop signal......")
        for item in self.messenger: 
            self.selector.unregister(item.socket)
            item.socket.close()
        self.selector.unregister(self.server)
        self.server.close()

        print("close work done, bye~~~")
        sys.exit(0)

    def serve_forever(self): 
        run_thread = threading.Thread(target=self.run, daemon=True)
        
        run_thread.start()

        while True :
            pass


    def generate_server(self) :

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.addr)
        sock.listen()

        sock.setblocking(False)

        return sock

    def run(self) :

        while True: 
            events = self.selector.select(timeout=None)

            for key, mask in events:
                # print(key.data) 
                if key.data == None: 
                    self.accept(key.fileobj)
                else: 
                    message = key.data
                    try:
                        message.process_read()
                    except lib.PartnerCloseError:
                        self._close_client(message)
                    except lib.RecvNothing:
                        self._close_client(message)
                    else:
                        self.respond(message)

    def accept(self, sock): 
        client, addr = sock.accept()
        print("get client:", addr)
        client.setblocking(False)

        message = lib.Messenger(self.selector, client, addr)

        self.selector.register(client, selectors.EVENT_READ, data=message)

        self._lock.acquire()
        self.messenger.append(message)
        self._lock.release()

    def broadcast(self): 

        pass

    def respond(self, message_of_client): 

        print("recv message:", message_of_client.header, message_of_client.content)

        message_of_client.send({"type":"message"}, message_of_client.content)

    def _close_client(self, message_of_client): 
        self.selector.unregister(message_of_client.socket)
        self._lock.acquire()
        self.messenger.remove(message_of_client)
        self._lock.release()

        print("close one client:", len(self.messenger))


if __name__ == '__main__':
    
    server = Server("0.0.0.0", 63335)
    server.serve_forever()