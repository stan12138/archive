import ui
import threading
import socket
import sys
import os
import appex
import configparser

from filer_ui import UI,have_to_close
from filer_ip import IP_Handler
from filer_server import CommunicateServer


class Manager :
	def __init__(self) :

		self.all_devices = []

		self.get_partner = False

		self.show_lock = threading.Lock()
		self.close_event = threading.Event()
		self.close_event.clear()
		self.ui = UI(self.close_event)
		cf = configparser.ConfigParser()
		cf.read('filer.conf')
		server_ip = cf.get('ip-server','ip')
		server_port = cf.getint('ip-server','port')
		
		self.ui.device_source.set_call(self.get_device)

		self.partner_address = ""

		self.communicater = CommunicateServer(self.ui.window, self.get_device, self.ui.message_box, self.ui.send, self.ui.process, self.ui.get_process)

		self.ip_handler = IP_Handler((server_ip,server_port),self.communicater.port)
		self.ip_handler.set_update_ui_caller(self.special_device_handler) #因为要查询设备端口，所以我只能截断原本的联系


		if appex.is_running_extension() :
			self.ui.set_file_button_caller(self.communicater.set_send)
		else :
			self.ui.file_source.set_call(self.communicater.set_send)
		
	def shutdown(self) :
		
		self.ip_handler.off_line()
		self.communicater.shutdown()

	def run(self) :

		ui_thread = threading.Thread(target=self.ui.run, daemon=True)
		ip_thread = threading.Thread(target=self.ip_handler.run, daemon=True)
		server_thread = threading.Thread(target=self.communicater.server_run, daemon=True)

		ui_thread.start()
		ip_thread.start()
		server_thread.start()
		#print('ip handler runing')

		while not self.partner_address :
			pass

		self.ip_handler.off_line()
		self.ui.show(2)
		#print('partner address:',self.communicater.partner_address)
		cilent_thread = threading.Thread(target=self.communicater.client_run, daemon=True)
		cilent_thread.start()
		
		self.close_event.wait()
		#print('recv stop signal')
		self.shutdown()
	
	def get_device(self,address) :
		ip = address[0]
		for device in self.all_devices :
			if ip == device[1] :
				self.partner_address = (device[1],device[2])
				break
		self.communicater.set_partner(self.partner_address)

	def special_device_handler(self,devices) :
		x = [self.all_devices.append(d) for d in  [i for i in devices if not i in self.all_devices]]
		#print(self.all_devices)
		#print('ready to set ui device')
		self.ui.device_source.set_device(devices)
		#print('ui device update done')

if __name__ == '__main__':
	mama = Manager()
	mama.run()
