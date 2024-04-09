class LinkedList:

	def __init__(self):
		self.first = None

	def getFirst(self):
		return self.first

	def addNode(self,node):

		if self.first is None:
			self.first = node
		else:
			current = self.first
			last = None
	
			while current:
				last = current
				current = current.getNext()

			last.next = node
		
	def search(self, name): # Nos ayuda a ver si una carpeta o archivo exista en la lista actual
		current = self.first
		while current:
			if name == current.getName():
				return True

			current = current.getNext()

		return False
		
	def getChild(self, name): #Obtenemos un nodo pasando un nombre
		if self.first is not None:
			current = self.first
		else:
			return None

		while current:
			if name == current.getName():
				return current

			current = current.getNext()
			
		return None

	def getBrotherNodeLeft(self, name): # Obtenemos el hermano de un nodo que tenga la lista
		current = self.first
		last = None
		if not self.search(name): # Comprobamos que exista
			return None	

		if (self.first.next is None) or (self.first.getName() == name): # Comprobamos que hallan 2 o mas elementos
			return None

		while current: # Aqui obtenemos al hermano comprobando el nombre del nodo siguiente con mi parametro name
			last = current.getNext()
			if name == last.getName():
				return current

			current = current.getNext()

	def getBrotherNodeRight(self, name): # Obtenemos el hermano de un nodo que tenga la lista
		
		if not self.search(name) or self.first.getName() == name : # Comprobamos que exista
			return None	

		current = self.first
		while current: # Aqui obtenemos al hermano comprobando el nombre del nodo siguiente con mi parametro name
			if name == current.getName():
				return current.getNext()
			
			current = current.getNext()

