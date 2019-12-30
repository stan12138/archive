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
考虑加入日志功能  19.12.30 2：26

"""

"""
考虑加入多播功能 19.12.30 21:53
"""


class Server :

    def __init__(self, ip, port) :

        self.addr = (ip, port)
        self.server = self.__generate_server()

        self.__selector = selectors.DefaultSelector()

        self.__selector.register(self.server, selectors.EVENT_READ, data=None)

        self.messenger = []

        self._lock = threading.Lock()

        signal.signal(signal.SIGINT, self.__interrupt_handler)

    def __interrupt_handler(self, sig, frame): 
        """
        捕捉到ctr-c
        定义处理方式为关闭所有socket
        private
        """
        print("get stop signal......")
        for item in self.messenger: 
            self.__selector.unregister(item.socket)
            item.socket.close()
        self.__selector.unregister(self.server)
        self.server.close()

        print("close work done, bye~~~")
        sys.exit(0)

    def __generate_server(self) :
        """
        生成TCP服务器
        配置TCP服务器
        private
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.addr)
        sock.listen()

        sock.setblocking(False)

        return sock


    def __accept(self, sock): 
        """
        接受一个客户端的连接
        private
        """
        client, addr = sock.accept()
        print("get client:", addr)
        client.setblocking(False)

        message = lib.Messenger(self.__selector, client, addr)

        self.__selector.register(client, selectors.EVENT_READ, data=message)

        self._lock.acquire()
        self.messenger.append(message)
        self._lock.release()



    def _listen(self) :
        """
        持续监听
        供外部调用，但是不希望被override
        """
        while True: 
            events = self.__selector.select(timeout=None)

            for key, mask in events:
                # print(key.data) 
                if key.data == None: 
                    self.__accept(key.fileobj)
                else: 
                    message = key.data
                    try:
                        message.process_read()
                    except lib.PartnerCloseError:
                        self._close_client(message)
                    except lib.RecvNothing:
                        self._close_client(message)
                    else:
                        self.process_read(message)



    def _close_client(self, message_of_client, need_lock=True): 
        """
        关闭一个客户端，可以选择是否需要使用锁，注意
        绝对不可以遍历self.messenger同时删除

        外部可以调用
        不要override
        """
        self.__selector.unregister(message_of_client.socket)
        if need_lock:
            self._lock.acquire()
            self.messenger.remove(message_of_client)
            self._lock.release()
        else: 
            self.messenger.remove(message_of_client)

        print("close one client:", len(self.messenger))

    def _broadcast(self, header, content=None): 
        """
        向全体客户端广播信息

        外部可以调用
        不要override
        """
        self._lock.acquire()
        remove_list = []
        for item in self.messenger: 
            try:
                item.send(header, content)
            except Exception as er:
                print(er) 
                remove_list.append(item)
        for item in remove_list: 
            self._close_client(item, need_lock=False)
        self._lock.release()


    def serve_forever(self): 
        """
        示范性自定义方法
        使用两个线程同时实现了listen和broadcast
        """
        run_thread = threading.Thread(target=self._listen, daemon=True)
        
        broadcast = threading.Thread(target=self.run_broadcast, daemon=True)


        run_thread.start()
        broadcast.start()

        while True :
            pass

    def run_broadcast(self): 
        """
        示范性自定义方法
        配合serve_forever进行广播
        """
        while True: 
            print("broadcast")
            self._broadcast({"TP":"broadcast"}, "我是服务器".encode("utf-8"))
            time.sleep(2)

    def process_read(self, message_of_client): 
        """
        子类通过重写这个方法实现对于接收到客户端信息之后的处理
        """
        print("recv message:", message_of_client.header, message_of_client.content)

        message_of_client.send({"type":"message"}, message_of_client.content)



if __name__ == '__main__':
    
    server = Server("0.0.0.0", 63335)
    server.serve_forever()