 # -*- coding:utf-8 -*-

import sys
import os
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import QPushButton
from PyQt4.QtCore import pyqtSignal


class HoverButton(QPushButton):
    mouseHover = pyqtSignal(bool)
    mouseLeave = pyqtSignal(bool)

    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
         self.mouseHover.emit(True)
 
    def leaveEvent(self, event):
         self.mouseLeave.emit(True)

         
class Interface(object):

	def __init__(self,windows):
		self.openFolderButton = QtGui.QPushButton(windows)
		self.openFileButton = QtGui.QPushButton(windows)
		self.openDestinyEncryptButton = QtGui.QPushButton(windows)
		self.aboutButton = QtGui.QPushButton(windows)
		self.encryptButton = HoverButton(windows)
		self.decryptButton = HoverButton(windows)
		self.fullScreenButton = QtGui.QPushButton(windows)
		self.encryptComboBox = QtGui.QComboBox(windows)
		self.styleCombobox = QtGui.QComboBox(windows)
		self.pathTreeViewTextBox = QtGui.QPlainTextEdit(windows)
		self.pathEncryptTextBox = QtGui.QLineEdit(windows)
		self.passwordTextBox = QtGui.QLineEdit(windows)
		self.descriptionLabel = QtGui.QLabel(windows)
		self.styleLabel = QtGui.QLabel(windows)
		self.typeEncriptationLabel = QtGui.QLabel(windows)
		self.passwordLabel = QtGui.QLabel(windows)
		self.pathTreeViewLabel = QtGui.QLabel(windows)
		self.pathDestinyLabel = QtGui.QLabel(windows)
		self.treeView = QtGui.QTreeView(windows)

	def create(self, windows):
		# Ventana
		y = 300		
		H_TreeViewHe = 430
		W_TreeView = 370
		X_TreeView = 200
		Y_TreeView = 200
		
			
		windows.setGeometry(0,50,1366,740)
		windows.setWindowTitle("Proyecto Chronos")
		windows.setWindowIcon(QtGui.QIcon("Program/Interface/Img/icon2.png"))
		windows.setWindowIconText("Algo")
		

		#TreeView
		self.treeView.setObjectName("TreeView")
		self.treeView.setGeometry(X_TreeView,Y_TreeView,W_TreeView,H_TreeViewHe)
		self.treeView.header().hide()
		self.treeView.setIconSize(QtCore.QSize(35,35))
		self.treeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.treeView.setAnimated(True)
		self.treeView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		
		
		# Botones 
		self.openFolderButton.setObjectName("openFolderButton")
		self.openFolderButton.setGeometry(X_TreeView + 380, Y_TreeView - 110, 50, 45) 
		
		self.openFileButton.setObjectName("openFileButton")
		self.openFileButton.setGeometry(X_TreeView + 380, Y_TreeView - 55, 50, 45)

		self.openDestinyEncryptButton.setObjectName("openDestinyEncryptButton")
		self.openDestinyEncryptButton.setGeometry(X_TreeView + 380, Y_TreeView + H_TreeViewHe + 10, 50, 45)
	
		self.encryptButton.setObjectName("encryptButton")
		self.encryptButton.setGeometry(800,y + 200, 130, 130)
		self.encryptButton.raise_()
		
	
		self.decryptButton.setObjectName("decryptButton")
		self.decryptButton.setGeometry(950,y + 200, 130, 130)
		self.decryptButton.raise_()
	

		self.fullScreenButton.setObjectName("fullScreenButton")
		self.fullScreenButton.setGeometry(1240, 50, 60,60)
		
		self.aboutButton.setObjectName("aboutButton")
		self.aboutButton.setGeometry(80, 30, 60,60)


		#Combobox
		self.encryptComboBox.setObjectName("encryptComboBox")
		self.encryptComboBox.setGeometry(800,Y_TreeView - 45, 290, 30)
		self.encryptComboBox.addItem("AES 256")
		self.encryptComboBox.addItem("BlowFish")		

		self.styleCombobox.setObjectName("styleCombobox")
		self.styleCombobox.setGeometry(800,Y_TreeView + 80, 290, 30)

		# Rutas Line Edit y TextEdit
		self.pathTreeViewTextBox.setObjectName("pathTreeViewTextBox")
		self.pathTreeViewTextBox.setGeometry(X_TreeView, Y_TreeView - 110, 370, 100)
		

		self.pathEncryptTextBox.setObjectName("pathEncryptTextBox")
		self.pathEncryptTextBox.setPlaceholderText("Ingrese El Destino De La Encriptacion")
		self.pathEncryptTextBox.setGeometry(X_TreeView, Y_TreeView + H_TreeViewHe + 20, 370, 30)	

		self.passwordTextBox.setObjectName("passwordTextBox")
		self.passwordTextBox.setPlaceholderText(unicode("Ingrese Contraseña","utf-8"))
		self.passwordTextBox.setGeometry(X_TreeView, Y_TreeView + H_TreeViewHe + 60 , 370 , 30)

		#Label
		self.descriptionLabel.setObjectName("descriptionLabel")
		self.descriptionLabel.setGeometry(820, y + 100, 250, 50)
		self.descriptionLabel.setAlignment(QtCore.Qt.AlignCenter)		

		self.styleLabel.setObjectName("styleLabel")
		self.styleLabel.setText("Estilos")
		self.styleLabel.setGeometry(840, Y_TreeView + 25, 200, 50)
		self.styleLabel.setAlignment(QtCore.Qt.AlignCenter)		
		self.styleLabel.lower()

		self.typeEncriptationLabel.setObjectName("typeEncriptationLabel")
		self.typeEncriptationLabel.setText("Tipo De Encriptacion")
		self.typeEncriptationLabel.setGeometry(840, 80, 200, 60)
		self.typeEncriptationLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.typeEncriptationLabel.setWordWrap(True)
		self.typeEncriptationLabel.lower()

		self.pathTreeViewLabel.setObjectName("pathTreeViewLabel")
		self.pathTreeViewLabel.setText("Rutas:")
		self.pathTreeViewLabel.setGeometry(60, 110, 200, 50)
		self.pathTreeViewLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.pathTreeViewLabel.setWordWrap(True)
		self.pathTreeViewLabel.lower()

		self.pathDestinyLabel.setObjectName("pathDestinyLabel")
		self.pathDestinyLabel.setText("Destino:")
		self.pathDestinyLabel.setGeometry(45, 640, 200, 50)
		self.pathDestinyLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.pathDestinyLabel.setWordWrap(True)
		self.pathDestinyLabel.lower()

		self.passwordLabel.setObjectName("passwordLabel")
		self.passwordLabel.setText(unicode("Contraseña:","utf-8"))
		self.passwordLabel.setGeometry(25, 680, 200, 50)
		self.passwordLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.passwordLabel.setWordWrap(True)
		self.passwordLabel.lower()

