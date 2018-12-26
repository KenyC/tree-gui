# APP IMPORTS
from tree import Tree
from cst import *
from transducer import *
from events import *
import re

# KIVY IMPORTS
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

import kivy

from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, BooleanProperty
from kivy.core.text import Label as CoreLabel
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window, Keyboard
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock



# MAIN CODE

# Construction of the default tree
main = Tree()
main.sprout(0)
main.sprout(2)
main.sprout(4)
main.sprout(6)




# Left widget: displays tree in Canvas
class TreeDisplay(Widget):
	# Fires event when structural changes were made to the tree
	treeChange = BooleanProperty(False)
	# Fires event when changes to the display need to be made
	displayChange = BooleanProperty(False)
	ctrlHeld = BooleanProperty(False)
	altHeld = BooleanProperty(False)

	nodeClick = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(TreeDisplay, self).__init__(**kwargs)



		# Position of canvas center in absolute coordinates
		self.absCenter = 0, 0 
		# Zoom level
		self.scale = 0.5

		# Compute position of nodes in tree in absolute coordinates if root is at POS_ABS_ROOT in absolute coordinates
		main.construct(POS_ABS_ROOT)

		# 1s after start, display Tree (why is this needed for proper drawing?)
		Clock.schedule_once(lambda dt: self.drawTree(main), 60./60.)

	# def setCtrl(self, keycode, value):
	# 	if keycode == 305: # CTRL is 305
	# 		self.ctrlHeld = value
	# 	elif keycode == 308: # ALT is 308
	# 		self.altHeld = value

	# Convenience aliases
	@property
	def absX(self):
		return self.absCenter[0]

	@property
	def absY(self):
		return self.absCenter[1]
	
	# Transform point and vector from absolute coordinates to canvas coordinates in vice-versa
	def toLocal(self, x, y):
		return ((1. / self.scale) * (x - self.absX) + self.center[0],
				 (1. / self.scale) * (y - self.absY) + self.center[1])

	# vectors only
	def toLocalS(self, x, y):
		return ((1. / self.scale) * x,
				 (1. / self.scale) * y)

	def toAbs(self, x, y):
		return ((self.scale) * (x - self.center[0]) + self.absX,
				 (self.scale) * (y - self.center[1]) + self.absY)

	# vectors only
	def toAbsS(self, x, y):
		return ((self.scale) * x,
				 (self.scale) * y)

	# Redraws tree
	def drawTree(self, tree): 
		self.canvas.clear()

		defaults = {"radiusPts": 10., "thickLines": 2, "colorDots" : (1,0,0), "fontSize": 10, "colorText": (0, 1, 0)}

		# Convert node positions in canvas coordinates
		lPos = [self.toLocal(*p) for p in tree.positions]


		with self.canvas:
			# Display lines first
			for i in range(tree.n):
				if tree.children[i]:
					for c in tree.children[i]:
						Line(points = (lPos[i][0], lPos[i][1], lPos[c][0], lPos[c][1]),
													width = defaults["thickLines"])
		
			Color(*defaults["colorDots"])
			
			# Display nodes	
			r = defaults["radiusPts"]
			for p in lPos:
				Ellipse(pos = (p[0] - r/2., p[1] - r/2.), size = (r, r))

			Color(*defaults["colorText"])

		# Display labels
		for i in range(tree.n):
			l = CoreLabel(text = tree.labels[i], font_size = defaults["fontSize"])
			l.refresh()
			self.canvas.add(Rectangle(size = l.texture.size, pos = lPos[i], texture = l.texture))




	
	# Event handler when structural modifications have been made to the tree
	def on_treeChange(self, instance, pos):
		main.construct(POS_ABS_ROOT)
		self.displayChange = not self.displayChange

	# When Display needs refreshing
	def on_displayChange(self, instance, pos):
		self.drawTree(main)

	def zoom(self, value):
		self.scale *= EXPONENT**(value)

	def clearLabels(self):
		main.labels = ["" for i in range(main.n)]
		self.displayChange = not self.displayChange
		self.nodeClick.updateTree()


# Right widget : displays the tree in string format and allows input of labels
class TreeInput(TextInput):

	def __init__(self, **kwargs):
		super(TreeInput, self).__init__(**kwargs)
		# Refresh string display
		self.updateTree()

		# Enter does not defocus widget
		# This is not working but may in other versions of kivy
		self.text_validate_unfocus = False


	def updateTree(self):
		# Get RegExp associated with tree
		# This is an expression that matches any string that represents a tree identical to `main`, except possibly for the labels
		self.pat = DEFAULT_TRANSDUCER.regExp(main)
		# This is the actual string representation of the tree
		self.text = DEFAULT_TRANSDUCER.toStr(main) 

	# Disallow modification of the structure of the tree in the text input
	def insert_text(self, substring, from_undo = False):
		# What comes before and after the inserted text
		before = self.text[:self.cursor_index()]
		after = self.text[self.cursor_index():]

		# If change results in modifying tree structure, cancel
		s = "" if self.pat.match(before + substring + after) is None else substring
		return super(TreeInput, self).insert_text(s, from_undo=from_undo)

	# When text changes, modify the labels accordingly
	# Structure is not allowed to change
	def on_text(self, instance, text):
		# use reg exp to recover labels
		m = self.pat.match(self.text)


		if m is not None:
			groups = m.groups()
			# Labels are obtained from the regexp in the linear order in which they are displayed
			# This may not be the order in which they are stored
			# We compute a table that matches linear order position to stored position
			inds = DEFAULT_TRANSDUCER.indicesOrder(main)

			# Modify the labels
			for i, g in enumerate(groups):
				main.labels[inds[i]] = g
		

	def ctrlTap(self, idx):
		Clock.schedule_once(lambda dt: self.setSelect(**DEFAULT_TRANSDUCER.find(main, idx)))

	def setSelect(self, start, end):
		self.focus = True
		self.cursor = self.get_cursor_from_index(end)
		self.select_text(start, end)

	def changeTransducer(self, transLabel):
		global DEFAULT_TRANSDUCER
		if transLabel in DICT_TRANSDUCER:
			DEFAULT_TRANSDUCER = DICT_TRANSDUCER[transLabel]
			self.updateTree()


class MainWindow(BoxLayout):
	treeDisplay = ObjectProperty(None)
	treeLabel = ObjectProperty(None)

	def __init__(self,**kwargs):
		super(MainWindow, self).__init__(**kwargs)

		self.deadkey = DeadKeyManager()
		self.zoom = ZoomManager(self.treeDisplay)
		self.pan = PanManager(self.treeDisplay)
		self.addremovenodes = AddRemoveNodeManager(self.treeDisplay, main, self.deadkey)
		self.changelabel = ChangeLabelManager(self.treeDisplay, self.treeLabel, self.deadkey, main)


class TreeApp(App):

	def build(self):
		return MainWindow()


if __name__ == '__main__':
    TreeApp().run()