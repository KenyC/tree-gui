# APP IMPORTS
from cst import *
from utils import *
from popup import PopupImport

# KIVY IMPORTS
import kivy
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.properties import BooleanProperty

# Middle mouse scrolls zooms in
class ZoomManager:

	def __init__(self, treeDisplay):
		self.td = treeDisplay
		self.td.bind(on_touch_down = lambda *args: self.effect(args[1]))

	def effect(self, touch):
		if self.td.collide_point(*touch.pos):
			# Scrolling zooms in
			if touch.is_mouse_scrolling:
				self.td.zoom(1. if touch.button == "scrollup" else -1.)
				self.td.displayChange = not self.td.displayChange
				return True

# Middle mouse click pans display
class PanManager:

	def __init__(self, treeDisplay):
		self.td = treeDisplay
		self.td.bind(on_touch_down = lambda *args: self.down(args[1]))
		self.td.bind(on_touch_move = lambda *args: self.move(args[1]))

	def down(self, touch):
		# Middle button to grab
		# Saves initial position of touch and initial center of canvas in absolute coordinates
		if "button" in touch.profile and touch.button == "middle":
			touch.ud["posInit"] = touch.pos
			touch.ud["initPos"] = self.td.absX, self.td.absY
			return True

	def move(self, touch):
		if "button" in touch.profile and touch.button == "middle":
			# Compute the displacement vector between original position of touch and current position of touch in absolute coordinates
			displacement = self.td.toAbsS(touch.ud["posInit"][0] - touch.pos[0], touch.ud["posInit"][1] - touch.pos[1])
			# Add displacement vector to initial position of canvas center
			# So that the point where the middle mouse click was initiated is exactly where the mouse currently is
			self.td.absCenter = touch.ud["initPos"][0] + displacement[0], touch.ud["initPos"][1] + displacement[1]
			# Refresh display
			self.td.displayChange = not self.td.displayChange

# Left click adds node ; right click removes node
class AddRemoveNodeManager:

	def __init__(self, treeDisplay, tree, deadkey):
		self.tree = tree
		self.td = treeDisplay
		self.dk = deadkey
		self.td.bind(on_touch_down = lambda *args: self.effect(args[1]))

	def effect(self, touch):
		# If a left or right click, we check whether the event occurs in the vicinity of a node
		# The notion of vicinity is scaled for zooming
		for i, p in enumerate(self.tree.positions):
			if dist(self.td.toLocal(*p), touch.pos) < SPROUT_DIST / self.td.scale:
				if "button" in touch.profile and touch.button == "left" and not self.dk.ctrl:
					self.tree.sprout(i)
					self.td.treeChange = not self.td.treeChange
					return True
				elif "button" in touch.profile and touch.button == "right":
					self.tree.delete(i)
					self.td.treeChange = not self.td.treeChange
					return True

# Ctrl + Left click on node positions cursor in text where label is.
class ChangeLabelManager:

	def __init__(self, treeDisplay, treeLabel,  deadkey, tree):
		self.tree = tree
		self.td = treeDisplay
		self.tl = treeLabel
		self.dk = deadkey

		self.td.bind(on_touch_up = lambda *args: self.effect(args[1]))

	def effect(self, touch):
		if self.dk.ctrl:
			for i, p in enumerate(self.tree.positions):
				if dist(self.td.toLocal(*p), touch.pos) < SPROUT_DIST / self.td.scale:
						if "button" in touch.profile and touch.button == "left":
							self.tl.ctrlTap(i)



class DeadKeyManager:

	def __init__(self):
		self.ctrl = False
		self.alt = False
		Window.bind(on_key_down = lambda *args: self.setCtrl(args[1], True))
		Window.bind(on_key_up = lambda *args: self.setCtrl(args[1], False))

	def setCtrl(self, keycode, value):
		if keycode == 305: # CTRL is 305
			self.ctrl = value
		elif keycode == 308: # ALT is 308
			self.alt = value
	

class ImportTreeManager:

	def __init__(self, tree, treeDisplay, treeInput):
		self.tree = tree
		self.display = treeDisplay
		self.input = treeInput

	def createPopUp(self):
		self.popup = PopupImport(self)
		self.popup.open()
		
		def setText():
			self.popup.textInput.text = Clipboard.paste()
			print("fezf", Clipboard.paste())
			self.popup.textInput.focus = True
			self.popup.textInput.select_all()

		Clock.schedule_once(lambda dt: setText(),0.2)
	
	def importTree(self, treeString):
		t = self.input.transd.parse(treeString)
		if t is not None:
			self.tree.set(t)
			self.display.treeChange = not self.display.treeChange
			return True
		else:
			return False