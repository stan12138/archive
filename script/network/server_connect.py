from My_server import make_server,f_log,s_log
from urllib.parse import parse_qs
import threading,signal
from io import BytesIO



__all__ = ['Application']

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
		'''
		print(' ')
		for i in environ.keys() :
			print(i,end=' ')
			print(environ[i])
		print(' ')
		print(' ')
		'''
		#print(self.get_handle_func)
		if 'Accept' in environ.keys() :
			typ = environ['Accept'].split(',')
			typ = typ[0]
		else :
			typ = ''
		path = environ['path']
		if environ['method'] == 'GET' :
			
			#print('client want ',typ)
			#print('first',help(start_response))
			
			if typ=='text/html' :
				body_head = self.handle_html(path)
				if len(body_head) == 2 :
					body = body_head[0]
					head = body_head[1]
				else :
					body = body_head
					head = ''
				if head and 'Content-Type' in head.keys() :
					start_response('200 OK', [('Content-Type', head['Content-Type']),('Content-Length',str(len(body)))])
				else :
					#print('ready going to html_handle function')
					start_response('200 OK', [('Content-Type', typ),('Content-Length',str(len(body)))])
				return body
			else :
				if path in self.get_handle_func.keys():
					body_head = self.get_handle_func[path]()
					#print("here")
				else :
					path = path[1:]  #为了把最前面肯定会带的/字符去掉，呃似乎没必要
					#print('GOING TO AUTO HANDLE')
					body_head = self.auto_handle(path)
				if body_head == 1 :
					body = 1
					head = ''
				elif len(body_head) == 2 :
					body = body_head[0]
					head = body_head[1]
				else :
					body = body_head
					head = ''

				if head and 'Content-Type' in head.keys() and not body==1 :
					start_response('200 OK', [('Content-Type', head['Content-Type']),('Content-Length',str(len(body)))])
				else :
					if path[-3:] in ['css','.js'] :
						start_response('200 OK', [('Content-Type', typ),('Content-Length',str(len(body)))])
					elif path[-3:] in ['jpg','JPG'] :
						start_response('200 OK', [('Content-Type', 'image/jpeg'),('Content-Length',str(len(body)))])
					elif path[-3:] in ['png','PNG'] :
						start_response('200 OK', [('Content-Type', 'image/png'),('Content-Length',str(len(body)))])
					else :
						start_response('200 OK', [('Content-Type', '')])
				return body
		elif environ['method'] == 'POST' :
			try :
				po = environ['wsgi.input'].read(int(environ['Content-Length']))
				#print("Hi stan ,going to handle.......")
				environ['wsgi.input'].close()  #我在这里卡了四小时
				self.environ = environ
				self.form = {}
				#print("Hi stan ,going to handle.......")
				self.handle_form(po)
				body_head = self.handle_post(self.form,path)
				if len(body_head) == 2 :
					body = body_head[0]
					head = body_head[1]
				else :
					body = body_head
					head = ''
				if head and ('Content-Type' in head.keys()) :
					start_response('200 OK', [('Content-Type', head['Content-Type']),('Content-Length',str(len(body)))])
				else :
					start_response('200 OK', [('Content-Type', typ),('Content-Length',str(len(body)))])

				return body
			
			except Exception :
				f_log.error("erro when try to handle post,going to close......")
				s_log.error("erro when try to handle post,going to close......")
				#print('Got nothing.....')
				self.ser.close()
	
	def auto_handle(self,path) :
		
		if path[-3:] in ['css','.js','JPG','jpg','png','PNG'] :
			try :
				with open(path,'rb') as fi :
					rep = fi.read()
				#print('read done')
				return rep
			except Exception :
				f_log.warning("don't support this path : "+path)
				s_log.warning("don't support this path : "+path)
				#print("don't support this path ",path)
				return 1				#暂时决定，这样处理，如果改了这里，也一定要修改server里面的handle_request
		else :
			f_log.warning("don't support this path : "+path)
			s_log.warning("don't support this path : "+path)
			#print("don't support this path ",path)
			return 1

	def handle_html(self,path) :
		#print('handleing.......')
		if path in self.get_handle_func.keys():
			return self.get_handle_func[path]()
		else :
			return self.handle_error()

	def handle_post(self,form,path) :
		if path in self.post_handle_func.keys() :
			return self.post_handle_func[path](form)

		else :
			return self.handle_error()

	def handle_error(self) :
		with open("static_file/wrong.html",'rb') as fi :
			rep = fi.read()
		return rep

	def handle_form(self,po) :
		#print("wtf")
		#print(self.environ)
		form_type = self.environ['Content-Type']
		#print("Hi stan ,get form type.......",form_type)
		if form_type == 'application/x-www-form-urlencoded' :
			po = parse_qs(po)
			for i in po.keys() :
				self.form[i.decode('utf-8')] = po[i]

		elif form_type == 'text/plain' :
			f_log.error('can not handle this type form , sorry......')
			s_log.error('can not handle this type form , sorry......')
			#print("can not handle this type form , sorry")

		else :
			#print("Hi stan ,find multipart.......")
			form_type = form_type.split("; ")
			if len(form_type)==2 and form_type[0]=='multipart/form-data' :
				boundary = form_type[1].split('=')
				if len(boundary) == 2 and boundary[0]=='boundary' :
					boundary = boundary[1]
					#print("Hi,stan,I come to here.....")
					self.form = self.handle_multipart(boundary,po)

	def handle_multipart(self,boundary,po) :
		#print(po)
		#print(boundary)
		bound = b'--' + boundary.encode()
		#print(po)
		fi = BytesIO(po)
		oneline = fi.readline()
		form = {}
		file_num = -1
		#print("Hi,stan,I come to here.....")
		if bound in oneline and bound==oneline.rstrip(b'\r\n'):
			while True :
				headers = b''
				while True :
					new = fi.readline()
					if new==b'\r\n' :
						break
					headers += new.replace(b'\r\n',b'; ')
				content = b''
				while True :
					new = fi.readline()
					if bound in new :
						break
					content += new
				headers = headers.split(b'; ')
				form['name'] = 'xxxstanxxx'
				for i in headers :
					if b': ' in i :
						c = i.split(b': ')
						form[c[0].decode('utf-8')] = c[1]
					elif b'=' in i :
						c = i.split(b'=')
						if c[0].decode('utf-8')=='filename' :
							form[form['name']+'.filename'] = c[1].replace(b'"',b'')
						elif c[0].decode('utf-8') == 'name' :
							form['name'] = c[1].replace(b'"',b'').decode('utf-8')
						else :
							form[c[0].decode('utf-8')] = c[1].replace(b'"',b'')
					if 'xxxstanxxx' in form.keys() :
						form[form['name']+'.filename'] = form['xxxstanxxx']
						del form['xxxstanxxx']
				form[form['name']+'.content'] = content
				file_num += 1
				if new.rstrip(b'\r\n') == bound :
					continue
				elif new.rstrip(b'\r\n') == bound + b'--' :
					break
		f_log.info('recive and parse %s files'%file_num)
		s_log.info('recive and parse %s files'%file_num)
		return form
	def close(self) :
		self.ser.server.close()

	def signal_handler(self,a,b) :
		self.stop = True
		f_log.warning('get stop signal......')
		s_log.warning('get stop signal......')
		#print('get stop signal')

	def run(self,host='',port=8000) :
		signal.signal(signal.SIGINT, self.signal_handler)

		s = threading.Thread(target=self.run_main, args=(host,port))
		s.setDaemon(True)
		s.start()

		while not self.stop :
			pass

		self.close()
		f_log.warning('already close......')
		s_log.warning('already close......')
		#print('already close')		



