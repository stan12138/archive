from server_connect import Application

ap = Application()

@ap.set_url('/')
def index() :
	with open("static_file/first.html",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep

ap.run(port=8001)