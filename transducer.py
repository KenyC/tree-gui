from tree import Tree
import re

DEFAULT_BLANK = "\t"

testTree = Tree()
testTree.sprout(0)
testTree.sprout(1)
testTree.sprout(2)
testTree.sprout(4)
testTree.sprout(6)

testString = "[.{aab} \n\t[.{efzfe} \n\t\t{zddz} \n\t\t[.{4zddz} \n\t\t\t{7dzdz} \n\t\t\t{dzdz8zdzd} \n\t\t]\n\t]\n\t[.{zazd2dzzd} \n\t\t{dzzd5zddz} \n\t\t[.{dd6ddzzd} \n\t\t\t{dzdz9dzzd} \n\t\t\t{dzdz10zdz} \n\t\t]\n\t]\n]\n"


def escapeBraces(str):
	return str.replace("{","\{").replace("}","\}").replace("[","\[").replace("]","\]")

class Transducer:

	# return expressions with formattable blanks
	def toUnsat(Tree):
		return ""
	
	@classmethod
	def toStr(cls, tree):
		return cls.toUnsat(tree).format(*tree.labels)

	# Returns list of labels
	# @classmethod
	# def extract(cls, tree, string):
	# 	regexp = escapeBraces(cls.toUnsat(tree).format(*["(?P<"+ str(i) +">.*)" for i in range(tree.n)]))
	# 	m = re.match(regexp, string)
	# 	if m is None:
	# 		return tree.labels #TEL
	# 	else:
	# 		return [ for i in range(tree.n)]

	@classmethod
	def regExp(cls, tree):
		regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		#regexp = escapeBraces(cls.toUnsat(tree).format(*["(.*)" for i in range(tree.n)]))
		return re.compile(regexp)

class QTreeTrans(Transducer):

	def toUnsat(tree):
		
		def toUnsatRec(tree, idx, space):
			if not tree.children[idx]:
				return space*DEFAULT_BLANK + "{{{{{idx}}}}} \n".format(idx = "{" + str(idx) + "}")
			else:
				returnStr = ""
				returnStr += space*DEFAULT_BLANK + "[.{{{{{idx}}}}} \n".format(idx = "{" + str(idx) + "}")

				for c in tree.children[idx]:
					returnStr += toUnsatRec(tree, c, space + 1)
				
				returnStr += space*DEFAULT_BLANK + "]\n"
				return returnStr

		return toUnsatRec(tree, 0, 0)

