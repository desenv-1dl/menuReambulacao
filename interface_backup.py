# -*- coding: utf-8 -*-


import os
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QSettings
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import qgis.utils

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

class Ui_Backup(object):
    def __init__(self, Dialog, iface):
	self.iface=iface
	self.Dialog=Dialog
        self.Dialog.setObjectName(_fromUtf8("Dialog"))
        self.Dialog.setStyleSheet(_fromUtf8("background-color: rgb(205,205,205);"))
	self.verticalLayout = QtGui.QVBoxLayout(self.Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))        
        self.label = QtGui.QLabel(self.Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)        	
        self.pushButton_3 = QtGui.QPushButton(self.Dialog)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.verticalLayout.addWidget(self.pushButton_3)
	self.pushButton_3.clicked.connect(self.backup)
        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "BACKUP:", None))
        self.label.setText(_translate("Dialog", "Crie arquivo com extensão (.sql) para Salvar o 'BACKUP':", None))
        self.pushButton_3.setText(_translate("Dialog", "GERAR BACKUP", None))
  	
    def backup(self):
	    try:
		    self.filename = QtGui.QFileDialog(self.iface.mainWindow()).getSaveFileName()
		    self.s = QSettings()
		    self.s.beginGroup("PostgreSQL/connections")
		    self.a=self.s.value(u'selected')+"/host"
		    self.b=self.s.value(u'selected')+"/port"
		    self.d=self.s.value(u'selected')+'/username'
		    self.e=self.s.value(u'selected')+'/password'

		    db = str(self.s.value(u'selected'))
		    user=str(self.s.value(self.d))
		    backupdir=str(self.filename)
		    date = time.strftime('%Y-%m-%d')
		    if backupdir[-4:] == ".csv":
		    	print backupdir
		    	print date
		    os.popen("pg_dump -U%s -d%s > %s" % (user , db, backupdir))
		    #self.feito()
	    except:
	   	QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Erro ao realizar o 'BACKUP'!</font>", QMessageBox.Close)

    def feito(self):
	QMessageBox.information(self.iface.mainWindow(), u"INFORMAÇÃO:", u"<font color=green>'BACKUP' realizado com sucesso!</font>", QMessageBox.Close)
	self.Dialog.close()















   
    

