import socket


class IP_Handler :
	def __init__(self, server_address, port) :
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = server_address
		self.ID = 'Stan-iPad'
		self.port = port
		
		self.device = []
		
		self.work_normal = True
		self.try_connect = True
		self.success = False
	def connect(self) :
		#self.try_connect = True
		while self.try_connect :
			try :
				self.client.connect(self.server_address)
				self.try_connect = False
			except :
				pass
	
	def report(self) :
		#print('begin report')
		self.success = False
		while not self.success :
			self.client.send(bytes(self.ID+'\n'+str(self.port),'utf-8'))
			data = self.client.recv(1024)
			if data == b'get' :
				#print(data)
				self.success = True
				
	def recv_ip(self) :
		#print('ready to recv ip')
		while self.work_normal :
			message = self.client.recv(4096)
			self.parse_ip_info(message)
			
	def parse_ip_info(self,message) :
		self.device = []
		#print(message)
		message = message.decode('utf-8')
		if message == '0' :
			pass
		else :
			message = message.split('\n\n')
			#self.device = []
			for s in message :
				if s :
					s = s.split('\n')
					self.device.append((s[0],s[2],int(s[1]))) #列表的每一项是一个设备的元组，每个元组的结构都是(ID,ip,port)
		#print(self.device)
		self.call(self.device)
		#print('call already')
	
	def off_line(self) :
		try :
			self.client.send(b'off-line')
		except :
			print('can not send offline')
		self.client.close()
		
	def run(self) :
		try :
			self.connect()
			self.report()
			self.recv_ip()
			#print('IP handler dead')
		except :
			pass
	def change_server(self, address) :
		self.success = True
		self.try_connect = False
		self.work_normal = False
		self.client.close()
		self.__init__(address)
		
	def set_update_ui_caller(self, call) :
		#print('set ip call')
		self.call = call
