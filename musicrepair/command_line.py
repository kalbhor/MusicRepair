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

import requests
import argparse
import configparser
from argparse import RawTextHelpFormatter
from mutagen.id3 import ID3
from mutagen import File
from os import chdir, listdir, rename, walk, path, environ
from os.path import basename, dirname, realpath
from musictools import musictools

def setup():
    """
    Gathers all configs
    """

    global CONFIG, GENIUS_KEY, config_path 

    CONFIG = configparser.ConfigParser()
    config_path = realpath(__file__).replace(basename(__file__),'')
    config_path = config_path + 'config.ini'
    CONFIG.read(config_path)

    GENIUS_KEY = CONFIG['keys']['genius_key']


    if GENIUS_KEY == '<insert genius key here>':
        print('Warning, you are missing the Genius key. Add it using --config\n\n')


def add_config():
    """
    Prompts user for API keys, adds them in an .ini file stored in the same
    location as that of the script
    """

    genius_key = input('Enter Genius key : ')

    CONFIG['keys']['genius_key'] = genius_key

    with open(config_path, 'w') as configfile:
        CONFIG.write(configfile)


def add_lyrics_genius(file_path, song_title):
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

    try:
        song_api_path = json["response"]["hits"][0]["result"]["api_path"]

    except KeyError:
        print('Could not find lyrics\n')
        return None

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path

    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, "html.parser")
    div = soup.find('div',{'class': 'song_body-lyrics'})
    lyrics = div.find('p').getText()

    tags = ID3(file_path)
    uslt_output = USLT(encoding=3, lang=u'eng', desc=u'desc', text=lyrics)
    tags["USLT::'eng'"] = uslt_output
    tags.save(file_path)
  
    return lyrics


def fix_music(rename_format, norename, files):
    """ 
    Checks whether files already contain album art and album name tags or not. 
    If not, calls other functions to add album art, details.
    """ 

    for file_path in files:
        tags = File(file_path)
        # Gets file name and removes .mp3 for better search results
        file_name = basename(file_path)[:-4]

        # Checks whether there is album art and album name
        if 'APIC:Cover' in tags.keys() and 'TALB' in tags.keys():
            print('%s already has tags' % tags["TIT2"])

        else:
            print('> ' + file_path)

            artist, album, song_name, albumart = musictools.get_metadata(file_name) 
            add_lyrics_genius(file_path, file_name)
            musictools.add_albumart(file_path, albumart)
            musictools.add_metadata(file_path, song_name, artist, album)

            print('{}\n{}\n{}\n'.format(song_name, album, artist))

            if not norename:

                song_title = rename_format.format(
                      title=song_name + ' -', 
                      artist=artist + ' -', 
                      album=album + ' -')

                song_title = song_title[:-1] if song_title.endswith('-') else song_title
                new_path = path.dirname(file_path) + '{}.mp3'.format(song_title)

                rename(file_path, new_path)


def list_files(recursive):
    """
    Returns a list of all .mp3 files in a directory or in nested directories
    (If recursive is True).
    """

    files = []

    if recursive:
        for dirpath, _, filenames in walk("."):
            for filename in [f for f in filenames if f.endswith(".mp3")]:
                files += [path.join(dirpath, filename)]
    else:
        files = [f for f in listdir('.') if f.endswith('.mp3')]

    return files



def main():
    """
    Deals with arguements and calls other functions
    """

    print('\n')
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
        musictools.revert_music(files)

    if music_dir:
        chdir(music_dir or '.')
        files = list_files(recursive)
        fix_music(rename_format, norename, files)
        open('musicrepair_log.txt', 'w')
        print('\n\nFinished repairing')


if __name__ == '__main__':
    main()
