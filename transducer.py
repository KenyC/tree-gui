from tree import Tree
import utils
import re

#Constants
DEFAULT_BLANK_QTREE = "\t"
DEFAULT_BLANK_PYTHON = "\t"
DEFAULT_BLANK_HASKELL = "   "


# HELPER FUNCTIONS
def escapeBraces(str):
	return str.replace("\\", "\\\\").replace("{","\{").replace("}","\}").replace("[","\[").replace("]","\]").replace("^","\^").replace("(","\(").replace(")","\)").replace("+","\+")

# TRANSDUCER
# Abstract class for tree-to-string transducer
# To be overloaded:
# - toUnsat : returns the structure of the tree in list of strings format formattable blanks, where the labels should be inserted
# Provided given overloaded methods
# - toStr : returns the string representation of the tree with its labels
# - regExp : compiles a regular expression that matches the tree's structure to strings ; 
#   this regular expression, in combination with indicesOrder, allows recovery of tree labels from string
# - indicesOrder : returns a look-up list where the i-th value is the index of the node at that position.
class Transducer:

	# return expressions with list of strings with labels in place
	def toUnsat(tree, labels):
		return labels
	
	@classmethod
	def toStr(cls, tree):
		return "".join(cls.toUnsat(tree, tree.labels))


	@classmethod
	def regExp(cls, tree):
		# Create a list with blanks where labels should be
		blankList = cls.toUnsat(tree, ["" for i in range(tree.n)])
		regexp = ["(.*)" if s == "" else escapeBraces(s) for s in blankList]
		#regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		return re.compile("".join(regexp))

	@classmethod
	def indicesOrder(cls, tree):
		return list(filter(lambda x: isinstance(x, int), cls.toUnsat(tree, range(tree.n))))

	@classmethod
	def find(cls, tree, i):
		listStr = cls.toUnsat(tree, range(tree.n))
		index = next( (j for j,x in enumerate(listStr) if isinstance(x, int) and x == i), -1)
		fillLabel = [tree.labels[word] if isinstance(word, int) else word for word in listStr]
		beginning = len("".join(fillLabel[:index]))
		return {"start": beginning, "end": beginning + len(tree.labels[i])}

# Daughter class for QTree representation
class QTreeTrans(Transducer):

	def toUnsat(tree, labels):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_QTREE + "{", labels[idx], "} \n"]
			else:
				returnStr = []
				returnStr.append(space*DEFAULT_BLANK_QTREE + "[.{")
				returnStr.append(labels[idx])
				returnStr.append("} \n")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr.append(space*DEFAULT_BLANK_QTREE + "]\n")
				return returnStr

		return ["\\Tree ","\n"] + toUnsatRec(tree, 0, 0)

	def parse(string):

		
		stack = []
		countBracket = 0
		lastTree = None

		for c in string:



			if c == "}":
				# collapse literals till "{"

				topChar = ""
				while stack[-1] != "{":
					stack[-1] += topChar
					topChar = stack.pop()

				stack.pop() 
				stack.append("{" + topChar + "}")
				countBracket -= 1

			elif c == "]" and countBracket == 0:
				elemTrees = []


				while len(elemTrees) != 3:
					topElem = stack.pop()

					if isinstance(topElem, Tree):
						elemTrees.append(topElem)
					elif topElem[0] == "{" and topElem[-1] == "}":
						elemTrees.append(Tree(label = topElem[1:-1]))

				topElem = ""
				while topElem != "[":
					topElem = stack.pop()

				elemTrees[2] = elemTrees[2].labels[0]
				lastTree = Tree.fromTrees(elemTrees[:-1][::-1], label = elemTrees[2])
				stack.append(lastTree)

			else:
				stack.append(c)
				if c == "{":
					countBracket += 1

		return lastTree






# Daughter class for my Haskell implementation of H&K
class HaskellTrans(Transducer):

	def toUnsat(tree, labels):
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_HASKELL + "(", labels[idx], ")\n"]
			else:
				returnStr = []
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_HASKELL + "(\n")

				for i,c in enumerate(tree.children[idx]):
					returnStr += toUnsatRec(tree, c, space + 1)
					if i != len(tree.children[idx]) - 1:
						returnStr.append((space + 1)*DEFAULT_BLANK_HASKELL + "  <^>\n")
				
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_HASKELL + ")\n")
				
				return returnStr

		return toUnsatRec(tree, 0, 0)

# Daughter class for forest
class ForestTrans(Transducer):

	def toUnsat(tree, labels):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_QTREE + "[", labels[idx], "] \n"]
			else:
				returnStr = []
				returnStr.append(space*DEFAULT_BLANK_QTREE + "[{")
				returnStr.append(labels[idx])
				returnStr.append("} \n")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr.append(space*DEFAULT_BLANK_QTREE + "]\n")
				return returnStr

		return ["\\begin{forest}\n"] + toUnsatRec(tree, 0, 0) + ["\\end{forest}\n"]

# Daughter class for my Python implementation of H&K
class PythonTrans(Transducer):

	def toUnsat(tree, labels):
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return [space*DEFAULT_BLANK_PYTHON + "(", labels[idx], ")"]
			else:
				returnStr = []
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_PYTHON + "(\n")

				for i,c in enumerate(tree.children[idx]):
					returnStr += toUnsatRec(tree, c, space + 1)
					if i != len(tree.children[idx]) - 1:
						returnStr.append("  +\\\n")
					else:
						returnStr.append("  \n")
				
				if idx != 0:
					returnStr.append(space*DEFAULT_BLANK_PYTHON + ")")
				
				return returnStr

		return toUnsatRec(tree, 0, -1)

if __name__ == "__main__":
	string = r"""
	\Tree
	[.{fezfe}
	[.{efz} {efz} {ezfe}]
	[.{zfeef} {efzef}  [.{fez} {zefef} {ezfef} ]]
	]
	"""

	# Test values for debugging
	testTree = Tree()
	testTree.sprout(0)
	testTree.sprout(1)
	testTree.sprout(2)
	testTree.sprout(4)
	testTree.sprout(6)

	testTree2 = testTree.copy()
	testTree2.labels = ["efz","ezfefz","joi","ohiho","trl","cvj","gjph","trb","erb","reh","gzr"]

	testString = "\\Tree \n[.{aab} \n\t[.{efzfe} \n\t\t{zddz} \n\t\t[.{4zddz} \n\t\t\t{7dzdz} \n\t\t\t{dzdz8zdzd} \n\t\t]\n\t]\n\t[.{zazd2dzzd} \n\t\t{dzzd5zddz} \n\t\t[.{dd6ddzzd} \n\t\t\t{dzdz9dzzd} \n\t\t\t{dzdz10zdz} \n\t\t]\n\t]\n]\n"
	testString2 = "\\Tree \n[.{} \n\t[.{} \n\t\t{} \n\t\t[.{} \n\t\t\t{} \n\t\t\t{} \n\t\t]\n\t]\n\t[.{} \n\t\t{} \n\t\t[.{} \n\t\t\t{} \n\t\t\t{} \n\t\t]\n\t]\n]\n"
