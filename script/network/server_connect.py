from My_server import make_server
from urllib.parse import parse_qs
class Application :
	def __init__(self) :
		self.get_handle_func = {}
		self.post_handle_func = {}
	def set_url(self,url,method='GET') :
		def second(func) :
			if method=='GET' :
				self.get_handle_func[url] = func
			elif method=='POST' :
				self.post_handle_func[url] = func
			return func
		return second
	def run(self,host='',port=8000) :
		self.ser = make_server(host,port,self.application)
		try :
			#print('ready for run in port: ',port)
			self.ser.run()
		except Exception :
			self.ser.server.close()
	def application(self,environ,start_response) :
		'''print(' ')
		for i in environ.keys() :
			print(i,end=' ')
			print(environ[i])
		print(' ')
		print(' ')'''
		#print(self.get_handle_func)
		if environ['method'] == 'GET' :
			path = environ['path']
			typ = environ['Accept'].split(',')
			typ = typ[0]
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
				po = environ['wsgi.input'].read(int(environ['Content-Length']))
				print(po)
				po = parse_qs(po)
				print(po)
			except Exception :
				print('Got nothing.....')
				self.ser.close()
	
	def auto_handle(self,path) :
		p = path.split('.')
		if p[-1]=='css' :
			with open(path,'rb') as fi :
				rep = fi.read()
			return rep
		else :
			return b'no'
		
	def handle_html(self,path) :
		#print('handleing.......')
		return self.get_handle_func[path]()
