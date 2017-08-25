from My_server import make_server
from urllib.parse import parse_qs
import threading,signal


class Application :
	def __init__(self) :
		self.get_handle_func = {}
		self.post_handle_func = {}
		self.stop = False
	def set_url(self,url,method='GET') :
		def second(func) :
			if method=='GET' :
				self.get_handle_func[url] = func
			elif method=='POST' :
				self.post_handle_func[url] = func
			return func
		return second
	def run_main(self,host='',port=8000) :
		self.ser = make_server(host,port,self.application)
		try :
			#print('ready for run in port: ',port)
			self.ser.run()
		except Exception :
			self.close()
	def application(self,environ,start_response) :
		print(' ')
		for i in environ.keys() :
			print(i,end=' ')
			print(environ[i])
		print(' ')
		print(' ')
		#print(self.get_handle_func)
		typ = environ['Accept'].split(',')
		typ = typ[0]
		path = environ['path']
		if environ['method'] == 'GET' :
			
			#print('client want ',typ)
			#print('first',help(start_response))
			start_response('200 OK', [('Content-Type', typ)])
			if typ=='text/html' :
				#print('ready going to html_handle function')
				return self.handle_html(path)
			else :
				path = path[1:]
				return self.auto_handle(path)
		elif environ['method'] == 'POST' :
			try :
				start_response('200 OK', [('Content-Type', typ)])
				po = environ['wsgi.input'].read(int(environ['Content-Length']))
				print(po)
				po = parse_qs(po)

				return self.handle_post(po,path)
			
			except Exception :
				print('Got nothing.....')
				self.ser.close()
	
	def auto_handle(self,path) :
		p = path.split('.')
		if p[-1]=='css' or p[-1]=='js' :
			with open(path,'rb') as fi :
				rep = fi.read()
			return rep
		else :
			return b'no'
		
	def handle_html(self,path) :
		#print('handleing.......')
		if path in self.get_handle_func.keys():
			return self.get_handle_func[path]()
		else :
			return self.handle_error()

	def handle_post(self,po,path) :
		if path in self.post_handle_func.keys() :
			return self.post_handle_func[path](po)

		else :
			return self.handle_error()

	def handle_error(self) :
		with open("static_file/wrong.html",'rb') as fi :
			rep = fi.read()
		return rep

	def close(self) :
		self.ser.server.close()

	def signal_handler(self,a,b) :
		self.stop = True
		print('get stop signal')

	def run(self,host='',port=8000) :
		signal.signal(signal.SIGINT, self.signal_handler)

		s = threading.Thread(target=self.run_main, args=(host,port))
		s.setDaemon(True)
		s.start()

		while not self.stop :
			pass

		self.close()

		print('already close')		



