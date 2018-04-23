import ui
import appex
import os
import sys
#from File_transfer import have_to_close
have_to_close = False
def full_path(path):
	# Return absolute path with expanded ~s, input path assumed relative to cwd
	return os.path.abspath(os.path.join(os.getcwd(), os.path.expanduser(path)))
	
def make_new_table(path) :
	path = full_path(path)
	lst = ui.TableView()
	# allow multiple selection when editing, single selection otherwise
	lst.allows_selection = True
	lst.allows_multiple_selection = False
	lst.background_color = 1.0
	source = FileSource(path)
	lst.data_source = lst.delegate = source
	lst.name = os.path.basename(path)
	current_list = lst
	return lst,source



class ProcessBar (ui.View):
	def __init__(self):
		self.width = 208
		self.height = 28
		self.value = 0
		self.my_border_x = self.x + 2
		self.my_border_y = self.y + 2
		self.my_border_width = self.width-4
		self.my_border_height = self.height-4
		
		self.bar_x = self.my_border_x+2
		self.bar_y = self.my_border_y+2
		self.bar_height = self.my_border_height-4
		self.bar_length = self.my_border_width-4
		self.bar_width = self.value*self.bar_length/100

		self.txt = '%.2f%%'%(self.value)
		

	def draw(self):
		path_border = ui.Path.rect(self.my_border_x,self.my_border_y,self.my_border_width,self.my_border_height)
		ui.set_color('black')
		path_border.stroke()
		path_bar = ui.Path.rect(self.bar_x,self.bar_y,self.bar_width,self.bar_height)
		ui.set_color('blue')
		path_bar.fill()
		ui.draw_string(self.txt,rect=(self.my_border_x+self.my_border_width+2,self.my_border_y+3,50,self.my_border_height),alignment=ui.ALIGN_CENTER)
	
	def set_value(self, new_value) :
		self.value = new_value*100
		self.bar_width = self.value*self.bar_length/100
		self.txt = '%.2f%%'%(self.value)
		self.set_needs_display()
		



class DeviceSource :

	def __init__(self):
		self.device = []
						
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.device)
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = self.device[row][0]
		return cell

	def tableview_did_select(self, tableview, section, row):
		self.call((self.device[row][1], self.device[row][2]))
		
	def set_tableview(self,table) :
		self.table = table

	def set_call(self, call) :
		self.call = call

	def set_device(self, device):
		self.device = device
		#print(self.device)
		self.table.reload()


class FileSource(object):
	# ui.TableView data source that generates a directory listing
	def __init__(self, path=os.getcwd()):
		# init
		self.path = full_path(path)
		self.refresh()

		#self.lists = [self.folders, self.files]
		
	def refresh(self):
		# Refresh the list of files and folders
		self.folders = []
		self.files = []
		for f in os.listdir(self.path):
			if os.path.isdir(os.path.join(self.path, f)):
				self.folders.append(f)
			else:
				self.files.append(f)
		self.lists = [self.folders, self.files]	
	def tableview_number_of_sections(self, tableview):
		# Return the number of sections
		return len(self.lists)
		
	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.lists[section])
		
	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.text_label.text = os.path.basename(os.path.join(self.path, self.lists[section][row]))
		if section == 0:
			cell.accessory_type = "disclosure_indicator"
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		if section == 0:
			return "Folders"
		elif section == 1:
			return "Files"
		else:
			return ""
			
	def tableview_did_select(self, tableview, section, row):
		# Called when the user selects a row
		if section == 0:
			lst, source = make_new_table(os.path.join(self.path, self.folders[row]))
			source.set_nav(self.nav)
			source.set_call(self.call)
			self.nav.push_view(lst)
		elif section == 1 :
			self.call("file",full_path(os.path.join(self.path, self.files[row])))

	def set_nav(self, nav) :
		self.nav = nav
	
	def set_call(self, call) :
		self.call = call



class MyView (ui.View):
	def __init__(self) :
		pass
		#self.have_to_close = False
	def will_close(self):
		#print('ui going to close')
		self.event.set()

	def set_close(self, event) :
		self.event = event

class UI :
	def __init__(self,close_event) :
		if appex.is_running_extension() :
			self.file_path = appex.get_file_path()
			self.v = ui.load_view("inner_ui")
			#self.have_to_close = self.v.have_to_close
			self.v.set_close(close_event)
			self.window = self.v['show']
			self.message_box = self.v['message_box']
			self.message_label = self.v["message_label"]
			self.send = self.v['send']
			
			self.device_source = DeviceSource()
			self.device_label = self.v["device_label"]
			self.device_table = self.v["device_table"]
			self.device_table.data_source = self.device_table.delegate = self.device_source

			self.device_source.set_tableview(self.device_table)

			self.process = self.v['bar']

			self.get_process = self.v["bar"]

			self.file_button = self.v['file_button']
			self.file_button.action = self.file_button_action

			self.start_page = [self.device_label, self.device_table]
			self.second_page = [self.window, self.message_box, self.message_label, self.send, self.file_button, self.process, self.get_process]

			self.show(1)



		else :
			self.v = ui.load_view("File_transfer")
			#print(type(close_event))
			self.v.set_close(close_event)
			self.window = self.v['show']

			self.message_box = self.v['message_box']
			self.message_label = self.v["message_label"]
			self.send = self.v['send']
			
			self.device_source = DeviceSource()
			self.device_label = self.v["device_label"]
			self.device_table = self.v["device_table"]
			self.device_table.data_source = self.device_table.delegate = self.device_source

			self.device_source.set_tableview(self.device_table)

			self.file_label = self.v["file_label"]
			self.process = self.v['bar']

			self.get_process = self.v["bar"]

			lst, source = make_new_table("~")
			self.file_nav = ui.NavigationView(lst)
			self.file_source = source
			source.set_nav(self.file_nav)
			self.file_nav.x = 390
			self.file_nav.y = 265
			self.file_nav.width = 361
			self.file_nav.height = 331
			self.file_nav.border_color = '#f0f0f0'
			self.file_nav.border_width = 1
			self.v.add_subview(self.file_nav)

			self.start_page = [self.device_label, self.device_table]
			self.second_page = [self.window, self.message_box, self.message_label, self.send, self.file_label, self.file_nav, self.process, self.get_process]

			self.show(1)
		
	def show(self, page) :
		if page==1 :
			for i in self.start_page :
				
				i.hidden = False
			for i in self.second_page :
				#print(type(i),dir(i))
				i.hidden = True
			#print('show 1 work')
		else :
			for i in self.start_page :
				i.hidden = True
			for i in self.second_page :
				i.hidden = False	

	def run(self) :
		self.v.present('fullscreen')

	def file_button_action(self,sender) :
		if self.file_path :
			self.file_button_call("file", self.file_path)
		else :
			print("there is no file path")
	def set_file_button_caller(self, call) :
		self.file_button_call = call
