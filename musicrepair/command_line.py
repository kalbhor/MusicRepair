#!/usr/bin/env python

DESC = """
  __  __           _      _____                  _      
 |  \/  |         (_)    |  __ \                (_)     
 | \  / |_   _ ___ _  ___| |__) |___ _ __   __ _ _ _ __ 
 | |\/| | | | / __| |/ __|  _  // _ \ '_ \ / _` | | '__|
 | |  | | |_| \__ \ | (__| | \ \  __/ |_) | (_| | | |   
 |_|  |_|\__,_|___/_|\___|_|  \_\___| .__/ \__,_|_|_|   
                                    | |                 
                                    |_|                 

______________________________________________________________
|                                                            |
| Tries to find the metadata of songs based on the file name |
|                                                            |
| Update : pip install musicrepair -U                        |
|                                                            |            
| https://github.com/lakshaykalbhor/MusicRepair              |
|____________________________________________________________|

"""


from bs4 import BeautifulSoup
import requests

import argparse
from argparse import RawTextHelpFormatter
import configparser
from colorama import init, deinit, Fore
import difflib
import six

import spotipy
from mutagen.id3 import ID3, APIC, USLT, _util
from mutagen.mp3 import EasyMP3
from mutagen import File

from os import chdir, listdir, rename, walk, path, environ
from os.path import basename, dirname, realpath


try:
    from . import albumsearch
    from . import improvename
    from . import log
except:
    import albumsearch
    import improvename
    import log

if six.PY2:
    from urllib2 import urlopen
    from urllib2 import quote
    input = raw_input
    Py3 = False
elif six.PY3:
    from urllib.parse import quote
    from urllib.request import urlopen
    Py3 = True

def setup():
    """
    Gathers all configs
    """

    global CONFIG, BING_KEY, GENIUS_KEY, config_path, LOG_FILENAME, LOG_LINE_SEPERATOR 

    LOG_FILENAME = 'musicrepair_log.txt'
    LOG_LINE_SEPERATOR = '........................\n'

    CONFIG = configparser.ConfigParser()
    config_path = realpath(__file__).replace(basename(__file__),'')
    config_path = config_path + 'config.ini'
    CONFIG.read(config_path)

    BING_KEY = CONFIG['keys']['bing_key']
    GENIUS_KEY = CONFIG['keys']['genius_key']

    if BING_KEY == '<insert bing key here>':
        log.log_error('Warning, you are missing the Bing key. Add it using --config')

    if GENIUS_KEY == '<insert genius key here>':
        log.log_error('Warning, you are missing the Genius key. Add it using --config')



def add_config():
    """
    Prompts user for API keys, adds them in an .ini file stored in the same
    location as that of the script
    """

    genius_key = input('Enter Genius key : ')
    bing_key = input('Enter Bing key : ')

    CONFIG['keys']['bing_key'] = bing_key
    CONFIG['keys']['genius_key'] = genius_key

    with open(config_path, 'w') as configfile:
        CONFIG.write(configfile)

def matching_details(song_name, song_title, artist):
    """
    Provides a score out of 10 that determines the
    relevance of the search result
    """

    match_name = difflib.SequenceMatcher(None, song_name, song_title).ratio()
    match_title = difflib.SequenceMatcher(None, song_name, artist).ratio()

    if match_name >= 0.55 or (match_name < 0.55 and match_title >= 0.45):
        return True, match_name
    else:
        return False, (match_name + match_title) / 2


def get_lyrics_genius(song_title):
    """
    Gets lyrics from genius.com by making an API call and fetching the url 
    of the of page with lyrics. Then scrapes that page for lyrics.
    """
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
    """
    Use Spotipy to send an API call to Spotify to fetch the details of a track
    """ 

    #Remove useless words such as - 'lyrics', 'HD', 'audio' from file name
    song_name = improvename.songname(song_name)
    spotify = spotipy.Spotify()
    #Choose top result
    results = spotify.search(song_name, limit=1)

    log.log_indented('* Finding metadata from Spotify.')

    try:
        album = (results['tracks']['items'][0]['album']['name'])
        artist = (results['tracks']['items'][0]['album']['artists'][0]['name'])
        song_title = (results['tracks']['items'][0]['name'])
    except IndexError:
        log.log_error('* Could not find metadata from spotify, trying something else.', indented=True)
        return None

    try:
        log.log_indented("* Finding lyrics from Genius.com")
        lyrics = get_lyrics_genius(artist+' '+song_title)
    except:
        lyrics=''
        log.log_error("* Could not find lyrics from Genius.com", indented=True)

    match_bool, score = matching_details(song_name, song_title, artist)

    if match_bool:
        log.log("Match score: %s/10.0" % round(score * 10, 1))
        return artist, album, song_title, lyrics
    else:
        return None


