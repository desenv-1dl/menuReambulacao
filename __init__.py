# -*- coding: utf-8 -*-

from main import menuAquisicao    


def name():
    return "Menu de Reambulação"

def description():
    return "Menu para torna mais automotizada a aquisição"

def version():
    return "Version 0.1"

def classFactory(iface):
    from main import menuAquisicao
    return menuAquisicao(iface)

def qgisMinimumVersion():
    return "2.0"

def author():
    return "sam"

def email():
    return "me@hotmail.com"

def icon():
    return "icon.png"

