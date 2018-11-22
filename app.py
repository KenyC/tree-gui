# APP IMPORTS
from tree import Tree
from transducer import QTreeTrans
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
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock


main = Tree()
main.sprout(0)
main.sprout(1)
main.sprout(2)
main.sprout(4)
main.sprout(6)

DEFAULT_TRANSDUCER = QTreeTrans
SPROUT_DIST = 20.
POS_ABS_ROOT = (0, 80)
EXPONENT = 1.1

rectAbsCoord = 50, 50, 30, 40

# HELPER FUNCTIONS
def dist(p1, p2):
	return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5




class TreeDisplay(Widget):
	treeChange = BooleanProperty(False)
	displayChange = BooleanProperty(False)

	def __init__(self, **kwargs):
		super(TreeDisplay, self).__init__(**kwargs)

		self.absCenter = self.absX, self.absY = 0, 0 # Position of center in absolute coordinates
		self.scale = 0.5

		self.testPos = (0,50)
		self.testSize = (100,100)

		main.construct(POS_ABS_ROOT)

		#self.bind(treeChange = lambda instance, pos: main.construct(POS_ABS_ROOT))

		#self.drawTree((self.xRoot, self.yRoot), main)
		Clock.schedule_once(lambda dt: self.drawTree(main), 60./60.)
		# self.drawStg()


		# with self.canvas:
		# 	Color(1, 1, 0)
		# 	d = 250
		# 	Ellipse(pos=self.center, size=(d, d))
		# 	Rectangle(size = self.size, pos = (0,0))

	def toLocal(self, x, y):
		return ((1. / self.scale) * (x - self.absX) + self.center[0],
				 (1. / self.scale) * (y - self.absY) + self.center[1])

	def toLocalS(self, x, y):
		return ((1. / self.scale) * x,
				 (1. / self.scale) * y)

	def toAbs(self, x, y):
		return ((self.scale) * (x - self.center[0]) + self.absX,
				 (self.scale) * (y - self.center[1]) + self.absY)


	# Pos start is the position of the root of the tree in absolute coordinates
	def drawTree(self, tree): 
		self.canvas.clear()

		defaults = {"radiusPts": 10., "thickLines": 2, "colorDots" : (1,0,0), "fontSize": 10, "colorText": (0, 1, 0)}

		lPos = [self.toLocal(*p) for p in tree.positions]
		with self.canvas:
			# Display lines first
			for i in range(tree.n):
				if tree.children[i]:
					for c in tree.children[i]:
						Line(points = (lPos[i][0], lPos[i][1], lPos[c][0], lPos[c][1]),
													width = defaults["thickLines"])
		
			Color(*defaults["colorDots"])
			
			r = defaults["radiusPts"]
			for p in lPos:
				Ellipse(pos = (p[0] - r/2., p[1] - r/2.), size = (r, r))

			Color(*defaults["colorText"])

		for i in range(tree.n):
			l = CoreLabel(text = tree.labels[i], font_size = defaults["fontSize"])
			l.refresh()
			self.canvas.add(Rectangle(size = l.texture.size, pos = lPos[i], texture = l.texture))



	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			if touch.is_mouse_scrolling:
				self.zoom(1. if touch.button == "scrollup" else -1.)
				self.displayChange = not self.displayChange
				return True
			else:
				for i, p in enumerate(main.positions):
					if dist(self.toLocal(*p), touch.pos) < SPROUT_DIST / self.scale:
						if "button" in touch.profile and touch.button == "left":
							main.sprout(i)
							self.treeChange = not self.treeChange
							return True
						elif "button" in touch.profile and touch.button == "right":
							main.delete(i)
							self.treeChange = not self.treeChange
							return True
	
	def on_treeChange(self, instance, pos):
		main.construct(POS_ABS_ROOT)
		self.displayChange = not self.displayChange

	def on_displayChange(self, instance, pos):
		self.drawTree(main)

	def zoom(self, value):
		self.scale *= EXPONENT**(value)

class TreeInput(TextInput):
	def __init__(self, **kwargs):
		super(TreeInput, self).__init__(**kwargs)
		self.updateTree()
		self.text_validate_unfocus = False

	def updateTree(self):
		self.pat = DEFAULT_TRANSDUCER.regExp(main)
		self.text = DEFAULT_TRANSDUCER.toStr(main) 

	def insert_text(self, substring, from_undo = False):
		before = self.text[:self.cursor_index()]
		after = self.text[self.cursor_index():]

		s = "" if self.pat.match(before + substring + after) is None else substring
		return super(TreeInput, self).insert_text(s, from_undo=from_undo)

	def on_text(self, instance, text):
		m = self.pat.match(self.text)

		if m is not None:
			groups = m.groups()
			inds = main.indicesOrder()

			for i, g in enumerate(groups):
				main.labels[inds[i]] = g



class MainWindow(BoxLayout):
	pass

class TreeApp(App):

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    TreeApp().run()