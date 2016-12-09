import re

def songname(song_name):
    '''
    Improves file name by removing crap words
    '''

    song_name = song_name[:-4]

    repls = {  # Words to omit from song title for better results through spotify's API
        '(':"", ')':"",

        '[':"", ']':"",

        '{':"", '}':"",

        'official': "", 'Official': "",

        'lyrics': "", 'Lyrics': "",

        'audio': "", 'Audio': "",

        'remix': "", 'Remix': "",

        'video':"", 'Video':"",

        'full':"", 'Full':"",

        'version':"", 'Version':"",

        'music':"", 'Music':"",

        '.mp3':"",

        'HD':"", 'hd':"",

        'hq':"", 'HQ':"",
    }

    song_name = re.sub('|'.join(re.escape(key) for key in repls.keys()),
                       lambda k: repls[k.group(0)], song_name)  # Regex to substitute repls

    return song_name
