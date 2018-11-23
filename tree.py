

# TREE
# stored as a list of list (Tree.children)
# at index i, Tree.children[i] is the set of indices that are children to i
# labels stored at index i
# IMPORTANT
# Always make sure that children always come after fathers
class Tree:

	def __init__(self, label = ""):
		self.labels = [label]
		self.children = [[]]

	# Add two children to a leaf, labels optional
	def sprout(self, idx, labelL = "", labelR = ""):
		if not self.children[idx]:
			self.labels += [labelL, labelR]
			self.children[idx] += [self.n , self.n + 1]
			self.children += [[],[]]

	@property
	def n(self):
		return len(self.children)
	
	# Delete all children of node idx
	def delete(self, idx):
		self.children[idx] = []
		# Some nodes may no longer be connected to the root ; delete them
		self.trim()

	# Returns the list of descendants of node "idx" ("idx" included)
	def accessible(self, idx = 0):
		l = [idx]
		for j in self.children[idx]:
			l.extend(self.accessible(j))

		return l

	# Remove nodes that are inaccessible from the root
	def trim(self):
		acc = self.accessible()

		# Stores the new position of nodes as function of the old position
		invAcc = {idx:i for i,idx in enumerate(acc)}

		# Creates new labels and children list from only the set of accessible nodes
		newLabels = [self.labels[idx] for idx in acc]
		newChildren = [self.children[idx] for idx in acc]

		# The position of nodes in the list has changed
		# Use the look-up table "invAcc" to replace old position of children with the new ones
		for i, cdren in enumerate(newChildren):
			newChildren[i] = [invAcc[c] for c in cdren]

		# Finally, update the tree with new values
		self.labels = newLabels
		self.children = newChildren

	# Prints simple representation of tree in string format (for debugging purposes)
	def show(self, idx = 0, space = 0):
		print(space*" "+ str(idx) if self.labels[idx] == "" else self.labels[idx])
		for c in self.children[idx]:
			self.show(c, space + 1)

	# Computes position of nodes if root is at coordinate "pos"
	# Display rules:
	#	- A leaf has a fixed width specified in "defaults".
	#	- The width of a subtree is the sum of width of his children.
	#	- A node's X coordinate is the average of its children's X coordinate (symmetry)
	#	- A node is always above its children by a height specified in "defaults".
	#	- Between adjacent sister nodes n1 and n2, there must be a gap of at least the width of n1 and the width of n2 (prenvents overlap)
	def construct(self, pos, **params):
		defaults = {"nodeWidth": 30., "height": 50.}
		defaults.update(params)


		# Computes the width of all subtrees
		# Looping from end to beginning makes sure we get to children before their mothers
		self.lgths = [0. for i in range(self.n)]
		for i in range(self.n - 1, -1, -1):
			if not self.children[i]:
				self.lgths[i] = defaults["nodeWidth"]
			else:
				self.lgths[i] = sum(self.lgths[c] for c in self.children[i])

		# Computes node position 
		# Initialization to the position of root
		self.positions = [pos for i in range(self.n)]
		for i in range(self.n):
			if self.children[i]:
				
				# Position of current node's daughter left edge
				leftEdge = 0.
				parentPos = self.positions[i]

				# Compute the position of daughter nodes relative to each other
				# As required by (prevents overlap)
				for c in self.children[i]:
					self.positions[c] = (parentPos[0] + leftEdge + self.lgths[c] / 2, parentPos[1] - defaults["height"])
					leftEdge += self.lgths[c]

				# Modify position so that mother node's X coordinate is the average of daughter nodes' X coordinate (symmetry)
				ecartPos = parentPos[0] - sum(self.positions[c][0] for c in self.children[i]) / (len(self.children[i]))
				for c in self.children[i]:
					self.positions[c] = (self.positions[c][0] + ecartPos, self.positions[c][1])
	



