import socket
import threading
import os.path
import sys
import time
import configparser

'''
这是一个命令行版本的文件传输工具，因为我困于input阻塞的问题，一直无法解决，所以
电脑端将无法选择设备。
'''



class IP_Handler :
	def __init__(self, server_address, port) :
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = server_address
		self.ID = 'Stan-Laptop'
		self.port = port
		
		self.device = []
	def connect(self) :
		try_connect = True
		while try_connect :
			try :
				self.client.connect(self.server_address)
				try_connect = False
			except Exception as er:
				print(er)
	
	def report(self) :
		success = False
		while not success :
			self.client.send(bytes(self.ID+'\n'+str(self.port),'utf-8'))
			print("send report")
			data = self.client.recv(1024)
			if data == b'get' :
				success = True
	def recv_ip(self) :
		while True :
			message = self.client.recv(4096)
			self.parse_ip_info(message)
	def parse_ip_info(self,message) :
		self.device = []
		
		message = message.decode('utf-8')
		if message == '0' :
			pass
		else :
			message = message.split('\n\n')
			#self.device = []
			for s in message :
				if s :
					s = s.split('\n')
					self.device.append((s[0],s[2],int(s[1])))
		self.device_caller(self.device)
	
	def off_line(self) :
		self.client.send(b'off-line')
		self.client.close()
		
	def run(self) :
		try :
			self.connect()
			self.report()
			self.recv_ip()
		except :
			pass

	def set_devices_caller(self, func) :
		self.device_caller = func

class CommunicateServer :
	def __init__(self) :
		self.port = 63834
		while True :
			try :
				self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.server.bind(('', self.port))
				break
			except OSError :
				self.port += 1
		self.server.listen(5)

		self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.send_try_connect = True
		self.recv_try_connect = True

		self.send_loop = True
		self.recv_loop = True

		self.send_connect = False
		self.recv_connect = False

		self.recv_size = 1024*512
	def server_run(self) :
		#try_connect = True

		while self.send_try_connect :
			client, client_address = self.server.accept()
			self.send_try_connect = False
			self.send_connect = True
			self.get_client_address = client_address[0]
			print("get client.....")
			self.send_server = client
			

		while self.send_loop :
			a = input(">> ")
			if a=='file' :
				file_ok = False
				while not file_ok :
					try :
						file_name = input("please input filename: ")
						if "\\" in file_name :
							file_name = file_name.replace("\\","/")
						if '"' in file_name :
							file_name = file_name.replace('"','')
						file_size = os.path.getsize(file_name)
						file_ok = True
					except Exception as er :
						print(er)
						print("please try again ")
				times = int(file_size/self.recv_size)+1

				if "/" in file_name :
					file_name1 = file_name[::-1]
					file_name1 = file_name[-1*file_name1.index("/"):]
				else :
					file_name1 = file_name

				content = bytes(str(file_size)+'\r\n'+str(times)+'\r\n'+file_name1,'utf-8')
				head = bytes("file\r\n"+str(len(content))+'\r\n', 'utf-8')+content
				#这里要注意，原始的字符串的长度和二进制编码后的长度并不相同
				self.send_server.send(head)
				time.sleep(1)
				#哇，找到了，找到了，当发送文件的时候，客户端解析头需要一小段时间，而服务端完全没有等待，直接就发送了，所以导致
				#始终会有大约4344字节的消息丢失，所以只需要延时一点就可以了
				read_length = 0
				with open(file_name, 'rb') as fi :
					for i in range(times) :
						try :
							data = fi.read(self.recv_size)
							#self.send_server.sendall(data)
							#这里是一个很神奇的错误点，无论是send还是sendall都无法保证数据完整送到，偏偏我接受了
							#send的返回值之后就可以保证了，实在是很奇怪，问题到底出在哪?
							read_length += self.send_server.send(data)
							print('\r'+str(i)+'    '+str(read_length), end='')
						except :
							pass
			elif a=='stop' :
				self.shutdown()
			else :
				data = bytes('message\r\n'+str(len(a))+'\r\n'+a, 'utf-8')
				self.send_server.send(data)

	def client_run(self) :
		#try_connect = True
		while self.recv_try_connect:
			try :
				print("self.partner_address",self.partner_address)
				self.recv_server.connect(self.partner_address)
				self.recv_try_connect = False
				self.recv_connect = True

				#self.recv_file = self.recv_server.makefile('rb')
				print("get server.....")
			except :
				print("\rconnect wrong try again.....",end="")
				self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while self.recv_loop :
			self.recv_file = self.recv_server.makefile('rb')
			content_type = self.recv_file.readline()
			content_type = content_type.decode('utf-8')
			content_type = content_type.rstrip('\r\n')
			

			content_length = self.recv_file.readline()
			content_length = content_length.decode('utf-8')
			content_length = int(content_length.rstrip('\r\n'))


			data = self.recv_file.read(content_length)
			self.recv_file.close()
			#print(content_length)
			#print(len(data)==content_length)
			data = self.parse_data(data, content_type)

			if content_type == 'message' :
				print(data)
			elif content_type == 'file' :
				file_size, times, filename = data
				length = 0
				print(file_size, filename)
				with open('inbox/'+filename,'wb') as fi :		#18.4.9 0:05 文件传输出现错误，无法读取足够长度的内容，未知错误出在何处，发送或者接受？
					while  True:
						data = self.recv_server.recv(self.recv_size)
						#同样不知道为啥，如果此处使用file进行接收一定会丢失一些字节
						length += len(data)
						fi.write(data)
						print('\r'+str(length), end='')
						if length >= file_size :
							break

			

	def shutdown(self) :
		self.send_try_connect = False
		self.send_loop = False
		self.recv_loop = False
		self.recv_try_connect = False
		try :
			self.recv_file.close()
		except :
			pass
		self.server.close()
		self.recv_server.close()
		try :
			self.send_server.close()
		except :
			pass
		sys.exit()
	def parse_data(self, data, content_type) :
		data = data.decode('utf-8')

		if content_type == 'message' :
			return data
		elif content_type == 'file' :
			data = data.split('\r\n')
			return int(data[0]), int(data[1]), data[2]

