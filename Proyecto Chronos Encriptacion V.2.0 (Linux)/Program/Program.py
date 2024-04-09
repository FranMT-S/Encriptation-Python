# -*- coding:utf-8 -*-
import os
import os.path
import sys
import codecs
import threading
from TDA.Tree import *
from Interface.Interface import * 
from EncryptDecrypt.AES256 import *
from EncryptDecrypt.BlowFish import *
from PerfomanceSimulator import *


class Program:
	def __init__(self):	
		self.tree = Tree()
		self.app = QtGui.QApplication(sys.argv)
		self.windows = QtGui.QMainWindow()
		self.interface = Interface(self.windows)
		self.alert = False
		self.destinyEmpty = False
		self.about = False

		# Agregar Stilos
		for css in os.listdir("Program/Interface/css"):
			if ".css" in css:
				end = css.index(".css")					
				self.interface.styleCombobox.addItem(unicode(css[0:end],"utf-8"))
				
		for i in range(self.interface.styleCombobox.count()):
			if self.interface.styleCombobox.itemText(i) == "Green":	
				self.interface.styleCombobox.setCurrentIndex(i)
		# Fin Agregar Estilos

		# Cargar El Arbol al inicio
		self.tree.load()
		self.setModel()
		
		"""=======================================
			Conexiones (Eventos) de los elementos
		   ======================================="""
		
		QtCore.QObject.connect(self.interface.pathTreeViewTextBox, QtCore.SIGNAL("textChanged()"), self.update)
		QtCore.QObject.connect(self.interface.treeView, QtCore.SIGNAL("expanded(QModelIndex)"), self.updateWidthModel)
		QtCore.QObject.connect(self.interface.treeView, QtCore.SIGNAL("collapsed(QModelIndex)"), self.updateWidthModel)
		QtCore.QObject.connect(self.interface.passwordTextBox, QtCore.SIGNAL("textChanged(QString)"), self.correctPassword)
		self.interface.encryptButton.clicked.connect(self.executeEncrypt)	
		self.interface.decryptButton.clicked.connect(self.executeDecrypt)	
		self.interface.aboutButton.clicked.connect(self.getAbout)	
		self.interface.openFolderButton.clicked.connect(self.setPath)
		self.interface.openFileButton.clicked.connect(self.setPathFile)
		self.interface.fullScreenButton.clicked.connect(self.fullScreen)		
		self.interface.openDestinyEncryptButton.clicked.connect(self.setPathDestinyEncrypt)				
		self.interface.encryptButton.mouseHover.connect(self.encryptionDescription)	
		self.interface.encryptButton.mouseLeave.connect(self.cleanDescription)	
		self.interface.decryptButton.mouseHover.connect(self.decryptionDescription)	
		self.interface.decryptButton.mouseLeave.connect(self.cleanDescription)	
		self.interface.styleCombobox.currentIndexChanged.connect(self.setStyle)	
		self.interface.styleCombobox.currentIndexChanged.connect(self.update)	


	# Actualizar el arbol interno y el treeview
	def update(self):	
		self.generateTree()
		self.setModel()
		self.interface.treeView.expandAll()
		self.updateWidthModel()

	"""===================================
			Crear TDA: Arbol (Tree)
	   ==================================="""
	def generateTree(self):
		node = None

		if not self.tree.getRoot().value.getFirstChild() is None:
			self.tree.deleteTree()
		
		# Convertir cadena utf-8 a cadena unicode
		for path in self.getListPath():
			path = unicode(path,"utf-8")
			if os.path.isdir(path):	

				if(path[-1] == "/"):
					nameFirstFolder = path.strip("/").split("/").pop()
				else:
					nameFirstFolder = path.split("/").pop()

				node = Node(Folder(nameFirstFolder))
				self.generateTreeInner(path,node)
				self.tree.getRoot().value.add(node)
			else:
				self.generateTreeInner(path,self.tree.getRoot())

		self.tree.save()
		

	def generateTreeInner(self,path = None,node = None):
		if "\\" in path:
			path = path.replace("\\","/")

		if os.path.isdir(path):
			folderContein = os.listdir(path)
			for directoryName in folderContein:	
				# Verificar que no existan datos tipo unicode_escape
				# Si existen convertirlos a Unicode
				if not type(directoryName) is unicode:
					directoryName = unicode(directoryName,"unicode_escape")			
					
				sub_path = os.path.join(path,directoryName).replace("\\","/") # unir rutas	

				if os.path.isdir(sub_path):		
					newNode = Node(Folder(directoryName)) 
					self.generateTreeInner(sub_path, newNode)
				elif os.path.isfile(sub_path):
					newNode = Node(File(directoryName))

				node.value.add(newNode)

		elif os.path.isfile(path):
			# Verificar que no existan datos tipo unicode_escape
			# Si existen convertirlos a Unicode
			if not type(path) is unicode:
				path = unicode(path,"unicode_escape")	

			nameNode = path.split("/").pop()
			newNode = Node(File(nameNode))
			node.value.add(newNode)

	"""===================================
			Crear el TreeView
	   ==================================="""

	def setModel(self):
		item = self.getItemTreeView()	
		model = QtGui.QStandardItemModel()
		model.appendRow(item)
		self.interface.treeView.setModel(model)

	def getItemTreeView(self):
		firstName = self.tree.getRoot().getName()
		rootItem = QtGui.QStandardItem(firstName)
		rootItem.setIcon(self.getIconRoot())
		
		return self.getItemTreeViewInner(self.tree.getRoot().value.getFirstChild(),rootItem)

	def getItemTreeViewInner(self, node = None, item = None):
		current = node
		while(current):
			subName = current.getName()
			subItem = QtGui.QStandardItem(subName)
			subItem.setIcon(self.getIconFile())
			if isinstance(current.value,Folder):
				icon = self.getIconFolder()
				subItem.setIcon(icon)
				self.getItemTreeViewInner(current.value.getFirstChild(), subItem)
			
			item.appendRow(subItem)
			current = current.getNext()

		return item

	def updateWidthModel(self):
		self.interface.treeView.resizeColumnToContents(0);

	"""===================================
		Ejecutar Encriptar y Desencriptar
	   ==================================="""

	def executeEncrypt(self):
		self.typeAlgorithm("Encriptacion")

	def executeDecrypt(self):
		self.typeAlgorithm("Desencriptacion")

	def typeAlgorithm(self, typeAlgorithm = ""):
		if self.getKey() == "":
			self.alertPassword()
		else:
			# Obtener destino, este vacio o no.
			self.destinyEmpty = True if self.getDestiny() == "" else False

			for pathCurrent in self.getListPath():
				if os.path.exists(pathCurrent):
					destiny = self.getDestiny()
					pathCurrent = unicode(pathCurrent,"utf-8")

					if self.destinyEmpty:
						if os.path.isfile(pathCurrent):
							f = pathCurrent.rfind("/")
							destiny = pathCurrent[:f] + "/"
						elif os.path.isdir(pathCurrent):
							destiny = pathCurrent + "/"

					if os.path.isdir(pathCurrent) and not self.destinyEmpty:
						pathComparation = pathCurrent.strip("/") + "/"
						destinyComparation = destiny.strip("/") + "/"
						if  pathComparation != destinyComparation:
							f = pathCurrent.rfind("/")
							nameFolder = pathCurrent[f:] + "/"
							destiny = destiny + nameFolder
	

					if self.interface.encryptComboBox.currentText() == "AES 256":
						self.writeHead("AES 256: %s" % typeAlgorithm)
						self.executeAlgorithm(
						path = pathCurrent, 
						destiny = destiny,
						algorithm = AES256,
						typeAlgorithm = typeAlgorithm
						)

					elif self.interface.encryptComboBox.currentText() == "BlowFish":
						self.writeHead("BlowFish: %s" % typeAlgorithm)
						self.executeAlgorithm(
						path = pathCurrent, 
						destiny = destiny,
						algorithm = BlowFish,
						typeAlgorithm = typeAlgorithm
						)

				if os.path.exists(pathCurrent) and os.path.isdir(pathCurrent):			
					if os.listdir(pathCurrent) == []:
						os.rmdir(pathCurrent)

				self.writeFoot()
				self.update()

	def executeAlgorithm(self, path = None, destiny = None, algorithm = None, typeAlgorithm = ""):
		if "\\" in path:
			path = path.replace("\\","/")

		if destiny != path:
			if not os.path.exists(destiny):
				os.mkdir(destiny)

		if os.path.isdir(path):
			folderContein = os.listdir(path)
			for fileEncrypt in folderContein:	
				# Verificar que no existan datos tipo unicode_escape
				# Si existen convertirlos a Unicode
				body = None
				if not type(fileEncrypt) is unicode:
					fileEncrypt = unicode(fileEncrypt,"unicode_escape")			
					
				sub_Path = os.path.join(path,fileEncrypt).replace("\\","/") # unir rutas	
				if os.path.isdir(sub_Path):	
					newName = sub_Path.split("/").pop()
					newDestiny = destiny + "/" + newName + "/" 
					self.executeAlgorithm(sub_Path, newDestiny, algorithm, typeAlgorithm)

				elif os.path.isfile(sub_Path):
					if typeAlgorithm == "Encriptacion":
						body = TestAlgorithm().test(algorithm(self.getKey()).encrypt_file, sub_Path, destiny)
					elif typeAlgorithm == "Desencriptacion" and ".enc" in sub_Path:
						body = TestAlgorithm().test(algorithm(self.getKey()).decrypt_file, sub_Path, destiny)
					
					if body is not None:
						self.writeBody(*body)
			
			if os.path.exists(path):			
				if os.listdir(path) == []:
					os.rmdir(path)

		elif os.path.isfile(path):
			# Verificar que no existan datos tipo unicode_escape
			# Si existen convertirlos a Unicode
			if not type(path) is unicode:
				path = unicode(path,"unicode_escape")	

			if typeAlgorithm == "Encriptacion":
				body = TestAlgorithm().test(algorithm(self.getKey()).encrypt_file, path, destiny)
			elif typeAlgorithm == "Desencriptacion" and ".enc" in path:
				body = TestAlgorithm().test(algorithm(self.getKey()).decrypt_file, path, destiny)

			self.writeBody(*body)

	"""==============================================
		Obtener y establecer,rutas,estilo y mensajes
	   =============================================="""

	def setPath(self):
		pathDesktop =  QtGui.QDesktopServices().storageLocation(QtGui.QDesktopServices.DesktopLocation)
		search = QtGui.QFileDialog(directory = pathDesktop)
		search.setFileMode(QtGui.QFileDialog.DirectoryOnly)
		search.setOption(QtGui.QFileDialog.DontUseNativeDialog,True)
		search.setViewMode(QtGui.QFileDialog.Detail)
		
		listView = search.findChild(type(QtGui.QListView()),"listView")
		if listView:
			listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
			listView.setViewMode(QtGui.QListView.IconMode)

		treeView = search.findChild(type(QtGui.QTreeView()))
		if treeView:
			treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


		if search.exec_():
			listPath = search.selectedFiles()
			path = ""	
			for p in listPath:
				path += "\n"*2 + str(p) 

			if not path == "":
				self.interface.pathTreeViewTextBox.clear()

			path = path.strip("\n")
			self.interface.pathTreeViewTextBox.insertPlainText(path)

	def setPathFile(self):
		
		listPath = QtGui.QFileDialog.getOpenFileNames()
		path = ""	
		for p in listPath:
			path += "\n"*2 + str(p.toUtf8()) 
			
		if not path == "":
			self.interface.pathTreeViewTextBox.clear()

		path = path.strip("\n")
		self.interface.pathTreeViewTextBox.insertPlainText(unicode(path,"utf-8"))


	def setPathDestinyEncrypt(self):
		path = QtGui.QFileDialog.getExistingDirectory().replace("\\","/")
		if not path == "":
			self.interface.pathEncryptTextBox.setText(path + "/")

	def setDestinyEmpty(self,path):
		f = path.rfind("/")
		self.interface.pathEncryptTextBox.setText(path[:f] + "/")

	def getListPath(self):
		# Porque al final es un objeto sobrecargado (QbytesString) debemos pasarlo a cadena string
		paths = str(self.interface.pathTreeViewTextBox.toPlainText().toUtf8()).strip()
		listPath = []

		for p in paths.replace("\\","/").split("\n"):
			if p is not "":
				listPath.append(p)

		return listPath

	def getDestiny(self):
		# Porque al final es un objeto sobrecargado (QbytesString) debemos pasarlo a cadena string
		return str(self.interface.pathEncryptTextBox.text().toUtf8())  


	def getKey(self):
		return str(self.interface.passwordTextBox.text().toUtf8())

	def setStyle(self):
		path = "Program/Interface/css/%s.css" % self.interface.styleCombobox.currentText().toUtf8() 
		with open(path,"r") as style:
			self.windows.setStyleSheet(style.read())
		

	def fullScreen(self):

		if(self.windows.isFullScreen()):
			self.windows.showMaximized()
		else:	
			self.windows.showFullScreen()

	def encryptionDescription(self):
		self.interface.descriptionLabel.setText("Encriptar")
	
	def decryptionDescription(self):
		self.interface.descriptionLabel.setText("Desencriptar")
	
	def cleanDescription(self):
		self.interface.descriptionLabel.setText("")

	"""===================================
		Obtener Iconos Para El Treeview
	   ==================================="""

	def getIconRoot(self):
		icon = None
		if self.interface.styleCombobox.currentText().toUtf8() == "Green":
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/Root_01.png")
		
		else:
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/Root_02.png")
			
		return icon

	def getIconFolder(self):
		icon = None
		if self.interface.styleCombobox.currentText().toUtf8() == "Green":
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/Folder_01.png")

		else:
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/Folder_02.png")

		return icon
		
	def getIconFile(self):
		icon = None
		if self.interface.styleCombobox.currentText().toUtf8() == "Green":
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/File_01.png")

		else:
			icon = QtGui.QIcon("Program/Interface/Img/TreeItem/File_02.png")


		return icon

	def getAbout(self):
		try:
			os.system("firefox Program/About/About.html &")
		except Exception as e:
			msg = QtGui.QMessageBox()
			msg.setText("No se pudo abrir About.html")
			msg.exec_()


	"""===================================
		    Evitar Password en blanco
	   ==================================="""

	def alertPassword(self):
		self.alert = True 
		self.interface.passwordTextBox.setStyleSheet("background:#870000; border: 1px solid #ff0000;")	


	def correctPassword(self):
		if self.alert:
			self.alert = False
			self.interface.passwordTextBox.setStyleSheet("")

	"""===================================
			Escribir el log
	   ==================================="""

	def writeHead(self,nameAlgorith,):
		contein = '''
--------------------------------------------------------------------------------------------------------------------
				Algoritmo: {}						 
--------------------------------------------------------------------------------------------------------------------

{:20}			{:35}			{:}

		'''.format(nameAlgorith, "Nombre", "Fecha y Hora", "Tiempo De Ejecucion").strip()

		with open("log.txt","a") as log:
   			 log.write(contein)		

	# Fin Write Head

	def writeBody(self, nameFile, date, timeExecution):
		

		contein = '''\r\n \r\n
{:20}			{:35}			{:} Segundos
		'''.format(nameFile, date, timeExecution)
		
		with open("log.txt","a") as log:
   			 log.write(contein)		

	# Fin Write Body

	def writeFoot(self,):
		contein = '''
____________________________________________________________________________________________________________________\n
'''

		with open("log.txt","a") as log:
			log.write(contein)		

	# Fin Write Foot

	def run(self):
		self.windows.setObjectName("windows")
		self.interface.create(self.windows)
		self.setStyle()
		self.windows.showFullScreen()
		sys.exit(self.app.exec_())










