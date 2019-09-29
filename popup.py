from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import kivy
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock


Builder.load_file("popup.kv")


class PopupImport(Popup):
	texte = StringProperty("")
	textInput = ObjectProperty(None)

	def __init__(self, eventManager, *args, **kwargs):
		super(PopupImport, self).__init__(*args, **kwargs)
		self.em = eventManager
	# 	Clock.schedule_once(lambda dt: self.giveFocus(), 0.2)

	# def giveFocus(self):
	# 	self.textInput.focus = True
	# 	self.textInput.select_all()

	def dismiss_import(self):
		if self.em.importTree(self.texte):
			super(PopupImport, self).dismiss()