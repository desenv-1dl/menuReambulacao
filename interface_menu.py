# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from MultiLayerSelection import MultiLayerSelection
from PyQt4.QtCore import QSettings
from qgis.core import *
from PyQt4.Qt import *
import psycopg2, sys, os, csv, resources
import os
import time
from interface_backup import *
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
class Ui_Dialog(object):
 	def __init__(self, Dialog, iface, DB):

		self.DB=DB
		self.iface=iface
								
		self.tool = MultiLayerSelection(self.iface.mapCanvas(), self.iface)
		self.caminho=""
		self.tabs={}
		
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(400, 659)
		Dialog.setStyleSheet(_fromUtf8("background-color: rgb(205,205,205);"))
		Dialog.rejected.connect(self.out)
		self.verticalLayout = QtGui.QVBoxLayout(Dialog)
		self.verticalLayout.setMargin(11)
		self.verticalLayout.setSpacing(6)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.botaoSelecionarCsv = QtGui.QPushButton(Dialog)
		self.botaoSelecionarCsv.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);background-color: rgb(205,205,205);"))
		self.botaoSelecionarCsv.setObjectName(_fromUtf8("botaoSelecionarCsv"))
		self.botaoSelecionarCsv.setText(_translate("Dialog", "Selecionar CSV", None))
		self.verticalLayout.addWidget(self.botaoSelecionarCsv)
		self.splitter_6 = QtGui.QSplitter(Dialog)
       		self.splitter_6.setOrientation(QtCore.Qt.Horizontal)
        	self.splitter_6.setObjectName(_fromUtf8("splitter_6"))	
		self.botaoSelecionarFeicao = QtGui.QPushButton(self.splitter_6)
		self.botaoSelecionarFeicao.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);background-color: rgb(205,205,205);"))
		self.botaoSelecionarFeicao.setObjectName(_fromUtf8("botaoSelecionarFeicao"))
		self.botaoSelecionarFeicao.setText(_translate("Dialog", " Selecionar Feição  ", None))
		self.botaoSelecionarFeicao.clicked.connect(self.run)	
		self.botaoRemoverSelecoes = QtGui.QPushButton(self.splitter_6)
		self.botaoRemoverSelecoes.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);background-color: rgb(205,205,205);"))
		self.botaoRemoverSelecoes.setObjectName(_fromUtf8("botaoRemoverSelecoes"))
		self.botaoRemoverSelecoes.setText(_translate("Dialog", "Remover Seleções", None))
		self.botaoRemoverSelecoes.clicked.connect(self.tool.removerSelecoes)
		self.verticalLayout.addWidget(self.splitter_6)
		self.splitter_7 = QtGui.QSplitter(Dialog)
       		self.splitter_7.setOrientation(QtCore.Qt.Horizontal)
        	self.splitter_7.setObjectName(_fromUtf8("splitter_7"))	
		self.botaoBackup = QtGui.QPushButton(self.splitter_7)
		self.botaoBackup.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);background-color: rgb(205,205,205);"))
		self.botaoBackup.setObjectName(_fromUtf8("botaoBackup"))
		self.botaoBackup.setText(_translate("Dialog", "          BACKUP       ", None))
		self.botaoBackup.clicked.connect(self.runBackup)	
		self.abrirFormulario = QtGui.QPushButton(self.splitter_7)
		self.abrirFormulario.setStyleSheet(_fromUtf8("color: rgb(0, 0, 0);background-color: rgb(205,205,205);"))
		self.abrirFormulario.setObjectName(_fromUtf8("abrirFormulario"))
		self.abrirFormulario.setText(_translate("Dialog", "Abrir Formulário", None))
		self.abrirFormulario.clicked.connect(self.openForm)
		self.verticalLayout.addWidget(self.splitter_7)
		self.line = QtGui.QFrame(Dialog)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.line.setObjectName(_fromUtf8("line"))
		self.verticalLayout.addWidget(self.line)
		self.splitter_3 = QtGui.QSplitter(Dialog)
		self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
		self.splitter_3.setObjectName(_fromUtf8("splitter_3"))
		self.label = QtGui.QLabel(self.splitter_3)
		self.label.setStyleSheet(_fromUtf8("background-color: rgb(85, 255, 0);"))
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(self.splitter_3)
		self.label_2.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 0);"))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_5 = QtGui.QLabel(self.splitter_3)
		self.label_5.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
		self.label_5.setObjectName(_fromUtf8("label_5"))
		self.label_3 = QtGui.QLabel(self.splitter_3)
		self.label_3.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
	"background-color: rgb(0, 0, 0);"))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(self.splitter_3)
		self.label_4.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 255);\n"
	"color: rgb(255, 255, 255);"))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.verticalLayout.addWidget(self.splitter_3)
		self.tabWidget = QtGui.QTabWidget(Dialog)
		self.tabWidget.setTabPosition(QtGui.QTabWidget.West)
		self.tabWidget.setMovable(True)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.verticalLayout.addWidget(self.tabWidget)
		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)
		
		

	def obterTabs(self):
		return self.tabs		
	

	def criarTab(self, listaCategorias):

		for categoria in listaCategorias:
			tab_3 = QtGui.QWidget()
			tab_3.setObjectName(_fromUtf8(categoria))
			verticalLayout_4 = QtGui.QVBoxLayout(tab_3)
			verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
			scrollArea = QtGui.QScrollArea(tab_3)
			scrollArea.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
			scrollArea.setWidgetResizable(True)
			scrollArea.setObjectName(_fromUtf8("scrollArea"))
			scrollAreaWidgetContents = QtGui.QWidget()
			scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 325, 647))
			scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
			verticalLayout_3 = QtGui.QVBoxLayout(scrollAreaWidgetContents)
			verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
			scrollArea.setWidget(scrollAreaWidgetContents)
			verticalLayout_4.addWidget(scrollArea)
			self.tabWidget.addTab(tab_3, _fromUtf8(""))
			self.tabWidget.setTabText(self.tabWidget.indexOf(tab_3), _translate("Dialog", categoria, None))
			self.tabs[categoria]=[scrollAreaWidgetContents, verticalLayout_3]			
		self.tabWidget.setCurrentIndex(0)

	

    	def criarBotao(self, nomeB, nomeF):
		pushButton = QtGui.QPushButton(self.tabs.get(self.DB.get(nomeF))[0])			
		if nomeF[-1:] == "P":			
			pushButton.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);background-color: rgb(0, 0, 255);"))
		elif nomeF[-1:]  == "L":			
			pushButton.setStyleSheet(_fromUtf8("background-color: rgb(21, 7, 7);color: rgb(255, 255, 255);"))
		elif nomeF[-1:]  == "D":			
			pushButton.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 0);"))
		elif nomeF[-1:] == "C":		
			pushButton.setStyleSheet(_fromUtf8("background-color: rgb(85, 255, 0);"))
		elif nomeF[-1:]  == "A":
			pushButton.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);background-color: rgb(246, 13, 13);"))			
		pushButton.setObjectName(_fromUtf8(_fromUtf8(nomeB)))
		self.tabs.get(self.DB.get(nomeF))[1].addWidget(pushButton)
		pushButton.setText(_translate("Dialog",_fromUtf8(nomeB), None))
		pushButton.clicked.connect(lambda:self.setNomeBotao(pushButton))
		return pushButton
		

	def setNomeBotao(self, b):
		self.NomeBotao = b.objectName()

    	def obterNomeBotao(self):
		return self.NomeBotao	


	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "      Menu de Reambulação", None))
		self.label.setText(_translate("Dialog", " Centroide ", None))
		self.label_2.setText(_translate("Dialog", "Delimitador", None))
		self.label_5.setText(_translate("Dialog", "    Área   ", None))
		self.label_3.setText(_translate("Dialog", "    Linha   ", None))
		self.label_4.setText(_translate("Dialog", "   Ponto  ", None))	

	def run(self): 
		self.iface.mapCanvas().setMapTool(self.tool)
		
	def out(self):
		self.iface.mapCanvas().unsetMapTool(self.tool)
		try:		
			self.Dialog.close()
		except:
			pass
	def getValueSelection(self):
		return self.tool.getValue()

	def runBackup(self):
		self.Dialog = QtGui.QDialog(self.iface.mainWindow())
      		self.menu2 = Ui_Backup(self.Dialog, self.iface)   
      		self.Dialog.show()
	

	def openForm(self):
             
		self.iface.activeLayer().startEditing() 
		self.formValor={}
		comboV={}
		if (self.iface.activeLayer().selectedFeaturesIds() != []) and (len(self.iface.activeLayer().selectedFeaturesIds()) == 1):

			for x in self.iface.activeLayer().pendingAllAttributesList():
				if (self.iface.activeLayer().valueMap(x).keys() != []) and (self.iface.activeLayer().valueMap(x).keys()[0] != u'UseHtml') :
					for nome in self.iface.activeLayer().valueMap(x):
						comboV[self.iface.activeLayer().valueMap(x).get(nome)]=nome
					self.formValor[self.iface.activeLayer().pendingFields()[x].name()]=[comboV.get(unicode(self.iface.activeLayer().selectedFeatures()[0].attribute(self.iface.activeLayer().pendingFields()[x].name())))]
					
				else:
					self.formValor[self.iface.activeLayer().pendingFields()[x].name()]=[unicode(self.iface.activeLayer().selectedFeatures()[0].attribute(self.iface.activeLayer().pendingFields()[x].name()))]
			
			self.formulario(self.formValor, self.iface.activeLayer().selectedFeaturesIds()[0])			
			
		elif len(self.iface.activeLayer().selectedFeaturesIds()) > 0:
			QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Há mais de uma feição selecionada:<br></font><font color=blue>Selecione apenas uma feição!</font>", QMessageBox.Close)
		elif len(self.iface.activeLayer().selectedFeaturesIds()) == 0:
			QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Selecione uma feição!</font>", QMessageBox.Close)
		
	     	
	    
        def formulario(self, form , ID):
			self.dialog3 = QtGui.QDialog(self.iface.mainWindow())
			self.form3 = Dialog(self.dialog3, self.iface)
			self.criarCampos1(form)
			self.form3.linha()
			self.form3.criarBotoes()   
			self.dialog3.show()
			QObject.connect(self.form3.pushButton_2, SIGNAL("clicked()"), self.dialog3.close)
			QObject.connect(self.form3.pushButton, SIGNAL("clicked()"), lambda:self.form3.valorCampos(ID, self.form3.obter_FormV(), self.dialog3))	

	def criarCampos1(self, valorPadrao):

		grupoType={}		
		for x in self.iface.activeLayer().pendingAllAttributesList():	
			grupoType[self.iface.activeLayer().pendingFields()[x].name()]=self.iface.activeLayer().pendingFields()[x].typeName()	

		for index in self.iface.activeLayer().pendingAllAttributesList():			
			if not index == 0:
				
				try:
				
				  	if self.iface.activeLayer().valueMap(index).keys()[0] != "UseHtml":
						
				  	  self.form3.criarCombo(unicode( self.iface.activeLayer().pendingFields()[index].name()), self.iface.activeLayer().valueMap(index), valorPadrao.get(self.iface.activeLayer().pendingFields()[index].name()))

				    	 
				  	else:

				    	   self.form3.criarLine(unicode(self.iface.activeLayer().pendingFields()[index].name()), grupoType.get(unicode(self.iface.activeLayer().pendingFields()[index].name())), valorPadrao.get(self.iface.activeLayer().pendingFields()[index].name()) )
				except:

			  		self.form3.criarLine(unicode(self.iface.activeLayer().pendingFields()[index].name()), grupoType.get(unicode(self.iface.activeLayer().pendingFields()[index].name())), valorPadrao.get(self.iface.activeLayer().pendingFields()[index].name()))

	
	
	
        def removeSelecoes(self):
		for i in range(len(self.iface.mapCanvas().layers())):
			try:
				self.iface.mapCanvas().layers()[i].removeSelection()
			except:
				pass	
	
	
        



    











