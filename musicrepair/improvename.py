import re
from os.path import splitext


def songname(song_name):
    '''
    Improves file name by removing crap words
    '''
    try:
        song_name = splitext(song_name)[0]
    except IndexError:
        pass

    # Words to omit from song title for better results through spotify's API
    chars_filter = "()[]{}-:_/=+\"\'"
    words_filter = ('official', 'lyrics', 'audio', 'remixed', 'remix', 'video',
                    'full', 'version', 'music', 'mp3', 'hd', 'hq', 'uploaded')

    # Replace characters to filter with spaces
    song_name = ''.join(map(lambda c: " " if c in chars_filter else c, song_name))

    # Remove crap words
    song_name = re.sub('|'.join(re.escape(key) for key in words_filter),
                       "", song_name, flags=re.IGNORECASE)

    # Remove duplicate spaces
    song_name = re.sub(' +', ' ', song_name)
    return song_name.strip()
