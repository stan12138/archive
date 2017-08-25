from server_connect import Application


ap = Application()

@ap.set_url('/')
def index() :
	with open("static_file/first.html",'rb') as fi :
		rep = fi.read()
	#print('got html file')
	return rep

@ap.set_url('/',method='POST')
def get_text(message) :
	print('here')
	print(message)
	with open('record.txt','wb') as fi :
		for i in message.keys() :
			fi.write(bytes(i,'utf-8'))
			fi.write(b':')
			print(message[i])
			for j in message[i] :
				fi.write(bytes(j,'utf-8'))
			fi.write(b'\r\n')
	with open('static_file/got.html','rb') as fi :
		rep = fi.read()

	return rep
ap.run(port=8000)