from Node import *
from ROM import * 

class Tree:
	def __init__(self, node = None):
		self.root = {"root": Node(Folder("/"))}
		self.currentNode = self.root["root"] # Nodo actual cuando invoque a cd
		self.path = '/'
		self.myROM = ROM()

	def getRoot(self):
		return self.root["root"]

	def getCurrentNode(self):
		return self.currentNode
	
	def save(self):
		self.myROM.save(self.root["root"])

	def load(self):
		self.root = self.myROM.load()
		self.currentNode = self.root["root"]

	# Comandos Auxiliares
	def find(self):
	 	print "Impresion"
		directory = self.getRoot()
		self.findInner(directory.getName(),directory)
		print "\nFin Impresion\n"

	def findInner(self,strPath,directory):
		currentDirectory = directory.value.getFirstChild()
		if strPath != "/":
			strPath += '/'
			
		while currentDirectory:
			print strPath + currentDirectory.getName()
			if isinstance(currentDirectory.value,Folder):
				if currentDirectory.value.getFirstChild() is not None:
					self.findInner(strPath + currentDirectory.getName(),currentDirectory)

			currentDirectory = currentDirectory.getNext()

	# Borrar arbol
	def deleteTree(self):	
		self.deleteTreeInner(self.getRoot())

	def deleteTreeInner(self,fatherDirectory):
		currentNode = fatherDirectory.value.getFirstChild()
		while currentNode:
			if isinstance(currentNode.value,Folder):
				self.deleteTreeInner(currentNode)
			
			currentNode = currentNode.next

		fatherDirectory.value.childs.first = None
			





