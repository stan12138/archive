import ui
import threading
import socket
import sys
import os
import appex

from filer_ui import UI,have_to_close
from filer_ip import IP_Handler
from filer_server import CommunicateServer


class Manager :
	def __init__(self) :

		self.get_partner = False

		self.show_lock = threading.Lock()

		self.ui = UI()
		
		self.ip_handler = IP_Handler(('10.112.101.153',6000))
		self.ip_handler.set_update_ui_caller(self.ui.device_source.set_device)
		self.ui.device_source.set_call(self.get_device)

		self.partner_address = ""

		self.communicater = CommunicateServer(self.ui.window, self.get_device, self.ui.message_box, self.ui.send, self.ui.process, self.ui.get_process)
		self.ui.v.get_close(self.shutdown)
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

		while not self.partner_address :
			pass

		self.ip_handler.off_line()
		self.ui.show(2)
		#print('partner address:',self.communicater.partner_address)
		cilent_thread = threading.Thread(target=self.communicater.client_run, daemon=True)
		cilent_thread.start()
		
		while not have_to_close :
			pass
		#print('recv stop signal')
		self.shutdown()
	
	def get_device(self,address) :
		self.partner_address = address
		self.communicater.set_partner(address)

if __name__ == '__main__':
	mama = Manager()
	mama.run()
