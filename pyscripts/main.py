#########################################
#									   #
#			   Magpie				  #
#				v0.1				   #
#									   #
#	   written by Otavio Cals		  #
#									   #
#	Description: A distance-based	  #
#	alarm clock built using the Google #
#	Maps API for geo-localizatoin.	 #
#									   #
#########################################

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.garden.mapview import MapView, MapMarker
from os.path import join, isdir, expanduser, isfile
from sys import platform
import sys
import os
import webbrowser



######################
#	Pre-Settings	#
######################

#Setting configurations

Config.set("kivy","log_enable","1")
Config.set("kivy","log_level","info")
Config.set("graphics","position","custom")
Config.set("graphics","top","50")
Config.set("graphics","left","10")
Config.set("graphics","width","700")
Config.set("graphics","height","600")
Config.set("graphics","fullscreen","0")
Config.set("graphics","borderless","0")
Config.set("graphics","resizable","1")
Config.write()

current_os = platform


#DLL for Windows
try:
	import win32api
	win32api.SetDllDirectory(sys._MEIPASS)
except:
	pass
		
	
#System specific configs
if current_os.startswith("win32") or current_os.startswith("cygwin"):
	slash = "\\"
else:
	slash = "/"
	
#Relative resources path
def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path,relative_path)
	
#Files path
logo_path = resource_path("resources"+slash+"logo.png")
kivi_app_path = resource_path("kivy"+slash+"app_screen.kv")
config_cloud_path = resource_path("conf"+slash+"cloud.conf")
version_num="0.1"

#Building GUI

Builder.load_file(kivi_app_path)	

######################
#	App Functions   #
######################

class AppScreen(GridLayout):

	default_folder = expanduser("~") + slash + "Documents"
	global sel_folder
	sel_folder = default_folder
	
	
#Setting window layout

	def __init__(self,**kwargs):
		super(AppScreen, self).__init__(**kwargs)

		Window.size = (600,900)
		Window.set_title("Magpie")


		self.cols = 1
		self.size_hint = (None,None)
		self.width = 600
		self.height = 900
		self.icon = logo_path
		self.ids.ce_logo.source = logo_path
		
#GUI functions

	def start(self,*args):
		global event
		if args[1] == "down":
			self.ids.check_button.disabled = True
			self.ids.folder_button.disabled = True
			event = Clock.schedule_once(self.scrap)
		if args[1] == "normal":
			self.ids.check_button.disabled = False
			self.ids.folder_button.disabled = False
			Clock.unschedule(event)

	def update_button(self,event):
		self.ToggleButton.text="Stop"

	def _open_link(self):
		webbrowser.open("http://www.calsemporium.com")
		
#Directory selection

	def _filepopup_callback(self, instance):
			if instance.is_canceled():
				return
			s = 'Path: %s' % instance.path
			s += ('\nSelection: %s' % instance.selection)
			global sel_folder
			self.ids.text_input.text = "Pasta selecionada:	" + instance.path
			sel_folder = instance.path

	def _folder_dialog(self):
		XFolder(on_dismiss=self._filepopup_callback, path=expanduser(u'~'))
		
#Map Functions

		

######################
#	Starting App	#
######################


class MAGPIE(App):

	def build(self):
		self.icon = logo_path
		self.resizable = 1
		self.title = "Magpie v"+version_num
		self.log_enable = 1
		return AppScreen()

		

######################
#		Main		#
######################

if __name__ == "__main__" :
	MAGPIE().run()