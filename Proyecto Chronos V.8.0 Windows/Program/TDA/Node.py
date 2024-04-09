
from File import *
from Folder import *

class Node:
	def __init__(self, value = None):
		self.value = value
		self.next = None

	def getValue(self):
		return self.value

	def getNext(self):
		return self.next

	def getName(self):
		return self.value.name

