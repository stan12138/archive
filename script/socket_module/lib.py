"""
固定通信协议：
2B  ---->  header length    little byteorder unsigned
---------- header    encoding: utf-8
CL:123;CT:image;     分号分割的键值对形式，结尾不包含分号, 至少包含一个CL
---------- body      长度由header的CL(content length)指定
自定义
"""

"""
考虑重新设计一下异常继承
设计一个NeedClose的异常，然后让所有应该导致关闭的异常都继承这个
这样就比较容易捕捉需要关闭socket的异常了
"""
import time

__all__ = ["Messenger", "RecvNothing", "SendNothing", "EncodeError", "DecodeError", "NeedCLError", "HeaderFormatError", "PartnerCloseError"]



class RecvNothing(Exception): pass
# recv没有收到信息， 应该关闭

class SendNothing(Exception): pass
#send没有发出去消息，应该关闭

class EncodeError(Exception): pass
#content的编码错误，需要bytes，无须关闭

class DecodeError(Exception): pass
#解码错误，收到的数据的header解码错误，客户端有问题

class NeedCLError(Exception): pass
#客户端发送的数据缺少了CL字段

class HeaderFormatError(Exception): pass
#客户端的header解析错误，不满足键值对的要求

class PartnerCloseError(Exception): pass
#对方关闭了

class Messenger:

    def __init__(self, selector, fileobj, addr, default_recv_length=4096): 

        self.socket = fileobj
        self.addr = addr

        self.recv_time = None
        self.send_time = None

        self.header = None
        self.body = None

        self.__header_length = None

        self.__content_length = None

        self.__default_recv_length = default_recv_length

    def __read(self, length=None): 
        """
        读取一定数据
        private
        """

        recv_length = self.__default_recv_length if length==None else length

        try: 
            data = self.socket.recv(recv_length)
        except BlockingIOError:
            pass
        except ConnectionResetError: 
            raise PartnerCloseError("recv close, partner close(reset), should close")
        else: 
            if data: 
                return data
            else: 
                raise RecvNothing("recv nothing, should close")

    def __write(self, message): 
        """
        发送二进制消息
        private
        """

        while len(message)>0: 
            try: 
                l = self.socket.send(message)
            except BlockingIOError: 
                pass
            except ConnectionAbortedError: 
                raise PartnerCloseError("partner close "+str(self.addr[0])+" "+str(self.addr[1]))
            else: 
                if l<=0:
                    raise SendNothing("send nothing, should close")
                else :
                    message = message[l:]

    def __parse_header(self, data): 
        """
        解析Header
        private
        """
        try: 
            data = data.decode("utf-8")
        except: 
            raise DecodeError("data decode error")

        header = {}
        data = data.split(";")
        for item in data :
            info = item.split(":")
            if len(info)!=2: 
                raise HeaderFormatError("wrong format info")
            else: 
                header[info[0]] = info[1]

        return header

    def __process_header(self, header_length, data): 
        """
        处理header
        private
        """
        while len(data)<header_length: 
            data += self.__read(header_length-len(data))
        header_data = data[:header_length]

        header = self.__parse_header(header_data)
        if "CL" not in header: 
            raise NeedCLError("header wrong, without content length")

        data = data[header_length:]

        return header, data


    def __process_body(self, data, content_length): 
        """
        处理body
        private
        """
        while len(data)<content_length:
            data += self.__read(content_length-len(data))

        return data


    def __construct_message(self, header, content): 
        """
        构建消息
        private
        """
        if content:         
            if type(content) != bytes: 
                raise EncodeError("content must be bytes")
            content_length = len(content)
        else: 
            content_length = 0

        header_message = "CL:%s;"%content_length
        for key in header: 
            header_message += str(key)+":"+str(header[key])+";"

        header_message = header_message[:-1]  #删除最后一个;

        header_message = header_message.encode("utf-8")

        header_length = len(header_message)

        message_head = header_length.to_bytes(2, byteorder="little")

        message = message_head+header_message

        if content: 
            message += content      

        return message



    def read(self): 
        """
        读取数据
        供外部调用
        """
        data = self.__read(3)
        header_length_info = 2
        self.__header_length = 0
        self.__content_length = 0

        while len(data)<header_length_info: 
            data += self.__read(1)

        self.__header_length = int.from_bytes(data[:header_length_info], byteorder="little")

        self.header, data = self.__process_header(self.__header_length, data[2:])

        self.__content_length = int(self.header["CL"])

        if self.__content_length>0 :
            self.content = self.__process_body(data, self.__content_length)
        else :
            self.content = None

        self.recv_time = time.time()


    def send(self, header, content=None):
        """
        content必须是二进制
        发送信息
        供外部调用
        """
        message = self.__construct_message(header, content)

        self.__write(message)

        self.send_time = time.time()


    def process_read(self): 
        """
        处理读数据请求，供外部调用
        """
        self.read()