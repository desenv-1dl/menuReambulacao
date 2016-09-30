# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils
import psycopg2
from PyQt4.QtCore import QSettings
import os
import re
import sys
import csv
import resources
import interface_menu
from interface_menu import *
from interface_form import *


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Dialog(object):
	def __init__(self, Dialog, face):
		self.Dialog=Dialog
		self.iface=face
		self.Dialog.setObjectName(_fromUtf8("Dialog"))
		self.Dialog.setStyleSheet(_fromUtf8("background-color: rgb(205,205,205);"))
		self.Dialog.resize(400, 769)
		self.verticalLayout = QtGui.QVBoxLayout(self.Dialog)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.formV={}       
		self.retranslateUi(self.Dialog)
		QtCore.QMetaObject.connectSlotsByName(self.Dialog)

	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", self.iface.activeLayer().name(), None))        	

	def criarCombo(self, nome, mapaValor, padrao=None):
		horizontalLayout_3 = QtGui.QHBoxLayout()
		horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		label_2 = QtGui.QLabel(self.Dialog)
		label_2.setObjectName(_fromUtf8("label_2"))
		label_2.setStyleSheet(_fromUtf8("background-color: rgb(255,255, 255);"))
		horizontalLayout_3.addWidget(label_2)
		comboBox = QtGui.QComboBox(self.Dialog)
		comboBox.setObjectName(_fromUtf8(nome+"CB"))
		horizontalLayout_3.addWidget(comboBox)
		self.verticalLayout.addLayout(horizontalLayout_3)
		label_2.setText(_translate("Dialog", nome, None))
		if len(mapaValor)> 0:		
			for x in mapaValor.keys():
				comboBox.addItem(x, x.replace(" ",""))
		index=comboBox.findData("Aserpreenchido")
		comboBox.setCurrentIndex(index)
		if padrao != None:
			index=comboBox.findData(padrao[0].replace(" ",""))
			comboBox.setCurrentIndex(index)
			if len(padrao) == 2:
				rgb = padrao[1].split("-")
				label_2.setStyleSheet(_fromUtf8("color: rgb("+rgb[0]+","+rgb[1]+","+rgb[2]+");"))		
		self.valorCombo(comboBox)	

	def valorCombo(self, combo=None):	
		def valorC(item):
			self.formV[unicode(combo.objectName())]=unicode(item)	
		self.formV[unicode(combo.objectName())]=""
		valorC(unicode(combo.currentText()))
		QObject.connect(combo, QtCore.SIGNAL("activated(const QString&)"), valorC)

	def criarLine(self, nome, tipo, padrao=None):		   
		horizontalLayout_2 = QtGui.QHBoxLayout()
		horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		label = QtGui.QLabel(self.Dialog)
		label.setObjectName(_fromUtf8("label"))
		label.setStyleSheet(_fromUtf8("background-color: rgb(255,255, 255);"))
		#label.setStyleSheet(_fromUtf8("color: rgb(x,x,x);"))
		horizontalLayout_2.addWidget(label)
		lineEdit = QtGui.QLineEdit(self.Dialog)
		lineEdit.setObjectName(_fromUtf8(nome+"LE"))
		horizontalLayout_2.addWidget(lineEdit)	
		self.verticalLayout.addLayout(horizontalLayout_2)
		label.setText(_translate("Dialog", nome, None))                
		if padrao != None:
			if (not padrao[0] == "NULL") and (not padrao[0] == None) and (not padrao[0] == 'None' ):
				lineEdit.setText(padrao[0])
		self.valorLine(lineEdit, tipo)         

	def valorLine(self, line, tp):
		tipagem=tp
		def valorL(item):
			if tipagem == "float4":
				if (item != "") :						
					try:
						self.formV[unicode(line.objectName())]=float(item)
					except:
						line.clear()
						QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Campo só recebe valores 'Float'!</font>", QMessageBox.Close)
				else:
					self.formV[unicode(line.objectName())]=None
	
			elif tipagem == "varchar":
				if item != "":	
					try:
						self.formV[unicode(line.objectName())]=unicode(item)
					except:
						line.clear()
						QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Campo só recebe valores 'Varchar'!</font>", QMessageBox.Close)
				else:
					self.formV[unicode(line.objectName())]=None

			elif tipagem == "int2":
				if item != "":
					try:
						self.formV[unicode(line.objectName())]=int(item)
					except:
						line.clear()
						QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Campo só recebe valores 'Int'!</font>", QMessageBox.Close)
				else:
					self.formV[unicode(line.objectName())]=None
			else:
			  QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Formato não relacionado!</font>", QMessageBox.Close)
		if not line.text() == None:
			self.formV[unicode(line.objectName())]=line.text()
		line.textEdited.connect(valorL)	

	def criarBotoes(self):
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.pushButton = QtGui.QPushButton(self.Dialog)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.horizontalLayout_3.addWidget(self.pushButton)
		self.pushButton_2 = QtGui.QPushButton(self.Dialog)
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.horizontalLayout_3.addWidget(self.pushButton_2)        
		self.verticalLayout.addLayout(self.horizontalLayout_3)
		self.pushButton.setText(_translate("Dialog", "Confirmar", None))
		self.pushButton_2.setText(_translate("Dialog", "Cancelar", None))

	def linha(self):
		self.line = QtGui.QFrame(self.Dialog)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.line.setObjectName(_fromUtf8("line"))
		self.verticalLayout.addWidget(self.line)

	def obter_FormV(self):
		return self.formV

	def criarCampos(self, botao, valores):
		self.atributagem=valores
		grupoType={}		
		for x in self.iface.activeLayer().pendingAllAttributesList():	
			grupoType[self.iface.activeLayer().pendingFields()[x].name()]=self.iface.activeLayer().pendingFields()[x].typeName()	
		for index in self.iface.activeLayer().pendingAllAttributesList():
			if not index == 0:
				try:
					if self.iface.activeLayer().valueMap(index).keys()[0] != "UseHtml":
						if self.iface.activeLayer().pendingFields()[index].name() in self.atributagem[botao][self.iface.activeLayer().name()].keys():
							self.criarCombo(unicode(self.iface.activeLayer().pendingFields()[index].name()), self.iface.activeLayer().valueMap(index), self.atributagem[botao][self.iface.activeLayer().name()].get(self.iface.activeLayer().pendingFields()[index].name()))
						else:
							self.criarCombo(unicode(self.iface.activeLayer().pendingFields()[index].name()), self.iface.activeLayer().valueMap(index), None)
					else:
						padrao = self.atributagem[botao][self.iface.activeLayer().name()].get(self.iface.activeLayer().pendingFields()[index].name())
						self.criarLine(unicode(self.iface.activeLayer().pendingFields()[index].name()), grupoType.get(unicode(self.iface.activeLayer().pendingFields()[index].name())), padrao)
				except:
					padrao = self.atributagem[botao][self.iface.activeLayer().name()].get(self.iface.activeLayer().pendingFields()[index].name())
					self.criarLine(unicode(self.iface.activeLayer().pendingFields()[index].name()), grupoType.get(unicode(self.iface.activeLayer().pendingFields()[index].name())), padrao)

	def valorCampos(self, i, valores, dialogo):
		formV=valores
		idt=int(i)
		dialogo.accept()
		grupoAttr={}
		for x in self.iface.activeLayer().pendingAllAttributesList():	
			grupoAttr[self.iface.activeLayer().pendingFields()[x].name()]=x				
		for campo in formV.keys():
			if (campo[:-2] in grupoAttr) :
				if unicode(campo[-2:]) == u"LE":
					if formV.get(campo) == u'':
						idx = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))						
						self.iface.activeLayer().changeAttributeValue(int(idt) , idx, None)
					else:
						idx = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))						
						self.iface.activeLayer().changeAttributeValue(int(idt) , idx, formV.get(campo))								
				else:					
					idx2 = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))
					self.iface.activeLayer().changeAttributeValue(int(idt) , idx2, self.iface.activeLayer().valueMap(grupoAttr.get(unicode(campo[:-2]))).setdefault(unicode(formV.get(campo))))
		self.removeSelecoes()
	
	def removeSelecoes(self):
		for i in range(len(self.iface.mapCanvas().layers())):
			try:
				self.iface.mapCanvas().layers()[i].removeSelection()
			except:
				pass
		
	








