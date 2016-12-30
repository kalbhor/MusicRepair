#!/usr/bin/env python

'''
Tries to find the metadata of songs based on the file name
https://github.com/lakshaykalbhor/MusicRepair
'''

import argparse
from os import chdir, listdir, rename, walk, path, environ
from os.path import basename, dirname

import difflib
import six

from bs4 import BeautifulSoup
import requests
from colorama import init, deinit, Fore
from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File

import spotipy

from . import albumsearch
from . import improvename
from . import log

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    Py3 = False
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen
    Py3 = True


LOG_FILENAME = 'musicrepair_log.txt'
LOG_LINE_SEPERATOR = '........................\n'

try:
    GENIUS_KEY = environ['GENIUS_LYRICS_KEY']

except KeyError:
    log.log_error('Warning, GENIUS_LYRICS_KEY not added in environment variables')

try:
    BING_KEY = environ['BING_IMG_KEY']

except KeyError:
    log.log_error('Warning, BING_IMG_KEY not added in environment variables')


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


def get_lyrics_letssingit(song_name):
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

def get_lyrics_genius(song_title):
    base_url = "http://api.genius.com"
    headers = {'Authorization': 'Bearer %s' %(GENIUS_KEY)}
    search_url = base_url + "/search"
    data = {'q': song_title}

    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_api_path = json["response"]["hits"][0]["result"]["api_path"]

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path

    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    div = soup.find('div',{'class': 'song_body-lyrics'})
    lyrics = div.find('p').getText()
  
    return lyrics


def get_details_spotify(song_name):
    '''
    Tries finding metadata through Spotify
    '''

    song_name = improvename.songname(song_name)

    spotify = spotipy.Spotify()
    results = spotify.search(song_name, limit=1)  # Find top result

    log.log_indented('* Finding metadata from Spotify.')

    try:
        album = (results['tracks']['items'][0]['album']['name'])  # Parse json dictionary
        artist = (results['tracks']['items'][0]['album']['artists'][0]['name'])
        song_title = (results['tracks']['items'][0]['name'])

        try:
            log.log_indented("* Finding lyrics from Genius.com")
            lyrics = get_lyrics_genius(artist+' '+song_title)

        except:
            log.log_error("* Could not find lyrics from Genius.com, trying something else", indented=True)
            lyrics = get_lyrics_letssingit(artist+' '+song_title)

        match_bool, score = matching_details(song_name, song_title, artist)
        if match_bool:
            return artist, album, song_title, lyrics, match_bool, score
        else:
            return None

    except IndexError:
        log.log_error('* Could not find metadata from spotify, trying something else.', indented=True)
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
            log.log_error("* Couldn't find lyrics", indented=True)

        try:
            song_title = title_div.contents[0]
            song_title = song_title[1:-8]
        except AttributeError:
            log.log_error("* Couldn't reset song title", indented=True)
            song_title = song_name

        try:
            artist = title_div.contents[1].getText()
        except AttributeError:
            log.log_error("* Couldn't find artist name", indented=True)
            artist = "Unknown"

        try:
            album = album_div.find('a').contents[0]
            album = album[:-7]
        except AttributeError:
            log.log_error("* Couldn't find the album name", indented=True)
            album = artist

    except AttributeError:
        log.log_error("* Couldn't find song details", indented=True)

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
        log.log_error("* Could not add album art", indented=True)
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
    log.log("> Added album art")


def add_details(file_path, title, artist, album, lyrics=""):
    '''
    Adds the details to song
    '''

    tags = EasyMP3(file_path)
    tags["title"] = title
    tags["artist"] = artist
    tags["album"] = album
    tags.save()

    tags = ID3(file_path)
    uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
    tags["USLT::'eng'"] = uslt_output

    tags.save(file_path)

    log.log("> Adding properties")
    log.log_indented("[*] Title: %s" % title)
    log.log_indented("[*] Artist: %s" % artist)
    log.log_indented("[*] Album: %s " % album)


