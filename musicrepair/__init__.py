#!/usr/bin/env python

'''
MusicNow :)
'''

from os import system, rename, listdir
from sys import version_info

import json
from bs4 import BeautifulSoup
import requests


from mutagen.id3 import ID3, APIC, USLT
from mutagen.mp3 import EasyMP3

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
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})
    try:
        link = link.get('href')
        link = requests.get(link)

        soup = BeautifulSoup(link.text, "html.parser")

        album_div = soup.find('div', {'id': 'albums'})
        title_div = soup.find('div', {'id': 'content_artist'}).find('h1')

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]
        except:
            lyrics = "Couldn't find lyrics"

        try:
            song_title = title_div.contents[0]
            song_title = song_title[1:-8]
        except Exception:
            print("Couldn't reset song title")
            song_title = song_name

        try:
            artist = title_div.contents[1].getText()
        except Exception:
            print("Couldn't find artist name")
            artist = "Unknown"

        try:
            album = album_div.find('a').contents[0]
            album = album[:-7]
        except Exception:
            print("Couldn't find the album name")
            album = artist

    except:
        print("Couldn't find song details")

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
              "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
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
    except:
        print("Could not add album art")
    try:
        audio = EasyMP3(song_title, ID3=ID3)
        try:
            audio.add_tags()
        except Exception:
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

    except Exception:
        print("An Error occured while adding the album art")


def add_details(file_name, song_title, artist, album, lyrics):
    '''
    Adds the details to song
    '''

    print(" \n\nSong name : %s \n\nArtist : %s \n\nAlbum : %s \n\n " % (
        song_title, artist, album))

    try:
        tags = EasyMP3(file_name)
        tags["album"] = album
        tags["title"] = song_title
        tags["artist"] = artist
        tags.save()

        tags = ID3(file_name)
        tags["USLT::'eng'"] = (
            USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics))

        tags.save(file_name)

    except Exception:
        print("Couldn't add song details")

    try:
        rename(file_name, song_title + '.mp3')
    except:
        pass


def search():
    '''
    Searches for '.mp3' files in current directory and checks whether they already contain tags or not.
    '''
    files = [f for f in listdir('.') if f[-4:] == '.mp3']
    for file_name in files:
        tags = EasyMP3(file_name)
        try:
            print("%s already has tags " % tags["album"][0])
        except:

            print("%s Adding metadata" % file_name)
            artist, album, song_name, lyrics = get_details(file_name)
            albumart = get_albumart(album)

            add_albumart(albumart, file_name)
            add_details(file_name, song_name, artist, album, lyrics)


system('clear')

