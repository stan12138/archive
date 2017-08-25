from server_connect import Application
import threading,signal

stop = False

def signal_handler(a,b) :
	global stop
	stop = True
	print('got signal')

signal.signal(signal.SIGINT, signal_handler)



ap = Application()

@ap.set_url('/')
def index() :
	with open("static_file/first.html",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep


s = threading.Thread(target=ap.run, args=('',8000))
s.setDaemon(True)
s.start()

while not stop :
	pass

ap.ser.server.close()

print('already close')