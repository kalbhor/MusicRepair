#!/usr/bin/env python

'''
Tries to find the metadata of songs based on the file name
https://github.com/lakshaykalbhor/MusicRepair
'''

from . import albumsearch
from . import improvename

import argparse
from os import rename, listdir, chdir
import difflib
import six

from bs4 import BeautifulSoup

from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File

import spotipy

if six.PY2:
    from urllib2 import urlopen, Request
    from urllib2 import quote
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen, Request



def matching_details(song_name, song_title, artist):
    '''
    Provides a score out of 10 that determines the
    relevance of the search result
    '''

    match_name = difflib.SequenceMatcher(None, song_name, song_title).ratio()
    match_title = difflib.SequenceMatcher(None, song_name, artist).ratio()

    if match_name >= 0.55 or (match_name < 0.55 and match_title >= 0.45):
        return True, match_name

    else:
        return False, (match_name + match_title) / 2


def get_lyrics(song_name):
    '''
    Scrapes the lyrics of a song since spotify does not provide lyrics
    takes song title as arguement
    '''

    lyrics = ""
    url = "http://search.letssingit.com/cgi-exe/am.cgi?a=search&artist_id=&l=archive&s=" + \
        quote(song_name.encode('utf-8'))
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    link = soup.find('a', {'class': 'high_profile'})

    try:
        link = link.get('href')
        link = urlopen(link).read()
        soup = BeautifulSoup(link, "html.parser")

        try:
            lyrics = soup.find('div', {'id': 'lyrics'}).text
            lyrics = lyrics[3:]

        except AttributeError:
            lyrics = ""

    except:
        lyrics = ""

    return lyrics


def get_details_spotify(song_name):
    '''
    Tries finding metadata through Spotify
    '''

    song_name = improvename.songname(song_name)

    spotify = spotipy.Spotify()
    results = spotify.search(song_name, limit=1)  # Find top result

    print('*Finding metadata from Spotify.')

    try:
        album = (results['tracks']['items'][0]['album']['name'])  # Parse json dictionary
        artist = (results['tracks']['items'][0]['album']['artists'][0]['name'])
        song_title = (results['tracks']['items'][0]['name'])
        lyrics = get_lyrics(song_title)

        match_bool, score = matching_details(song_name, song_title, artist)
        if match_bool:
            return artist, album, song_title, lyrics, match_bool, score
        else:
            return None

    except IndexError:
        print('*Could not find metadata from spotify, trying something else.')
        return None


def get_details_letssingit(song_name):
    '''
    Gets the song details if song details not found through spotify
    '''

    song_name = improvename.songname(song_name)

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
            lyrics = ""
            print("     > Couldn't find lyrics")

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

    match_bool, score = matching_details(song_name, song_title, artist)

    return artist, album, song_title, lyrics, match_bool, score


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


def add_details(file_name, song_title, artist, album, lyrics=""):
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

    print("\n     [*]Song name : %s \n     [*]Artist : %s \n     [*]Album : %s \n " % (
        song_title, artist, album))


def fix_music(optional_arg = False):
    '''
    Searches for '.mp3' files in directory
    and checks whether they already contain album art
    and album name tags or not.
    '''

    files = [f for f in listdir('.') if f[-4:] == '.mp3']

    for file_name in files:
        tags = File(file_name)

        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys(): #Checks whether there is album art and album name
            print("%s already has tags " % tags["TIT2"])

        elif not('APIC:Cover' in tags.keys()) and 'TALB' in tags.keys():
            album = tags["TALB"].text[0]
            print("........................\n")

            print("%s Adding metadata" % file_name)

            try:
                albumart = albumsearch.img_search_google(album)
            except Exception:
                albumart = albumsearch.img_search_bing(album)

            add_albumart(albumart, file_name)

        else:
            print("........................\n")

            print("%s Adding metadata" % file_name)

            try:
                artist, album, song_name, lyrics, match_bool, score = get_details_spotify(
                    file_name)  # Try finding details through spotify

            except Exception:
                artist, album, song_name, lyrics, match_bool, score = get_details_letssingit(
                    file_name)  # Use bad scraping method as last resort

            try:
                print('*Trying to extract album art from Google.com')
                albumart = albumsearch.img_search_google(album)
            except Exception:
                print('*Trying to extract album art from Bing.com')
                albumart = albumsearch.img_search_bing(album)

            if match_bool:
                add_albumart(albumart, file_name)
                add_details(file_name, song_name, artist, album, lyrics)

                try:
                    if not optional_arg:
                        rename(file_name, song_name + '.mp3')

                except FileNotFoundError:
                    pass
            else:
                print("*Couldn't find appropriate details of your song")
                with open("musicrepair_log.txt", "a") as problems:
                    problems.write(str(file_name)+'\n') #log song that couldn't be repaired

            print("\nMatch score : %s%s" % (round(score * 10, 1), "/10.0"))
            print("........................\n\n")


def revert_music():
    files = [f for f in listdir('.') if f[-4:] == '.mp3']

    for file_name in files:
        print("Removing all metadata from %s" %file_name)
        tags = EasyMP3(file_name)
        tags.delete()
        tags.save()


def main():
    '''
    Deals with arguements and calls other functions
    '''

    print('\n\n')


    parser = argparse.ArgumentParser(
        description="Fix .mp3 files in any directory (Adds song details,album art)")
    parser.add_argument('-d', '--dir', action='store', dest='repair_directory',
                        help='Specifies the directory where the music files are located')
    parser.add_argument('-r', '--revert', action='store', dest='revert_directory',
                        help='Specifies the directory where music files that need to be reverted are located')
    parser.add_argument('-n', '--norename', action='store_true', help='Does not rename files to song title')

    args = parser.parse_args()

    music_dir = args.repair_directory
    revert_dir = args.revert_directory

    optional_arg = args.norename


    if not music_dir and not revert_dir:
        fix_music(optional_arg)
        open('musicrepair_log.txt','w') #Create log file (If it exists from prev session, truncate it)
    elif music_dir and not revert_dir:
        chdir(music_dir)
        open('musicrepair_log.txt','w') #Create log file (If it exists from prev session, truncate it)
        fix_music(optional_arg)

    elif revert_dir and not music_dir:
        chdir(revert_dir)
        revert_music()
    elif revert_dir and music_dir:
        print("Can't revert and repair together")

if __name__ == '__main__':
    main()
