from My_server import make_server,f_log,s_log
from urllib.parse import parse_qs
import threading,signal
from io import BytesIO

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
		#print(' ')
		#for i in environ.keys() :
		#	print(i,end=' ')
		#	print(environ[i])
		#print(' ')
		#print(' ')
		#print(self.get_handle_func)
		typ = environ['Accept'].split(',')
		typ = typ[0]
		path = environ['path']
		if environ['method'] == 'GET' :
			
			#print('client want ',typ)
			#print('first',help(start_response))
			
			if typ=='text/html' :
				#print('ready going to html_handle function')
				start_response('200 OK', [('Content-Type', typ)])
				return self.handle_html(path)
			else :
				path = path[1:]
				if path[-3:] in ['css','.js'] :
					start_response('200 OK', [('Content-Type', typ)])
				elif path[-3:] in ['jpg','JPG'] :
					start_response('200 OK', [('Content-Type', 'image/jpeg')])
				elif path[-3:] in ['png','PNG'] :
					start_response('200 OK', [('Content-Type', 'image/png')])
				return self.auto_handle(path)
		elif environ['method'] == 'POST' :
			try :
				start_response('200 OK', [('Content-Type', typ)])
				po = environ['wsgi.input'].read(int(environ['Content-Length']))
				#print("Hi stan ,going to handle.......")
				#po = parse_qs(po)
				self.environ = environ
				self.form = {}
				#print("Hi stan ,going to handle.......")
				self.handle_form(po)

				return self.handle_post(self.form,path)
			
			except Exception :
				print('Got nothing.....')
				self.ser.close()
	
	def auto_handle(self,path) :
		
		if path[-3:] in ['css','.js','JPG','jpg','png','PNG'] :

			with open(path,'rb') as fi :
				rep = fi.read()
			#print('read done')
			return rep
		else :
			print("don't support this path ",path)
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
		f_log.info('get stop signal......')
		s_log.info('get stop signal......')
		#print('get stop signal')

	def run(self,host='',port=8000) :
		signal.signal(signal.SIGINT, self.signal_handler)

		s = threading.Thread(target=self.run_main, args=(host,port))
		s.setDaemon(True)
		s.start()

		while not self.stop :
			pass

		self.close()
		f_log.info('already close......')
		s_log.info('already close......')
		#print('already close')		



