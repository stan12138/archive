import socket
import io
import sys
import http.client
import logging
import logging.config
import ctypes

__all__ = ['f_log','s_log','make_server']


class stan_log :
	def __init__(self,logger) :
		self.logger = logger
		self.out_handler = ctypes.windll.kernel32.GetStdHandle(-11)
		self.black = 0xf0
		self.red = 0xfc
		self.dark_yellow = 0xf6
		self.green = 0xfa
	def set_color(self,color) :
		ctypes.windll.kernel32.SetConsoleTextAttribute(self.out_handler,color)

	def reset(self) :
		self.set_color(0xf0)


	def info(self,message) :
		self.set_color(self.green)
		self.logger.info(message)
		self.reset()

	def warning(self,message) :
		self.set_color(self.dark_yellow)
		self.logger.warning(message)
		self.reset()

	def error(self,message) :
		self.set_color(self.red)
		self.logger.error(message)
		self.reset()


logging.config.fileConfig('stan.conf')
f_log = logging.getLogger('file')
s_log = stan_log(logging.getLogger('screen'))



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
		ip = show_ip()
		f_log.info('waiting for connect in '+ip+':%s ,use CTR-C stop server'%self.port)
		s_log.info('waiting for connect in '+ip+':%s ,use CTR-C stop server'%self.port)
		#print('waiting for connect in port : ',self.port,' ,use CTR-C stop server')
		try :
			while self.life :
				self.client,self.cli_addrs = self.server.accept()
				f_log.info('got connect from %s:%s'%(self.cli_addrs[0],self.cli_addrs[1]))
				s_log.info('got connect from %s:%s'%(self.cli_addrs[0],self.cli_addrs[1]))
				#print("got on connect")
				self.handle_request()
			f_log.warning('going to stop......')
			s_log.warning('going to stop......')
			#print('going stop.....')
			self.server.close()
		except Exception :
			f_log.error('something wrong,sever going to close......')
			s_log.error('something wrong,sever going to close......')
			#print('something happen,sever going to close....')
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
		if self.env['method'] == 'GET' :
			self.rfile.close() #我在这里卡了四小时
		self.response_body = self.wsgi(self.env,self.response)
		#print("trying to send")
		#print(self.response_body[:20])
		if self.response_body == 1 :
			f_log.warning("can't handle this request, so give you nothing")
			s_log.warning("can't handle this request, so give you nothing")
			self.response_body = b''
			self.send_close()
		else :
			#print('wtf')
			self.send_close()
	def get_requestline(self) :
		self.raw_requestline = self.rfile.readline(65537)
		if len(self.raw_requestline) > 65536 :
			f_log.error('request line too long , recive fail , going to close......')
			s_log.error('request line too long , recive fail , going to close......')			
			#print("request line too long , recive fail , going to close......")
			self.client.close()
			self.server.close()
		else :
			self.parse_request_line()



	def get_headers(self) :
		self.headers = http.client.parse_headers(self.rfile,_class=http.client.HTTPMessage)
		#print('type(self.headers)')
		for i in self.headers :
			self.env[i] = self.headers.get(i,'')

		

	def parse_request_line(self) :

		requestline = self.raw_requestline.decode('utf-8')
		requestline = requestline.rstrip('\r\n')
		self.request_line = requestline
		f_log.info(self.request_line)
		s_log.info(self.request_line)
		words = self.request_line.split()
		if len(words)==3 :
		
			command,path,version = words
			self.env['method'] = command
			self.env['path'] = path
			self.env['version'] = version
			
		else :
			f_log.error('sorry , len(request line) not equal to 3 , can not parse......')
			s_log.error('sorry , len(request line) not equal to 3 , can not parse......')
			#print('sorry , I do not accept not len(request line)==3')

		
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
					h1 += '\r\n'
			#print(h1)
			res += bytes(h1,'utf-8')
			res += b'\r\n'
			res += self.response_body
			#print('begin send')
			self.client.sendall(res)
			#self.life -= 1
		finally :
			self.client.close()
			f_log.info('reponse done......')
			s_log.info('reponse done......')
			
			#if self.life < 1 :
			#	self.server.close()

def make_server(host,port,application) :
	serve = Server(host,port)
	serve.set_app(application)
	return serve

	
	