class Manager :
	def __init__(self) :

		self.all_devices = []
		self.partner_address = ()

		cf = configparser.ConfigParser()
		cf.read("filer.conf")

		server_address = (cf.get("ip-server","ip"),cf.getint("ip-server", "port"))
		client_address = []
		choose_already = False

		self.my_client = CommunicateServer()
		self.ip_reporter = IP_Handler(server_address, self.my_client.port)
		self.ip_reporter.set_devices_caller(self.get_devices)

	def run(self) :
		self.ip_thread = threading.Thread(target=self.ip_reporter.run, daemon=True)
		self.server_thread = threading.Thread(target=self.my_client.server_run, daemon=True)

		self.ip_thread.start()
		self.server_thread.start()

		while self.my_client.send_try_connect:
			pass

		time.sleep(1)
		self.ip_reporter.off_line()

		print("my_client.get_client_address",self.my_client.get_client_address)
		self.my_client.partner_address = self.find_partner(self.my_client.get_client_address)
		self.client_thread = threading.Thread(target=self.my_client.client_run, daemon=False)
		self.client_thread.start()
		self.client_thread.join()
		print("client runing.....")

	def get_devices(self, devices) :
		[self.all_devices.append(d) for d in  [i for i in devices if not i in self.all_devices]]
		print(self.all_devices)


	def find_partner(self, ip) :
		for d in self.all_devices :
			if ip==d[1] :
				return (d[1], d[2])


if __name__ == '__main__':
	manger = Manager()
	manger.run()

#我发现了一个巨牛叉的事情，已经知道了，我们可以在其他程序内部运行python，刚才测试了ui也是可以的哦，你明白什么意思
#然后，更加牛叉的是，我发现了从网上弄到的那个转移文件的程序的工作方法是拿到了原本文件的绝对路径而已，这意味着我可以把这个嵌入到我的代码里面
#更进一步，我一会要测试一下，如果我能在指定文件夹写文件，那就更加牛叉了.

#不让读也不让写，目录都不让读