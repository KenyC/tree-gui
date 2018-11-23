from tree import Tree
import re

#Constants
DEFAULT_BLANK_QTREE = "\t"
DEFAULT_BLANK_HASKELL = "   "

# Test values for debugging
testTree = Tree()
testTree.sprout(0)
testTree.sprout(1)
testTree.sprout(2)
testTree.sprout(4)
testTree.sprout(6)

testString = "[.{aab} \n\t[.{efzfe} \n\t\t{zddz} \n\t\t[.{4zddz} \n\t\t\t{7dzdz} \n\t\t\t{dzdz8zdzd} \n\t\t]\n\t]\n\t[.{zazd2dzzd} \n\t\t{dzzd5zddz} \n\t\t[.{dd6ddzzd} \n\t\t\t{dzdz9dzzd} \n\t\t\t{dzdz10zdz} \n\t\t]\n\t]\n]\n"


# HELPER FUNCTIONS
def escapeBraces(str):
	return str.replace("{","\{").replace("}","\}").replace("[","\[").replace("]","\]")

# TRANSDUCER
# Abstract class for tree-to-string transducer
# To be overloaded:
# - toUnsat : returns the structure of the tree in string format with formattable blanks, where the labels should be inserted
# - indicesOrder : look-up table matching the order of appearance in the string with index in Tree structure
# Provided given overloaded methods
# - toStr : returns the string representation of the tree with its labels
# - regExp : compiles a regular expression that matches the tree's structure to strings ; 
#   this regular expression, in combination with indicesOrder, allows recovery of tree labels from string
class Transducer:

	# return expressions with formattable blanks
	def toUnsat(tree):
		return ""
	
	@classmethod
	def toStr(cls, tree):
		return cls.toUnsat(tree).format(*tree.labels)


	@classmethod
	def regExp(cls, tree):
		regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		#regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		return re.compile(regexp)

	def indicesOrder(tree, index = 0):
		s = [index]

		for c in tree.children[index]:
			s += Transducer.indicesOrder(tree, c)

		return s

# Daughter class for QTree representation
class QTreeTrans(Transducer):

	def toUnsat(tree):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return space*DEFAULT_BLANK_QTREE + "{{{{{idx}}}}} \n".format(idx = "{" + str(idx) + "}")
			else:
				returnStr = ""
				returnStr += space*DEFAULT_BLANK_QTREE + "[.{{{{{idx}}}}} \n".format(idx = "{" + str(idx) + "}")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr += space*DEFAULT_BLANK_QTREE + "]\n"
				return returnStr

		return toUnsatRec(tree, 0, 0)

# class HaskellTrans(Transducer):

# 	def toUnsat(tree):
# 		def toUnsatRec(tree, idx, space):
# 			if not tree.children[idx]:
# 				return space*DEFAULT_BLANK_HASKELL + "{idx} \n".format(idx = "{" + str(idx) + "}")
# 			else:
# 				returnStr = ""
# 				returnStr += space*DEFAULT_BLANK_QTREE + "({idx} \n".format(idx = "{" + str(idx) + "}")
# 				returnStr += space*DEFAULT_BLANK_QTREE + "<^>"
# 				returnStr += space*DEFAULT_BLANK_QTREE + "("
# 				for c in tree.children[idx]:
# 					returnStr += toUnsatRec(tree, c, space + 1)
				
# 				returnStr += space*DEFAULT_BLANK_QTREE + "]\n"
# 				return returnStr

# 		return toUnsatRec(tree, 0, 0)