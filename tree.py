# from kivy.graphics.instructions import InstructionGroup
# from kivy.graphics import Line, Ellipse

# Make sure that children always come after fathers
class Tree:

	def __init__(self, label = ""):
		self.labels = [label]
		self.children = [[]]

	def sprout(self, idx, labelL = "", labelR = ""):
		if not self.children[idx]:
			self.labels += [labelL, labelR]
			self.children[idx] += [self.n , self.n + 1]
			self.children += [[],[]]

	@property
	def n(self):
		return len(self.children)
	
	def delete(self, idx):
		# for branches in self.children:
		# 	if idx in branches:
		# 		branches.remove(idx)
		self.children[idx] = []
		self.trim()

	def accessible(self, idx = 0):
		l = [idx]
		for j in self.children[idx]:
			l.extend(self.accessible(j))

		return l


	def trim(self):
		acc = self.accessible()
		invAcc = {idx:i for i,idx in enumerate(acc)}

		newLabels = [self.labels[idx] for idx in acc]
		newChildren = [self.children[idx] for idx in acc]

		for i, cdren in enumerate(newChildren):
			newChildren[i] = [invAcc[c] for c in cdren]

		self.labels = newLabels
		self.children = newChildren

	def show(self, idx = 0, space = 0):
		print(space*" "+ str(idx) if self.labels[idx] == "" else self.labels[idx])
		for c in self.children[idx]:
			self.show(c, space + 1)

	def construct(self, pos, **params):
		defaults = {"nodeWidth": 30., "height": 50.}
		defaults.update(params)

		self.lgths = [0. for i in range(self.n)]

		for i in range(self.n - 1, -1, -1):
			if not self.children[i]:
				self.lgths[i] = defaults["nodeWidth"]
			else:
				self.lgths[i] = sum(self.lgths[c] for c in self.children[i])

		self.positions = [pos for i in range(self.n)]


		for i in range(self.n):
			if self.children[i]:
				
				leftEdge = 0.
				parentPos = self.positions[i]

				for c in self.children[i]:
					self.positions[c] = (parentPos[0] + leftEdge + self.lgths[c] / 2, parentPos[1] - defaults["height"])
					leftEdge += self.lgths[c]

				ecartPos = parentPos[0] - sum(self.positions[c][0] for c in self.children[i]) / (len(self.children[i]))

				for c in self.children[i]:
					self.positions[c] = (self.positions[c][0] + ecartPos, self.positions[c][1])
	
	def indicesOrder(self, index = 0):
		s = [index]

		for c in self.children[index]:
			s += self.indicesOrder(c)

		return s

	# def display(self, **params):
	# 	defaults = {"radiusPts": 10., "thickLines": 2, "localCoords": lambda x: x}
	# 	defaults.update(params)

	# 	self.lPos = [defaults["localCoords"](*p) for p in self.positions]
	# 	self.displayLines = InstructionGroup()
	# 	# Display lines first
	# 	for i in range(self.n):
	# 		if self.children[i]:
	# 			for c in self.children[i]:
	# 				self.displayLines.add(Line(points = (self.lPos[i][0], self.lPos[i][1], self.lPos[c][0], self.lPos[c][1]),
	# 											width = defaults["thickLines"]))
		
	# 	self.displayPts = InstructionGroup()

	# 	r = defaults["radiusPts"]
	# 	for p in self.lPos:
	# 		self.displayPts.add(Ellipse(pos = (p[0] - r/2., p[1] - r/2.), size = (r, r)))






