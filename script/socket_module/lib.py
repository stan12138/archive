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

        self.info = None

        self.recv_time = None

        self.send_time = None

        self.header_length = None
        self.header = None
        self.body = None
        self.content_length = None

        self.default_recv_length = default_recv_length

    def _read(self, length=None): 

        recv_length = self.default_recv_length if length==None else length

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

    def _write(self, message): 
        """
        消息已经经过二进制处理了
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

    def _parse_header(self, data): 
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

    def _process_header(self, header_length, data): 
        while len(data)<header_length: 
            data += self._read(header_length-len(data))
        header_data = data[:header_length]

        header = self._parse_header(header_data)
        if "CL" not in header: 
            raise NeedCLError("header wrong, without content length")

        data = data[header_length:]

        return header, data


    def _process_body(self, data, content_length): 
        while len(data)<content_length:
            data += self._read(content_length-len(data))

        return data


    def read(self): 

        data = self._read(3)
        header_length_info = 2
        self.header_length = 0
        self.content_length = 0

        while len(data)<header_length_info: 
            data += self._read(1)

        self.header_length = int.from_bytes(data[:header_length_info], byteorder="little")

        self.header, data = self._process_header(self.header_length, data[2:])

        self.content_length = int(self.header["CL"])

        if self.content_length>0 :
            self.content = self._process_body(data, self.content_length)
        else :
            self.content = None

        self.recv_time = time.time()


    def send(self, header, content=None):
        """
        content必须是二进制
        """
        message = self._construct_message(header, content)

        self._write(message)

        self.send_time = time.time()

    def _construct_message(self, header, content): 
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


    def process_read(self): 
        # print("process read")
        self.read()