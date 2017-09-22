from server_connect import Application



ap = Application()

@ap.set_url('/')
def index() :
	with open("static_file/testpage.html",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep

@ap.set_url('/static_file/stan.JPG')
def second() :
	with open("stan.conf",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep,{'Content-Type':'text/plain'}

@ap.set_url('/give.py')
def third() :
	with open("My_server.py",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep,{'Content-Type':'text/x-script.phyton'}

@ap.set_url('/',method='POST')
def get_text(form) :
	#print('come here........')
	if 'user' in form.keys() :
		print(form['user'])
	if 'stan' in form.keys() :
		print(form['stan'])
	'''
	with open(form['user.filename'].decode('utf-8'),'wb') as fi :
		fi.write(form['user.content'])
	with open(form['stan.filename'].decode('utf-8'),'wb') as fi :
		fi.write(form['stan.content'])
	'''	
	with open('static_file/homepage.html','rb') as fi :
		rep = fi.read()

	return rep,{'Content-Type':'text/html'}
#print("my ip is :", ip)
ap.run(port=8000)