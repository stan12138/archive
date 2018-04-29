import socket
import time
import threading
import os
import console

class CommunicateServer :
	def __init__(self, window, get_device_caller, message_box, send_button, file_bar, get_bar) :
		self.port = 63834
		while True:
			try :
				self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.server.bind(('', self.port))
				break
			except OSError :
				self.port += 1
		self.server.listen(5)
		self.window = window
		self.get_device_caller = get_device_caller
		self.message_box = message_box
		self.send_button = send_button

		self.file_bar = file_bar
		self.get_bar = get_bar

		self.want_send = False
		self.send_type = ""
		self.message_content = ""
		self.file_name = ""

		self.show_lock = threading.Lock()

		self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.partner_address = ''

		self.send_try_connect = True
		self.recv_try_connect = True

		self.send_loop = True
		self.recv_loop = True

		self.send_connect = False
		self.recv_connect = False

		self.recv_size = 1024*512

		self.set_ui_action()

	def set_partner(self, address) :

		self.partner_address = address
		
	def server_run(self) :
		#try_connect = True

		while self.send_try_connect :
			try :
				client, client_address = self.server.accept()
			except :
				pass
			else :
				
				self.send_try_connect = False
				self.send_connect = True

				self.show_lock.acquire()
				self.window.text += "get client....\n"
				self.show_lock.release()
	
				self.send_server = client
				if not self.partner_address :
					self.get_device_caller((client_address[0], 63834))

		while self.send_loop :
			while not self.want_send :
				if not self.send_loop :
					self.send_type = 'wrong'
					break
			if self.send_type == 'file' :
				file_name = self.file_name
				file_size = os.path.getsize(file_name)
				times = int(file_size/self.recv_size)+1
				if "/" in file_name :
					file_name1 = file_name[::-1]
					file_name1 = file_name[-1*file_name1.index("/"):]
				else :
					file_name1 = file_name

				content = bytes(str(file_size)+'\r\n'+str(times)+'\r\n'+file_name1,'utf-8')
				head = bytes("file\r\n"+str(len(content))+'\r\n', 'utf-8')+content
				self.send_server.send(head)

				self.show_lock.acquire()
				self.window.text += ("going to send " + file_name1 + '\n')
				self.show_lock.release()

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
							self.file_bar.set_value(read_length/file_size)

						except :
							pass

				self.show_lock.acquire()
				self.window.text += (file_name1 + "send done" + '\n')
				self.show_lock.release()

			elif self.send_type=='message' :

				data = bytes('message\r\n'+str(len(self.message_content))+'\r\n'+self.message_content, 'utf-8')
				self.send_server.send(data)

				self.message_box.text = ''

				self.show_lock.acquire()
				self.window.text += (self.message_content + '\n')
				self.show_lock.release()

			self.want_send = False
		#print('server dead')
	def client_run(self) :
		#try_connect = True
		while self.recv_try_connect:
			try :
				self.show_lock.acquire()
				self.window.text += 'try to connect with '+str(self.partner_address)+'\n'
				self.show_lock.release()
				#print('try to connect with :',self.partner_address)
				self.recv_server.connect(self.partner_address)
				self.recv_try_connect = False
				self.recv_connect = True

				#self.recv_file = self.recv_server.makefile('rb')
				self.show_lock.acquire()
				self.window.text += "get server....\n"
				self.show_lock.release()
			except :
				self.recv_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		while self.recv_loop :
			self.recv_file = self.recv_server.makefile('rb')
			try :
				content_type = self.recv_file.readline()
			
				content_type = content_type.decode('utf-8')
				content_type = content_type.rstrip('\r\n')
				
	
				content_length = self.recv_file.readline()
				content_length = content_length.decode('utf-8')
				content_length = int(content_length.rstrip('\r\n'))
	
	
				data = self.recv_file.read(content_length)
				self.recv_file.close()
				data = self.parse_data(data, content_type)
			except :
				self.recv_file.close()
			
			try :
				if content_type == 'message' :
					self.show_lock.acquire()
					self.window.text += (data+'\n')
					self.show_lock.release()
	
				elif content_type == 'file' :
					file_size, times, filename = data
	
					self.show_lock.acquire()
					self.window.text += ('server send '+filename+'\n')
					self.show_lock.release()
					filename = '/private/var/mobile/Containers/Shared/AppGroup/1E6396A6-FB23-4A10-B1BB-B5F1F35BE42E/Pythonista3/Documents/inbox/'+filename
					length = 0
					with open(filename,'wb') as fi :		#18.4.9 0:05 文件传输出现错误，无法读取足够长度的内容，未知错误出在何处，发送或者接受？
						while True :
							#data = self.recv_file.read(self.recv_size)
							data = self.recv_server.recv(self.recv_size)
							length += len(data)
							fi.write(data)
							self.get_bar.set_value(length/file_size)
							if length >= file_size :
								self.show_lock.acquire()
								self.window.text += "file recv done\n"
								self.show_lock.release()
								break
					console.open_in(filename)
			except :
				self.recv_server.close()
		#print('client dead')
	def close(self,sender) :
		self.shutdown()	

	def shutdown(self) :
		self.send_try_connect = False
		self.send_loop = False
		self.recv_loop = False
		self.recv_try_connect = False
		
		try :
			self.server.shutdown(socket.SHUT_RDWR)
			self.server.close()
		except :
			pass
		#print('server close')
		try :
			self.send_server.shutdown(socket.SHUT_RDWR)
			self.send_server.close()
		except Exception as er :
			pass
		#print('send server close')
		
		try :
			self.recv_server.shutdown(socket.SHUT_RDWR)
			self.recv_server.close()
		except :
			pass
		#print('recv server close')
		
		try :
			#print('try to close recv file')
			#self.recv_file.shutdown(socket.SHUT_RDWR)
			self.recv_file.close()
		except Exception as er :
			pass
		#print('recv file close')
		#sys.exit()
	def parse_data(self, data, content_type) :
		try :
			data = data.decode('utf-8')
		except Exception as er :
			#print(er)
			#print(data)
			self.shutdown()

		if content_type == 'message' :
			return data
		elif content_type == 'file' :
			data = data.split('\r\n')
			return int(data[0]), int(data[1]), data[2]

	def set_ui_action(self) :
		self.send_button.action = self.send_push
		#self.close_button.action = self.close

	def send_push(self, sender) :
		self.set_send("message", self.message_box.text)

	def set_send(self, send_type, content) :
		self.send_type = send_type
		if send_type == "file" :
			self.file_name = content
		elif send_type == "message" :
			self.message_content = content
		self.want_send = True
