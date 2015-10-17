# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function
__author__ = 'dtrillo'
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#reload(sys)
#sys.setdefaultencoding('utf-8')

import bs4
import ConfigParser
from downloads import Downloading
from partidosweb import PartidosWeb

HTML = ".html"
miVersion = "SEF LiveScore - Version 0.5.0 - 20140403"
iniurl = "url.ini"

#contenedores = [ "td", "td", "td" ]
#conte_clases = [ "fh", "fa", "fs" ]
contenedores = [ "div", "div", "div", "div" ]
conte_clases = [ "ply tright name", "ply name", "sco", "min"]



class LiveScore():
    """ Tratamiento de URL de BetFair """
    def __init__(self, misclaves, misvalores):
        self.partidos = []
        self.equipos = set()
        self.misclaves = misclaves
        self.misvalores = misvalores
        self.dw = Downloading('')
        for k in range(0, len(misclaves)):
            url = misvalores[k]
            html = self.descarga(url)
            self.ejecuta(html)
    def descarga(self, surl):
        data, error = self.dw.gethtml(surl,'')
        return data

    def ejecuta(self, data):
        soup = bs4.BeautifulSoup(data)
        locales = soup.findAll(contenedores[0], { "class" : conte_clases[0] })
        visitantes = soup.findAll(contenedores[1], { "class" : conte_clases[1] })
        marcador = soup.findAll(contenedores[2], { "class" : conte_clases[2] })
        minuto = soup.findAll(contenedores[3], { "class" : conte_clases[3] })
        self.partidos = map(lambda a, b, c, d: PartidosWeb(a.text, b.text, c.text, minuto=d.text), locales, visitantes, marcador, minuto)
        tmp = [x.text for x in locales]
        tmp2 = [x.text for x in visitantes]
        self.equipos = set(tmp)
        self.equipos.update(tmp2)


    def listadoPartidos(self):
        print ("Total equipos: %s" % len(self.equipos))
        for p in self.partidos:
            try:
                print (p)
            except: pass



class ini2urls():
    """ Recupera de ficheros INI el listado de URL a procesar """
    def __init__(self, fichero, numseccion = 0):
        self.fichero = fichero
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.fichero)
        self.secciones = self.config.sections()
        self.error = True if len(self.secciones) == 0 else False
        self.seccion = self.secciones[numseccion] if self.error == False else ''
        self.misclaves = []
        self.misvalores = []
        self.dicc = ()
        if self.error: print("ERROR - Fichero INI no es el esperado!")
        if self.error == False:
            self.misclaves = self.config.options(self.seccion)
        for k in self.misclaves:
            tmp = self.config.get(self.seccion,k)
            self.misvalores.append(tmp)
            #self.dicc = tmp
    def claves_valores(self):
        return  self.misclaves, self.misvalores

    def listado(self):
        """ Listado de URL recuperadas """
        for i in range(0, len(self.misclaves)):
            print (self.misclaves[i] + " - " + self.misvalores[i])


if __name__ == '__main__':
    print (miVersion)
    listadoURLs = ini2urls(iniurl,0)    # Lectura de URL desde fichero de INICIO
    keys, vlr = listadoURLs.claves_valores()  # Claves y valores

    listadoURLs.listado()
    ls = LiveScore(keys, vlr)
    ls.listadoPartidos()