def fix_music(rename_format, norename=False, recursive=False):
    '''
    Searches for '.mp3' files in directory (optionally recursive)
    and checks whether they already contain album art and album name tags or not.
    '''
    files = []

    if recursive:
        for dirpath, _, filenames in walk("."):
            for filename in [f for f in filenames if f.endswith(".mp3")]:
                if Py3:
                    files += [path.join(dirpath, filename)]
                else:
                    files += [path.join(dirpath, filename).decode('utf-8')]
    else:
        if Py3:
            files = [f for f in listdir('.') if f.endswith('.mp3')]

        else:
            files = [f.decode('utf-8') for f in listdir('.') if f.endswith('.mp3')]

    for file_path in files:
        tags = File(file_path)
        file_name = basename(file_path)[:-4] #Gets file name and removes .mp3 for better search results

        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys():  # Checks whether there is album art and album name
            log.log('%s already has tags ' % tags["TIT2"])

        elif not('APIC:Cover' in tags.keys()) and 'TALB' in tags.keys():
            album = tags["TALB"].text[0]
            log.log(LOG_LINE_SEPERATOR)

            log.log(file_path)
            log.log('> Adding metadata')

            try:
                albumart = albumsearch.img_search_google(album)
            except Exception:
                albumart = albumsearch.img_search_bing(album, BING_KEY)

            add_albumart(albumart, file_path)

        else:
            log.log(LOG_LINE_SEPERATOR)

            log.log(file_path)
            log.log('> Adding metadata')

            try:
                artist, album, song_name, lyrics, match_bool, score = get_details_spotify(
                    file_name)  # Try finding details through spotify

            except Exception:
                log.log_error("* Couldn't find metadata from Spotify, trying something else")
                artist, album, song_name, lyrics, match_bool, score = get_details_letssingit(
                    file_name)  # Use bad scraping method as last resort

            try:
                log.log_indented('* Trying to extract album art from Google.com')
                albumart = albumsearch.img_search_google(artist+' '+album)
            except Exception:
                log.log_indented('* Trying to extract album art from Bing.com')
                albumart = albumsearch.img_search_bing(arist+' '+album)

            if match_bool:
                add_albumart(albumart, file_path)
                add_details(file_path, song_name, artist, album, lyrics)

                try:
                    if not norename:
                        song_title = rename_format.format(title=song_name + '-', artist=artist + '-', album=album+'-')
                        song_title = song_title[:-1] if song_title.endswith('-') else song_title
                        rename(file_path, path.dirname(file_path) + '/{song_title}.mp3'.format(song_title=song_title))
                except Exception:
                    pass
            else:
                log.log_error("* Couldn't find appropriate details of your song", indented=True)
                with open(LOG_FILENAME, "a") as problems:
                    problems.write(str(file_path) + '\n')  # log song that couldn't be repaired

            log.log("Match score: %s/10.0" % round(score * 10, 1))
            log.log(LOG_LINE_SEPERATOR)


def revert_music(recursive=False):

    files = []

    if recursive:
        for dirpath, _, filenames in walk("."):
            for filename in [f for f in filenames if f.endswith(".mp3")]:
                if Py3:
                    files += [path.join(dirpath, filename)]
                else:
                    files += [path.join(dirpath, filename).decode('utf-8')]
    else:
        if Py3:
            files = [f for f in listdir('.') if f.endswith('.mp3')]
        else:
            files = [f.decode('utf-8') for f in listdir('.') if f.endswith('.mp3')]

    for file_path in files:
        log.log('Removing all metadata from %s' % file_path)
        tags = EasyMP3(file_path)
        tags.delete()
        tags.save()


def main():
    '''
    Deals with arguements and calls other functions
    '''
    init()

    log.log('\n')

    parser = argparse.ArgumentParser(
        description="Fix .mp3 files in any directory (Adds song details, album art)")
    parser.add_argument('-d', '--dir', action='store', dest='repair_directory',
                        help='Specifies the directory where the music files are located')
    parser.add_argument('-R', '--recursive', action='store_true',
                        help='Specifies whether or not to run recursively in the given music directory')
    parser.add_argument('-r', '--revert', action='store', dest='revert_directory',
                        help='Specifies the directory where music files that need to be reverted are located')
    parser.add_argument('-n', '--norename', action='store_true',
                        help='Does not rename files to song title')
    parser.add_argument('--format', action='store', dest='rename_format',
                        help='Specify the title format used in renaming, these keywords will be replaced respectively: {title}{artist}{album}')

    args = parser.parse_args()

    # Collect all the args
    arg_music_dir = args.repair_directory
    arg_revert_dir = args.revert_directory
    arg_recursive = args.recursive
    arg_norename = args.norename
    arg_rename_format = args.rename_format or '{title}' #Fallback to default format

    # Decide what to do
    if not arg_music_dir and not arg_revert_dir:
        fix_music(arg_rename_format, norename=arg_norename, recursive=arg_recursive)

        open(LOG_FILENAME, 'w')  # Create log file (If it exists from prev session, truncate it)
        log.log_success()

    elif arg_music_dir and not arg_revert_dir:
        chdir(arg_music_dir)
        fix_music(arg_rename_format, norename=arg_norename, recursive=arg_recursive)

        open(LOG_FILENAME, 'w')  # Create log file (If it exists from prev session, truncate it)
        log.log_success()

    elif arg_revert_dir and not arg_music_dir:
        chdir(arg_revert_dir)
        revert_music(recursive=arg_recursive)

        log.log_success()

    elif arg_revert_dir and arg_music_dir:
        log.log("Can't revert and repair together")


if __name__ == '__main__':

    main()
