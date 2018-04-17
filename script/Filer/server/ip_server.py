import socket
import select
import logging
import logging.config
#是否要持久化数据？数据库？文件？抑或不持久化，直接存入字典，或者列表。需要一个时间戳，以保证在线设备是最新的

#是不是应该采用OOP
logging.config.fileConfig("stan.conf")
log = logging.getLogger("second")



class IP_Server :
	def __init__(self) :
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setblocking(False)
		self.server.bind(('0.0.0.0',6000))
		self.server.listen(10)

		self.r_list = [self.server]
		self.w_list = []

		self.log = log

		self.device = {}

		self.ip_record = []
		log.info("ip server start bind in port 6000")
# 应该采用ID作为唯一的标识符，或者IP？
	def run(self) :
		while True:
			read_list, write_list, error_list = select.select(self.r_list, self.w_list, self.r_list)

			for s in read_list :
				if s is self.server :
					client, client_address = s.accept()
					if client_address[0] in self.ip_record :
						client.close()
					else :
						client.setblocking(False)
						self.r_list.append(client)
						#self.client.append(client)
						self.device[client] = [bytes(client_address[0], 'utf-8'),client_address[0],False]
						self.ip_record.append(client_address[0])
						print(client_address,'is on-line')
						self.log.info("IP: %s, port: %s is on-line"%client_address)
				else :
					try :
						data = s.recv(1024)
					except ConnectionResetError as er :
						self.log.error("error happen in %s , error information: %s"%(self.device[s][1], er))
						print(er)
						self.close_one_client(s)
						pass
					else :
						if data.decode('utf-8') == 'off-line' :
							#print(self.device[s],'is off-line')
							#self.client.remove(s)
							self.log.info("%s is off-line"%self.device[s][1])
							self.close_one_client(s)

						elif self.check_report(data, s) :
							#防止有人动手脚
							if not self.device[s][2] :
								self.device[s][0] = data + b'\n' + self.device[s][0]
								self.device[s][2] = True
							s.send(b'get')
							self.log.info("recv report from %s (%s), and send get to it already"%(self.device[s][1], self.device[s][0]))
							self.tell_other_device()
						else :
							self.close_one_client(s)

	def close_one_client(self, s) :
		
		if s in self.r_list :
			self.r_list.remove(s)
			s.close()
			self.log.info("%s is close"%self.device[s][1])
		if s in self.device.keys() :
			self.ip_record.remove(self.device[s][1])
			del self.device[s]
			self.tell_someone_offline()


	def check_report(self,data, s) :
		try :
			data = data.decode('utf-8')
			data = data.split('\n')
		except Exception as er :
			self.log.error("%s send wrong format data, can't decode (%s) , error is %s , going to close"%(self.device[s][1], data, er))
			#self.close_one_client(s)
			return False
		if len(data)==2 and len(data[0])<40 and len(data[1])<20 :
			return True
		else :
			self.log.warning("%s send wrong message (%s), going to close"%(self.device[s][1], data))
			return False

	def tell_other_device(self) :
		if len(self.ip_record) > 1 :
			print(self.ip_record)
			for client in self.device.keys() :
				message = b''
				for s in self.device.keys() :
					if not client is s :
						message += self.device[s][0] + b'\n\n'
				client.send(message)

	def tell_someone_offline(self) :
		for client in self.device.keys() :
			message = b''
			for s in self.device.keys() :
				if not client is s :
					message += self.device[s][0] + b'\n\n'
			if message == b'' :
				message = b'0'
			client.send(message)

Server = IP_Server()
Server.run()
