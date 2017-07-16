from os import listdir, path 
import sys
import re
import shutil

DEBUG = True

def lista_archivos(directorio, tipo, recursividad):
    extensiones = {'Video':['avi','div','divx','dvd','flv','mkv','mov','mp4','mpg','mpeg','wmv'],
                   'Audio':['mp3','aac','wma','m4a'],
                   'Imagen':['gif','jpg','jpeg','bmp','png']}
    archivos = recorrerDir(directorio)
    listaPedida = []
    dirInteriores = []
    for i in archivos:
        temporal = directorio + '/' + i
        if path.isfile(temporal):
            partes = i.split('.')
            if partes[-1].lower() in extensiones[tipo]:
                listaPedida.append(i)
        elif path.isdir(temporal) and recursividad == 'Si':
            dirInteriores.append(temporal) 
    for i in dirInteriores:
        listaPedida.extend(lista_archivos(i,tipo))
    return listaPedida

def recorrerDir(directorio):
    return listdir(directorio)

def mover_archivos(lista):
    for archivo in lista:
        if (isChapter(archivo)):
            ubicarCapitulo(archivo)
        else:
            ubicarPelicula(archivo)
    return

def isChapter(archivo):
    series_regex = ".[Ss][0-9][0-9][eE][0-9][0-9]"
    pattern = re.compile(series_regex)
    return pattern.match(archivo)

def ubicarCapitulo(archivo):
    if(DEBUG):
        print "moviendo capitulo: " + archivo
        return 
    return

def ubicarPelicula(archivo):
    if(DEBUG):
        print "moviendo pelicula: " + archivo
        return
    shutil.move(archivo, FILMS_DIR) 
    return

def main():
    tipo = 'Video'
    recursivo = 'Si'
    lista = lista_archivos(DOWNLOADS_DIR,tipo,recursivo)
    mover_archivos(lista)
    print 'Programa Finalizado - '+str(len(lista))+' archivos encontrados.'

DOWNLOADS_DIR="../Downloads"
FILMS_DIR= sys.argv[1] + "Media/Films"
SERIES_DIR = sys.argv[1] + "Media/Series"
main()
