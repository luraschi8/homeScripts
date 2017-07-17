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
                listaPedida.append(temporal)
        elif path.isdir(temporal) and recursividad == 'Si':
            dirInteriores.append(temporal) 
    for i in dirInteriores:
        listaPedida.extend(lista_archivos(i,tipo, recursividad))
    return listaPedida

def recorrerDir(directorio):
    return listdir(directorio)

def mover_archivos(lista):
    series = []
    for archivo in lista:
        if (isChapter(archivo)):
            if (len(series) == 0):
                series = armar_lista_series()
            ubicarCapitulo(archivo,series)
        else:
            ubicarPelicula(archivo)
    return

def armar_lista_series():
    dirlist = [ item for item in os.listdir(SERIES_DIR) if os.path.isdir(os.path.join(SERIES_DIR, item.replace(" ","."))) ]
    print dirlist
    return dirlist

def isChapter(archivo):
    series_regex = ".[Ss][0-9][0-9][eE][0-9][0-9]"
    pattern = re.compile(series_regex)
    return pattern.match(archivo)

def ubicarCapitulo(archivo, series):
    serieEncontrada = ''
    for serie in series:
        nombre = serie.split('/')[-1].lower()
        if (archivo.lower().find(nombre) != -1):
            serieEncontrada = serie
            break
    if (serieEncontrada == ''):
        return
    if(DEBUG):
        print "moviendo capitulo: " + archivo + " a: " + serie
        return
    shutil.move(archivo, serieEncontrada) 
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
    print lista
    mover_archivos(lista)
    print 'Programa Finalizado - '+str(len(lista))+' archivos encontrados.'

DOWNLOADS_DIR="../Downloads"
FILMS_DIR= sys.argv[1] + "Media/Films"
SERIES_DIR = sys.argv[1] + "Media/Series"
print FILMS_DIR
print SERIES_DIR
main()
