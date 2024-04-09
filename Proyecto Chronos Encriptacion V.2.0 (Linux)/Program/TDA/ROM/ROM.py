 # -*- coding: utf-8 -*-
import json
from Program.TDA.Node import *

class ROM:

	def save(self,node):
	
		diccionaryTree = {"/":[]}
		current = node
		self.saveInner(diccionaryTree["/"], current)
		file = open("ROM.json", 'w')
		file.write(json.dumps(diccionaryTree, indent = 2))
									
	def saveInner(self,array,currentNode):
		current = currentNode.value.getFirstChild()

		while current:
			d = {"Type":"","Name":""}
			strType = isinstance(current.value,Folder)
			strName = current.getName() 	
			d.update(Type=strType)
			d.update(Name=strName)
			
			if strType: # Si es True significa que es una carpeta
				d.update(Child=[])
				self.saveInner(d["Child"], current)	#aqui deberia ir la funcion recursiva donde enviaran el arreglo

			array.append(d)
			current = current.getNext()

	def load(self):
		file = open("ROM.json","r")
		data = json.load(file)
		data = data["/"]
		node = Node(Folder("/"))
		
		self.loadInner(node,data)
		
		return {"root":node}
		

	def loadInner(self,node,listChildNode):	
		listNode = []
		father = node

		for dic in listChildNode:
			nodeType = dic["Type"]
			nodeName = dic["Name"]

			if nodeType is True:
				node = Node(Folder(nodeName))
				self.loadInner(node,dic["Child"])
				listNode.append(node)
			else:
				node = Node(File(nodeName))
				listNode.append(node)
		
		for child in listNode:
			father.value.add(child)
