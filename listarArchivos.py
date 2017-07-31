from os import listdir, path, getcwd 
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
                listaPedida.append(temporal)
        elif path.isdir(temporal) and recursividad == 'Si':
            dirInteriores.append(temporal) 
    for i in dirInteriores:
        listaPedida.extend(lista_archivos(i,tipo, recursividad))
    return listaPedida

def recorrerDir(directorio):
    return listdir(directorio)

def mover_archivos(lista):
    series = armar_lista_series()
    #print series
    for archivo in lista:
        if (isChapter(archivo)):
            ubicarCapitulo(archivo,series)
        else:
            ubicarPelicula(archivo)
    return

def armar_lista_series():
    #currentDir = getcwd()
    #direcorio = currentDir + SERIES_DIR[2:]
    dirlist = {}
    for item in listdir(SERIES_DIR):
        directorioCompleto = path.join(SERIES_DIR, item) 
        if path.isdir(directorioCompleto):
            dirlist[item.replace(" ",".").lower()] = directorioCompleto 
    #print dirlist
    return dirlist

def isChapter(archivo):
    series_regex = "[Ss][0-9][0-9][eE][0-9][0-9]"
    pattern = re.compile(series_regex)
    return pattern.search(archivo)

def ubicarCapitulo(archivo, series):
    serieEncontrada = ''
    for serie in series:
        if (archivo.lower().find(serie) != -1):
            serieEncontrada = serie
            break
    if (serieEncontrada == ''):
        print "carpeta no encontrada para archivo:" + archivo
        return
    if(DEBUG):
        print "moviendo capitulo: " + archivo + " a: " + series[serieEncontrada]
        return
    shutil.move(archivo, series[serieEncontrada]) 
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
    #print lista
    mover_archivos(lista)
    print 'Programa Finalizado - '+str(len(lista))+' archivos encontrados.'

DOWNLOADS_DIR="../Downloads"
FILMS_DIR= sys.argv[1] + "Films"
SERIES_DIR = sys.argv[1] + "Series"
print FILMS_DIR
print SERIES_DIR
main()