def add_albumart(query, song_title):
    """ 
    Adds the album art to a song by editing ID3 tags using Mutagen
    """ 

    try: 
        log.log_indented('* Trying to extract album art from Google.com')
        albumart = albumsearch.img_search_google(query)
    except:
        log.log_error('* Could not extract from Google, trying Bing')
        albumart = albumsearch.img_search_bing(query)

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
            data=img.read()
        )
    )
    audio.save()
    log.log("> Added album art")


def add_details(file_path, title, artist, album, lyrics=""):
    """  
    Adds the details of a song using Mutagen
    """ 

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


def fix_music(rename_format, norename, files):
    """ 
    Checks whether files already contain album art and album name tags or not. 
    If not, calls other functions to add album art, details.
    """ 

    for file_path in files:
        tags = File(file_path)
        #Gets file name and removes .mp3 for better search results
        file_name = basename(file_path)[:-4]

        # Checks whether there is album art and album name
        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys():
            log.log('%s already has tags ' % tags["TIT2"])

        elif not('APIC:Cover' in tags.keys()) and 'TALB' in tags.keys():
            album = tags["TALB"].text[0]
            
            log.log(LOG_LINE_SEPERATOR)
            log.log(file_path)
            log.log('> Adding metadata')

            add_albumart(album, file_path)

        else:
            log.log(LOG_LINE_SEPERATOR)
            log.log(file_path)
            log.log('> Adding metadata')

            try:
                artist, album, song_name, lyrics = get_details_spotify(file_name) 
                add_albumart(artist+' '+album, file_path)
                add_details(file_path, song_name, artist, album, lyrics)
            except Exception:
                log.log_error("* Couldn't find metadata from Spotify")

            try:
                if not norename:
                    song_title = rename_format.format(
                                 title=song_name + '-', 
                                 artist=artist + '-', 
                                 album=album + '-')

                    song_title = song_title[:-1] if song_title.endswith('-') else song_title
                    rename(file_path, 
                           path.dirname(file_path) 
                           + '/{song_title}.mp3'.format(song_title=song_title))

            except Exception:
                pass


def list_files(recursive):
    """
    Returns a list of all .mp3 files in a directory or in nested directories
    (If recursive is True).
    """

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

    return files


def revert_music(files):
    """
    Removes all tags from a mp3 file
    """

    for file_path in files:
        log.log('Removing all metadata from %s' % file_path)
        tags = EasyMP3(file_path)
        tags.delete()
        tags.save()


def main():
    """
    Deals with arguements and calls other functions
    """
    init()

    log.log('\n')
    setup()

    parser = argparse.ArgumentParser(
    description="{}".format(DESC), formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c', '--config', action='store_true',
                        help='Add API keys to config\n\n')

    parser.add_argument('-d', '--dir', action='store', dest='repair_directory',
                        help='Specifies the directory where the music files are located\n\n')

    parser.add_argument('-R', '--recursive', action='store_true',
                        help='''Specifies whether or not to run recursively 
                        in the given music directory\n\n''')

    parser.add_argument('-r', '--revert', action='store', dest='revert_directory',
                        help='''Specifies the directory where music files 
                        that need to be reverted are located\n\n''')

    parser.add_argument('-n', '--norename', action='store_true',
                        help='Does not rename files to song title\n\n')

    parser.add_argument('--format', action='store', dest='rename_format',
                        help='''Specify the title format used in renaming, 
                        these keywords will be replaced respectively: 
                        {title}{artist}{album}\n\n''')

    args = parser.parse_args()

    # Collect all the args
    music_dir = args.repair_directory
    revert_dir = args.revert_directory
    recursive = args.recursive or False
    norename = args.norename or False
    rename_format = args.rename_format or '{title}' #Fallback to default format
    config = args.config

    if config:
        add_config()

    if revert_dir:
        chdir(revert_dir)
        files = list_files(recursive)
        revert_music(files)


    if music_dir:
        chdir(music_dir or '.')
        files = list_files(recursive)
        fix_music(rename_format, norename, files)
        open(LOG_FILENAME, 'w')
        log.log_success()


if __name__ == '__main__':
    main()
