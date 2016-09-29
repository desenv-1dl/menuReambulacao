# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4 import uic
import psycopg2, sys, os, csv, resources, interface_menu, qgis.utils, time
from PyQt4.QtCore import QSettings
from MultiLayerSelection import *
from interface_menu import *
from interface_form import *
from selectConnection import SelectConnection
from PyQt4.QtCore import QT_TR_NOOP as tr
import os

class menuAquisicao:
	def __init__(self, iface):
		self.iface = iface
	   
	def initGui(self):
		self.action = QAction(QIcon(":/plugins/menuReambulacao/icon.png"), u"Menu de Reambulação", self.iface.mainWindow())
		self.action.setObjectName("testAction")
		self.action.setWhatsThis("Configuration Menu plugin")
		self.action.setStatusTip("This is status tip")
		QObject.connect(self.action, SIGNAL("triggered()"), self.selectCon)
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToMenu(u"&Menu de Aquisição", self.action)    
		self.iface.actionAddFeature().toggled.connect(self.desconectarMenu1)
		self.iface.layerTreeView().clicked.connect(self.desconectarMenu1)
		self.iface.legendInterface().itemAdded.connect(self.desconectarMenu2)

	def unload(self):	
		self.iface.removePluginMenu(u"&Menu de Aquisição", self.action)
		self.iface.removeToolBarIcon(self.action)
		try:
			self.MainWindow.close()
		except:
			pass
		
	def selectCon(self):
		dialog = QtGui.QDialog(self.iface.mainWindow())
		d = SelectConnection(dialog)
		self.addCon(d)
		d.okButton.clicked.connect(lambda:self.run(d, dialog))
		dialog.show()
	
	def addCon(self, d):
		s = QSettings()
		s.beginGroup("PostgreSQL/connections")
		try:
			connects=[]
			for x in s.allKeys():
				if  x[-9:] == "/username":
					connects.append(x[:-9])
			d.listConCombo.addItems(connects)
		except:		
			QMessageBox.warning(self.iface.mainWindow(),"ERRO", u"Erro ao ler 'Conexões'")
		
	def run(self, c, d):
		#try:
			db = c.listConCombo.currentText().replace(" ","")
			d.close()
			self.action.setEnabled(False)
			self.conectarDB(db)
			self.abrirMenu(db)	
		#except:
			#QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Não conectado ao Banco de dados:<br></font><font color=blue>Tente conectar e salvar seu 'Usuário' , sua 'Senha' e a 'Máquina'!</font>", QMessageBox.Close)
			#self.action.setEnabled(True)

 	def conectarDB(self, db):		
	    self.s = QSettings()
	    self.s.beginGroup("PostgreSQL/connections")
	    self.a=db+"/host"
	    self.b=db+"/port"
	    self.c=db+"/database"
	    self.d=db+'/username'
	    self.e=db+'/password'
	    self.dataBase = db
	    conn_string = "host="+self.s.value(self.a)+" dbname="+self.s.value(self.c)+" user="+self.s.value(self.d)+" password="+self.s.value(self.e)+" port="+self.s.value(self.b)
	    conn = psycopg2.connect(conn_string)
	    cursor = conn.cursor()
	    cursor.execute("SELECT schemaname, tablename FROM pg_tables order by schemaname;")
	    self.records = cursor.fetchall()
	    self.uri = QgsDataSourceURI()
	    self.uri.setConnection(self.s.value(self.a), self.s.value(self.b), self.s.value(self.c), self.s.value(self.d), self.s.value(self.e))
	    self.leituradb={}
	    for x in range(len(self.records)):
			self.leituradb[self.records[x][1]]=self.records[x][0]    
	    cursor.execute("SELECT tablename FROM pg_tables where schemaname = 'DOMINIOS' order by schemaname;")
	    self.records2 = cursor.fetchall()
	    self.listaCampos=[]
	    for i in self.records2:
			self.listaCampos.append(i[0])
	    self.listaValores={}    
	    cursor.execute("select conname from pg_constraint;")
	    self.records3 = cursor.fetchall()
	    self.listaDominios=[]
	    for nome in self.records3:
			cursor.execute("select consrc from pg_constraint where conname = '"+nome[0]+"' ;")
			teste = cursor.fetchall()[0][0]
			if teste != None :
				teste2 = teste.split(" ")[0].replace("(", "").replace("\"","")
				if not (teste2.endswith(")") or teste2.endswith(",") or teste2.endswith("]")):
					self.listaDominios.append(teste2)       
	    for campo in self.listaCampos:
			grupo=[]
			cursor.execute("SELECT * FROM \"DOMINIOS\".\""+campo+"\";")
			self.records4 = cursor.fetchall()
			for vl in self.records4:
				grupo.append(vl[1])
			self.listaValores[campo]=grupo
	    cursor.close()	    
   
	def abrirMenu(self, db):
		self.MainWindow = QtGui.QDialog(self.iface.mainWindow())
		self.menu = Ui_Dialog(self.MainWindow, self.iface, self.leituradb, db)
		self.menu.botaoSelecionarCsv.clicked.connect(self.selecioneCsv)   
		self.MainWindow.show()
		self.MainWindow.rejected.connect(self.sairMenu)
   
	def selecioneCsv(self):
		fileN = QtGui.QFileDialog(self.iface.mainWindow()).getOpenFileName()
		if fileN[-4:] == ".csv":
			self.lerCsv(fileN)
			self.menu.botaoSelecionarCsv.close()		
		elif (fileN[-4:] != ".csv") and (fileN[-4:] != "") :		
			QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Arquivo não compatível:<br></font><font color=blue>Selecione um Arquivo com extensão '.csv'!</font>", QMessageBox.Close)

	def sairMenu(self):
		if self.iface.activeLayer():
			self.iface.activeLayer().startEditing()
		try:
			self.iface.activeLayer().setFeatureFormSuppress(False)
		except:
			pass
		try:
			self.iface.activeLayer().featureAdded.disconnect(self.formulario)
		except:
			pass
		self.action.setEnabled(True)

  	def desconectarMenu1(self):
		try:
			self.iface.activeLayer().setFeatureFormSuppress(False)
		except:
			pass
		try:
			self.iface.activeLayer().featureAdded.disconnect(self.formulario)
		except:
			pass

  	def desconectarMenu2(self):
		try:
			self.iface.activeLayer().setFeatureFormSuppress(False)
		except:
			pass

	def lerCsv(self, file1):
		self.relatorioDeErros=[]
		self.conjBot=[]	
		self.atributagem={}
		linhaCsv=2
		conjuntoBotaoFeicao=[]
		conjuntoCategorias=[]
		fileC=open(file1, 'rb')
		for linha in fileC:					
			if not linha.startswith("CATEGORIA"):   
				linha=linha.replace("\n","").split(",")
				validar= linha[2:]
				nomeBot=unicode(linha[1], "utf-8")
				nomeCamada=unicode(linha[2].replace(" ",""), "utf-8")
				self.atributagem[nomeBot]={}
				self.atributagem[nomeBot][nomeCamada]={}
				index=3			
				for i in range(len(linha)-3):
					if len(linha[index].split(":")) > 1:
						campo=unicode(linha[index].split(":")[0], "utf-8")
						valor1=unicode(linha[index].split(":")[1].replace("\r","").replace("\n",""), "utf-8")						
						if len(linha[index].split(":")) == 3:
							valor2=unicode(linha[index].split(":")[2], "utf-8")					
							self.atributagem[nomeBot][nomeCamada][campo]=[valor1, valor2]
							index+=1							
						elif len(linha[index].split(":")) == 2:
							self.atributagem[nomeBot][nomeCamada][campo]=[valor1]
							index+=1							                       	
				conjuntoCategorias.append(self.leituradb.get(nomeCamada))
				conjuntoBotaoFeicao.append([nomeBot, nomeCamada, campo, valor1])			
				linhaCsv+=1
		conjuntoCategoria = list(set(conjuntoCategorias))
		self.menu.criarTab(conjuntoCategoria)		
		for botaofeicao in conjuntoBotaoFeicao:		
			bot = self.menu.criarBotao(botaofeicao[0], botaofeicao[1])
			bot.clicked.connect(self.definirAcao)	

	def definirAcao(self):
		botao=self.menu.obterNomeBotao()		
		selecaoQgis=[]
		contador=0
		camada= self.atributagem.get(botao).keys()[0]
		selecionado = self.iface.mapCanvas().layers()
		for x in range(len(selecionado)):
			try:
				if self.iface.mapCanvas().layers()[x].selectedFeatureCount() > 0 :
					selecaoQgis.append(self.iface.mapCanvas().layers()[x].name())
					contador+=1
			except:
				pass
		if contador != 0:
				if self.menu.getValueSelection() != []:
					if self.menu.getValueSelection()[0][-1:] == camada[-1:]:
						self.cortaCola(camada, botao)
					else:
						QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Você não pode recorta e colar Feições de geometrias diferentes:</font><br><font color=blue>Tente recorta e colar feições de mesma geometria!</font>", QMessageBox.Close)
				else:
					if selecaoQgis[0][-1:] == camada[-1:]:
						self.cortaCola(camada, botao)
					else:
						QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Você não pode recorta e colar Feições de geometrias diferentes:</font><br><font color=blue>Tente recorta e colar feições de mesma geometria!</font>", QMessageBox.Close)
			
		else:		
			self.addCamada(camada, botao)



  
	def addCamada(self, camada, botao):		
		self.formTeste=[]	
		layers = QgsMapLayerRegistry.instance().mapLayers()
		grupo={}
		for x in range(len(layers)):
			if self.dataBase == layers[layers.keys()[x]].dataProvider().dataSourceUri().split(' ')[0][8:-1]:
				grupo[layers.keys()[x][:-17]]=layers.get(layers.keys()[x])
		if camada in grupo.keys():
			try:
				self.iface.activeLayer().setFeatureFormSuppress(False)
			except:
				pass
			try:
				self.iface.activeLayer().featureAdded.disconnect(self.formulario)
			except:
				pass
			self.iface.setActiveLayer(grupo.get(camada))
			self.iface.activeLayer().startEditing()
			self.iface.actionAddFeature().trigger()	
			self.iface.activeLayer().setFeatureFormSuppress(True)				
			self.botao1=botao			
			self.iface.activeLayer().featureAdded.connect(self.formulario)			
		else:
			try:
				self.iface.activeLayer().setFeatureFormSuppress(False)
			except:
				pass
			try:
				self.iface.activeLayer().featureAdded.disconnect(self.formulario)
			except:
				pass
			self.uri.setDataSource(str(self.leituradb.get(camada)), str(camada), "geom", "", "id" )
		 	vlayer = QgsVectorLayer(self.uri.uri(), str(camada), "postgres")
			QgsMapLayerRegistry.instance().addMapLayer(vlayer)
			self.iface.activeLayer().startEditing()
			self.iface.activeLayer().loadDefaultStyle()
			self.iface.actionAddFeature().trigger()
			self.iface.activeLayer().setFeatureFormSuppress(True)
			self.botao1=botao
			self.iface.activeLayer().featureAdded.connect(self.formulario)

	def cortaCola(self, camada, botao):	
		layers = QgsMapLayerRegistry.instance().mapLayers()
		grupo={}
		for x in range(len(layers)):
			if self.dataBase == layers[layers.keys()[x]].dataProvider().dataSourceUri().split(' ')[0][8:-1]:
				grupo[layers.keys()[x][:-17]]=layers.get(layers.keys()[x])
		if camada in grupo.keys():
			self.iface.setActiveLayer(grupo.get(camada))
		else:
			self.uri.setDataSource(str(self.leituradb.get(camada)), str(camada), "geom", "", "id" )
		 	vlayer = QgsVectorLayer(self.uri.uri(), str(camada), "postgres")
			QgsMapLayerRegistry.instance().addMapLayer(vlayer)	
			self.iface.activeLayer().loadDefaultStyle()
		self.formulario2(botao)

  	def formulario(self, featureAdded ):
		if self.iface.activeLayer() :        	    
			if (not featureAdded in self.formTeste) and (featureAdded < 0):
				self.formTeste.append(featureAdded)
				self.dialog = QtGui.QDialog(self.iface.mainWindow())
				self.form1 = Dialog(self.dialog, self.iface)
				self.form1.criarCampos(self.botao1, self.atributagem)
				self.form1.linha()
				self.form1.criarBotoes()   
				self.dialog.show()
				self.dialog.rejected.connect(lambda:self.fechar(featureAdded))
				QObject.connect(self.form1.pushButton_2, SIGNAL("clicked()"), lambda:self.fechar(featureAdded))
				QObject.connect(self.form1.pushButton, SIGNAL("clicked()"), lambda:self.form1.valorCampos(featureAdded, self.form1.obter_FormV(), self.dialog))	

	def formulario2(self, botao):
		if self.menu.getValueSelection() <> []:
			if self.iface.activeLayer() :	 	    
				self.dialog2 = QtGui.QDialog(self.iface.mainWindow())
				self.form2 = Dialog(self.dialog2, self.iface)
				self.form2.criarCampos(botao, self.atributagem)
				self.form2.linha()
				self.form2.criarBotoes()   
				self.dialog2.show()
				QObject.connect(self.form2.pushButton_2, SIGNAL("clicked()"), self.dialog2.close)
				QObject.connect(self.form2.pushButton, SIGNAL("clicked()"), lambda:self.valorCamposCC(self.form2.obter_FormV()))
		elif self.menu.getValueSelection() == []:
			QMessageBox.warning(self.iface.mainWindow(), u"ERRO:", u"<font color=red>Não há feições selecionadas:</font><br><font color=blue>Tente selecionar as feições com a ferramenta de seleção do 'Menu'!</font>", QMessageBox.Close)

	def valorCamposCC(self, valor):	
		destino = self.iface.activeLayer().name()
		origem = self.menu.getValueSelection()
		self.valor=valor
		self.dialog2.accept()
		layers = QgsMapLayerRegistry.instance().mapLayers()
		grupo={}
		for x in range(len(layers)):
			if self.dataBase == layers[layers.keys()[x]].dataProvider().dataSourceUri().split(' ')[0][8:-1]:
				grupo[layers.keys()[x][:-17]]=layers.get(layers.keys()[x])
		entre=True    
		for nome in origem:
			self.teste2=0
			self.iface.setActiveLayer(grupo.get(nome))
			grupoIds = self.iface.activeLayer().selectedFeaturesIds()
			self.iface.activeLayer().removeSelection()
			self.teste1=len(grupoIds)
			for ID in grupoIds:
				self.iface.setActiveLayer(grupo.get(nome))
				self.iface.activeLayer().select(ID)
				self.iface.activeLayer().startEditing()
				self.iface.actionCutFeatures().trigger()
				self.iface.setActiveLayer(grupo.get(destino))
				if entre:
					try:
						self.iface.activeLayer().featureAdded.disconnect(self.formulario)
					except:
						pass
					entre=False		
				self.iface.activeLayer().startEditing()
				self.iface.activeLayer().featureAdded.connect(self.atributar)
				self.iface.actionPasteFeatures().trigger()
				self.iface.activeLayer().removeSelection()
			if self.teste1 == self.teste2:			
					#self.save()
					pass
		for nome in origem:	
			self.iface.setActiveLayer(grupo.get(nome))	
			#self.save()
		self.iface.setActiveLayer(grupo.get(destino))

	def atributar(self, ID):
		self.teste2+=1		
		idt=ID
		grupoAttr={}
		for x in self.iface.activeLayer().pendingAllAttributesList():	
			grupoAttr[self.iface.activeLayer().pendingFields()[x].name()]=x
		for campo in self.valor.keys():
			if (campo[:-2] in grupoAttr) :
				if unicode(campo[-2:]) == u"LE":
					if self.valor.get(campo) == u'':
						idx = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))
						self.iface.activeLayer().changeAttributeValue(idt , idx, None)
					else:
						idx = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))
						self.iface.activeLayer().changeAttributeValue(idt , idx, self.valor.get(campo))
				
				else:				
					idx2 = self.iface.activeLayer().fieldNameIndex(unicode(campo[:-2]))
					self.iface.activeLayer().changeAttributeValue(idt , idx2, self.iface.activeLayer().valueMap(grupoAttr.get(unicode(campo[:-2]))).setdefault(unicode(self.valor.get(campo))))
		self.iface.activeLayer().featureAdded.disconnect(self.atributar)

	def fechar(self, ID):
		self.removeSelecoes()		
		self.iface.activeLayer().select(ID)
		self.iface.activeLayer().deleteSelectedFeatures()
		self.removeSelecoes()
		self.dialog.close()
		self.iface.mapCanvas().refresh()

	def removeSelecoes(self):
		for i in range(len(self.iface.mapCanvas().layers())):
			try:
				self.iface.mapCanvas().layers()[i].removeSelection()
			except:
				pass	

 
  







