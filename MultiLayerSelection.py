# -*- coding: utf-8 -*-
from qgis.gui import *
from qgis.core import *
from PyQt4.Qt import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence

selecaoVar=[]
class MultiLayerSelection(QgsMapTool):
	
	def __init__(self, canvas, iface):
		self.iface=iface        
		self.canvas = canvas
		self.active = False
		self.selecaoVariada=[]
		QgsMapTool.__init__(self, self.canvas)
		
	def getValue(self):
		self.selecaoVariada =  list(set( self.selecaoVariada ))
		return self.selecaoVariada

	def canvasPressEvent(self, e):
		self.removerSelecoes()
		contador=0
		selecionado = self.iface.mapCanvas().layers()
		for x in range(len(selecionado)):
			try:
				if self.iface.mapCanvas().layers()[x].selectedFeatureCount() > 0 :
					contador+=1
			except:
				pass
		if contador == 0:
			self.selecaoVariada=[]
			self.testeGeom=""		
		layers = self.canvas.layers()	
		layer2 = QgsMapLayerRegistry.instance().mapLayers()	
		grupo={}
		for x in range(len(layer2)):
			grupo[layer2.keys()[x][:-17]]=layer2.get(layer2.keys()[x])    		
		p = self.toMapCoordinates(e.pos())
		w = self.canvas.mapUnitsPerPixel() * 10
		rect = QgsRectangle(p.x()-w, p.y()-w, p.x()+w, p.y()+w)
		for layer in layers:
			if layer.type() == QgsMapLayer.RasterLayer:
				continue
			if (self.testeGeom != "") and (self.testeGeom == layer.name()[-1:]):
				lRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)			   
				layer.select(lRect, False)
				if layer.selectedFeatureCount() == 1 and (not layer.name() in self.selecaoVariada):#                
					self.selecaoVariada.append(layer.name())
					self.iface.setActiveLayer(grupo.get(layer.name()))
					self.iface.activeLayer().startEditing()		
                                                                        
			elif (self.testeGeom == "") and (layer.name()[-1:]== "P" or \
					layer.name()[-1:]== "A" or layer.name()[-1:]=="L" or layer.name()[-1:]=="C" or layer.name()[-1:]=="D"):
				lRect = self.canvas.mapSettings().mapToLayerCoordinates(layer, rect)			   
				layer.select(lRect, False)				
				if layer.selectedFeatureCount() == 1 and (not layer.name() in self.selecaoVariada):
					self.testeGeom=layer.name()[-1:]				
					self.selecaoVariada.append(layer.name())
					self.iface.setActiveLayer(grupo.get(layer.name()))
					self.iface.activeLayer().startEditing()
		maisDeUm = 0
		for layer in layers:		
			if (layer.name()[-1:]== "P" or layer.name()[-1:]== "A" or \
				layer.name()[-1:]=="L" or layer.name()[-1:]=="C" or layer.name()[-1:]=="D"):
				if len(layer.selectedFeatures()) > 1:
					layer.removeSelection()
				if len(layer.selectedFeatures()) == 1:
					maisDeUm+=1
		if maisDeUm > 1:
			self.removerSelecoes()                                             
                       
	def deactivate(self):
		if self is not None:
			QgsMapTool.deactivate(self)

	def activate(self):
		QgsMapTool.activate(self)

	
	def removerSelecoes(self):
		for i in range(len(self.iface.mapCanvas().layers())):
			try:
				self.iface.mapCanvas().layers()[i].removeSelection()
			except:
				pass
		self.selecaoVariada=[]
		self.testeGeom=""
		






