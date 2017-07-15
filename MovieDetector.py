#Service that gets movies from yify-torrents.org
from datetime import datetime
from Movie import Movie
import requests
import json
import MySQLdb
import urllib2
import transmissionrpc

DOWNLOAD_DIR = "/home/pi/Torrents"
LOGFILE = "~/Scripts/crawler.log"
LOGMODE = "DEPLOY" #DEPLOY / DEBUG
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
DBHOST = "192.168.0.108"
DBNAME = "Torrents"
DBUSER = "xbmc"
DBPASS = "xbmc"

ARGENTEAM_TVSHOW  = "http://argenteam.net/api/v1/tvshow"
ARGENTEAM_EPISODE = "http://argenteam.net/api/v1/episode"


def addMovies(data, toadd):
        existent = getExistentMovies()
        limitYear = datetime.today().year - 1
        for mov in toadd:
            current = Movie()
            current.title = mov["title_long"]
            current.link = mov["url"]
            for tor in mov["torrents"]:
                if tor["quality"] == "1080p":
                    current.link1080p = tor["url"]
                elif tor["quality"] == "720p":
                    current.link720p = tor["url"]
                elif tor["quality"] == "3D":
                    current.link3D = tor["url"]
            if (current.title in existent):
                return False, data
            elif mov["year"] >= limitYear:
                data.append(current)
        return True, data


def getNewMovies():
        newMovies = True
        page = 1
        newMoviesList = []
        while newMovies:
            response = requests.get("https://yts.ag/api/v2/list_movies.json?limit=25&page=" + str(page) )
            if response.status_code != 200 :
                writeToLog(ERROR, "Error connecting to API page " + page +".")
                return []
            data = response.json()
            newMovies, newMoviesList = addMovies(newMoviesList, data["data"]["movies"])
            page += 1
        return newMoviesList

def getNewSeries(listaSeries):
    for serie in listaSeries:
        response = requests.get(ARGENTEAM_TVSHOW + "?id=" + str(serie["serieID"]) )
        if response.status_code != 200 :
            writeToLog(ERROR, "Error connecting to API serie " + serie +".")
        else:
            data = response.json()["seasons"]
            for season in data:
                if int(season["season"]) == serie["lastChapterSeason"]:
                    for episode in season["episodes"]:
                        if episode["number"] == 'XX':
                            continue
                        if int(episode["number"]) > serie["lastChapterNumber"]:
                            downloadEpisode(episode["id"], str(serie["serieID"]))
                if int(season["season"]) > serie ['lastChapterSeason']:
                    for episode in season["episodes"]:
                        if episode["number"] == 'XX':
                            continue
                        downloadEpisode(episode["id"], str(serie["serieID"]))

def addToTransmission(magnet):
    try:
        tc = transmissionrpc.Client('localhost', port=9091, user='admin', password='0310Matias')
        tor = tc.add_torrent(magnet)
        return True
    except:
        return False

def addToDB(episodeID, serieID, season, number, magnet):
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()   
    # Use all the SQL you like
    query = "INSERT INTO episodes (id, serieID, season, number, magnet) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(query, (episodeID, serieID, season, number, magnet))


def downloadEpisode(episodeID, serieID):
    response = requests.get(ARGENTEAM_EPISODE + "?id=" + str(episodeID) )
    if response.status_code != 200 :
        print "Error connecting to API episode " + str(episodeID) +"."
    else:
        data = response.json()["releases"]
        if len(data) == 0:
            print "No releases for episode " + str(episodeID) + " yet."
            return
        for release in data:
            if release['source'] == 'HDTV' and release['tags'] == '720p':
                if addToTransmission(release["torrents"][0]["uri"]):
                    addToDB(episodeID, serieID, response.json()['season'], response.json()['number'], release["torrents"][0]["uri"])
                else:
                    print "Error agregando torrent: " + release["torrents"][0]["uri"]
                return
        for release in data:
            if release['tags'] == '1080p':
                if addToTransmission(release["torrents"][0]["uri"]):
                    addToDB(episodeID, serieID, response.json()['season'], response.json()['number'], release["torrents"][0]["uri"])
                else:
                    print "Error agregando torrent: " + release["torrents"][0]["uri"]
                return

def getSeries():
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()   
    # Use all the SQL you like
    cur.execute("SELECT * FROM series")
    titulos = []
    for row in cur.fetchall():
        serie = {}
        serie["serieID"] = row[0]
        titulos.append(serie)
    #print titulos
    for serie in titulos:
        #print serie
        cur.execute("SELECT * FROM episodes WHERE serieID = '" + str(serie["serieID"]) + "' ORDER BY season DESC, number DESC LIMIT 1" )
        row = cur.fetchall()
        serie["lastChapterID"] = row[0][0]
        serie["lastChapterSeason"] = row[0][2]
        serie["lastChapterNumber"] = row[0][3]
    return titulos

def checkChapters():
    listaSeries = getSeries()
    getNewSeries(listaSeries)


def getExistentMovies():
        db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()   
        # Use all the SQL you like
        cur.execute("SELECT * FROM movies")
        titulos = set()
        for row in cur.fetchall():
                titulos.add(row[2])
        return titulos


def addNewMovieToDB(dbCursor, movie, state): 
        # Use all the SQL you like
        query = "INSERT INTO movies ( id, date, title, detailLink, link1080p, link720p, link3D, status) VALUES ( NULL, NULL, %s, %s, %s, %s, %s, %s)"
        dbCursor.execute(query, (movie.title, movie.link, movie.link1080p, movie.link720p, movie.link3D, state))
        

def writeToLog(type, message):
        time = datetime.now()
        f = open(LOGFILE, 'a')
        f.write(str(time) + "[" + type + "] - " + message + "\n")
        f.close()

def downloadAndAddToDB(movieList):
        db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DBNAME)

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()  
        for movie in movieList:
            state = "DOWNLOADED"
            if movie.link3D != "":
                downloadTorrent(movie.link3D, movie.title + ".torrent")
            elif movie.link1080p != "":
                downloadTorrent(movie.link1080p, movie.title + ".torrent")
            elif movie.link720p != "":
                downloadTorrent(movie.link720p, movie.title + ".torrent")
            else:
                writeToLog(WARNING, "No links for movie: " + movie.title +".")
                state = "NO_LINK"
            addNewMovieToDB(cur, movie, state)



def downloadTorrent(url, name):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(url, headers=hdr)
    torfile = urllib2.urlopen(req)
    try:
        output = open(DOWNLOAD_DIR + "/" + name,'wb')
    except UnicodeEncodeError:
        print "UnicodeError with file name."
        output = open(DOWNLOAD_DIR + "/errorName.torrent", 'wb')
    output.write(torfile.read())
    output.close()



def run():
        movieList = getNewMovies()
        downloadAndAddToDB(movieList)
        checkChapters()

run()
