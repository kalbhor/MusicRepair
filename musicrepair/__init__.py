#!/usr/bin/env python

'''
Tries to find the metadata of song based on the file name

https://github.com/lakshaykalbhor/MusicRepair
'''

from os import system, rename, listdir
from sys import version_info

import json
from bs4 import BeautifulSoup

from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File

if version_info[0] < 3:
    from urllib2 import urlopen, Request
    from urllib2 import quote
else:
    from urllib.parse import quote
    from urllib.request import urlopen, Request


def get_details(song_name):
    '''
    Gets the song details
    '''

    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})
    try:
        link = link.get('href')
        link = urlopen(link).read()

        soup = BeautifulSoup(link, "html.parser")

        album_div = soup.find('div', {'id': 'albums'})
        title_div = soup.find('div', {'id': 'content_artist'}).find('h1')

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]
        except AttributeError:
            lyrics = "     > Couldn't find lyrics"

        try:
            song_title = title_div.contents[0]
            song_title = song_title[1:-8]
        except AttributeError:
            print("    > Couldn't reset song title")
            song_title = song_name

        try:
            artist = title_div.contents[1].getText()
        except AttributeError:
            print("    > Couldn't find artist name")
            artist = "Unknown"

        try:
            album = album_div.find('a').contents[0]
            album = album[:-7]
        except AttributeError:
            print("    > Couldn't find the album name")
            album = artist

    except AttributeError:
        print("    > Couldn't find song details")

        album = song_name
        song_title = song_name
        artist = "Unknown"
        lyrics = ""

    return artist, album, song_title, lyrics


def get_albumart(album):
    '''
    Fetches the album art
    '''

    album = album + " Album Art"
    url = ("https://www.google.co.in/search?q=" +
           quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
    header = {'User-Agent':
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/43.0.2357.134 Safari/537.36"
             }

    soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

    albumart_div = soup.find("div", {"class": "rg_meta"})
    albumart = json.loads(albumart_div.text)["ou"]
    return albumart


def add_albumart(albumart, song_title):
    '''
    Adds the album art to the song
    '''

    try:
        img = urlopen(albumart)  # Gets album art from url

    except Exception:
        print("    > Could not add album art")
        return None

    audio = EasyMP3(song_title, ID3=ID3)
    try:
        audio.add_tags()
    except _util.error:
        pass

    audio.tags.add(
        APIC(
            encoding=3,  # UTF-8
            mime='image/png',
            type=3,  # 3 is for album art
            desc='Cover',
            data=img.read()  # Reads and adds album art
        )
    )
    audio.save()
    print("     >Added Album Art")


def add_details(file_name, song_title, artist, album, lyrics):
    '''
    Adds the details to song
    '''

    tags = EasyMP3(file_name)
    tags["album"] = album
    tags["title"] = song_title
    tags["artist"] = artist
    tags.save()

    tags = ID3(file_name)
    tags["USLT::'eng'"] = (
        USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics))

    tags.save(file_name)

    try:
        rename(file_name, song_title + '.mp3')
    except FileNotFoundError:
        pass

    print("\n\n     ~Song name : %s \n\n     ~Artist : %s \n\n     ~Album : %s \n\n " % (
        song_title, artist, album))


def search():
    '''
    Searches for '.mp3' files in current directory
    and checks whether they already contain tags or not.
    '''
    files = [f for f in listdir('.') if f[-4:] == '.mp3']
    for file_name in files:
        tags = File(file_name)
        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys():
            print("%s already has tags " % tags["TIT2"])

        elif not('APIC:Cover' in tags.keys()) and 'TALB' in tags.keys():
            album = tags["TALB"].text[0]
            print("........................\n")

            print("%s Adding metadata" % file_name)

            albumart = get_albumart(album)
            add_albumart(albumart, file_name)

        else:
            print("........................\n")

            print("%s Adding metadata" % file_name)
            artist, album, song_name, lyrics = get_details(file_name)
            albumart = get_albumart(album)

            add_albumart(albumart, file_name)
            add_details(file_name, song_name, artist, album, lyrics)


system('clear')
