from LinkedList import *

class Folder:
	def __init__(self,name = "New Folder"):
		self.name = name
		self.childs = LinkedList()

	def add(self,node):
		self.childs.addNode(node)

	def getFirstChild(self):
		return self.childs.first

	def getChild(self,name):
		return self.childs.getChild(name)

	def printChilds(self):
		current = self.childs.first

		while(current):
			print current.value.name
			current = current.next