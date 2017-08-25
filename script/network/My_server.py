import socket
import io
import sys


class Stop(Exception) :
	pass


class Server :
	def __init__(self,host='',port='8000') :
		self.host = host
		self.port = port
		
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.server.bind((self.host,self.port))
		self.server.listen(5)
		self.life = True

	def set_app(self,application) :
		self.wsgi = application
		
	def run(self) :
		print('waiting for connect in port : ',self.port,'use CTR-C stop server')
		try :
			while self.life :
				self.client,self.cli_addrs = self.server.accept()
				#print("got on connect")
				self.handle_request()
			print('going stop.....')
			self.server.close()
		except Stop :
			print('ok')
			self.server.close()
			sys.exit()
		
	def handle_request(self) :
		
		self.cli_message = self.client.recv(4096)
		
		print(self.cli_message)

		self.cli_message = self.cli_message.decode('utf-8')
		#self.cli_message = self.cli_message.replace('\r\n\r\n','\r\n')
		self.env = {}
		#print("decode done")
		self.parse_request(self.cli_message)
		self.response_body = self.wsgi(self.env,self.response)
		#print("trying to send")
		if self.response_body.decode('utf-8') == 'no' :
			pass
		else :
			self.send_close()
	def parse_request(self,message) :
		message = message.split('\r\n\r\n')
		flage = False
		if len(message) == 2 :
			front = message[0]
			body = message[1]
			flage = True
		else :
			front = message[0]
		#print('first split done')
		front = front.split('\r\n')
		start_line = front[0].split()
		if len(start_line)==3 :
			self.env['method'] = start_line[0]
			self.env['path'] = start_line[1]
			self.env['version'] = start_line[2]
		del front[0]
		for i in front :
			t = i.split(': ')
			if len(t) == 2 :
				self.env[t[0]] = t[1]
		if self.env['method']=='POST' and flage :
			print(body)
			self.env['wsgi.input'] = io.StringIO(body)
		#print("phrase done")


	def response(self,code,header) :
		self.code = bytes(code,'utf-8')
		self.header = header
		
	def send_close(self) :
		try :
			res = b'HTTP/1.1 '+self.code+b'\r\n'
			h1 = ''
			#print(res)
			for i in self.header :
				if len(i)==2 :
					h1 += i[0]
					h1 += ': '
					h1 += i[1]
			res += bytes(h1,'utf-8')
			res += b'\r\n\r\n'
			res += self.response_body
			#print(res)
			self.client.sendall(res)
			#self.life -= 1
		finally :
			self.client.close()
			#if self.life < 1 :
			#	self.server.close()

def make_server(host,port,application) :
	serve = Server(host,port)
	serve.set_app(application)
	return serve

	
	