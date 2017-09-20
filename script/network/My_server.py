import socket
import io
import sys
import http.client


def show_ip() :
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try :
		s.connect(('baidu.com',80))
		ip = s.getsockname()[0]
		s.close()
	except :
		ip = 'N/A'
	return ip

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
		print('waiting for connect in port : ',self.port,' ,use CTR-C stop server')
		try :
			while self.life :
				self.client,self.cli_addrs = self.server.accept()
				#print("got on connect")
				self.handle_request()
			print('going stop.....')
			self.server.close()
		except Exception :
			print('something happen,sever going to close....')
			if self.client :
				self.client.close()
			self.server.close()
			sys.exit()
		
	def handle_request(self) :
		self.env = {}
		self.rfile = self.client.makefile('rb',-1)
		self.get_requestline()
		self.get_headers()
		self.get_body()

		self.response_body = self.wsgi(self.env,self.response)
		#print("trying to send")
		#print(self.response_body[:20])
		if self.response_body == 1 :
			pass
		else :
			#print('wtf')
			self.send_close()
	def get_requestline(self) :
		self.raw_requestline = self.rfile.readline(65537)
		if len(self.raw_requestline) > 65536 :
			print("request line too long , recive fail , going to close......")
			self.client.close()
			self.server.close()
		else :
			self.parse_request_line()



	def get_headers(self) :
		self.headers = http.client.parse_headers(self.rfile,_class=http.client.HTTPMessage)
		#print(type(self.headers))
		for i in self.headers :
			self.env[i] = self.headers.get(i,'')

		

	def parse_request_line(self) :

		requestline = self.raw_requestline.decode('utf-8')
		requestline = requestline.rstrip('\r\n')
		self.request_line = requestline

		words = self.request_line.split()
		if len(words)==3 :
		
			command,path,version = words
			self.env['method'] = command
			self.env['path'] = path
			self.env['version'] = version
			
		else :
			print('sorry , I do not accept not len(request line)==3')

		
	def get_body(self) :
		self.env['wsgi.input'] = self.rfile


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
			#print(body)
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
			#print('begin send')
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

	
	