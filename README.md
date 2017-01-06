# MusicRepair
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/musicrepair)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
##### Fix .mp3 files in a directory (Adds song details,album art)

* Fixes .mp3 files in nested directories recursively.
* Adds lyrics to songs from genius.com.
* Adds metadata to songs from spotify.com.
* Multiple options to format file name.

## Table of Contents
- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Options](#options)
- [Usage](#usage)

## Features
##### > Adds artist name, album name, album art

<img src="https://s28.postimg.org/wibuzmq8d/Music_Repair_GIF.gif" width="800px" height="270px" />

##### > Adds Lyrics
<img src="https://s19.postimg.org/3rbf4ql4j/Screen_Shot_2016_11_28_at_2_37_00_AM.png" width="317px" height="350px" />

## Dependencies  

##### Fetch API keys from [Genius.com](https://genius.com/api-clients)

1. Create an account and register an application 
2. Grab Access Token
3. Set environment variable in your bashrc/zshrc file

```sh 
export GENIUS_LYRICS_KEY=YOUR KEY 
```

<img src="https://s29.postimg.org/k4ga1gmsn/Genius_API.png" width="543px" height="362px" />

##### Fetch image search API keys from [Microsoft.com](https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api)

1. Create an account
2. Grab Access Token
3. Set environment variable in your bashrc/zshrc file

```sh
export BING_IMG_KEY=YOUR KEY 
```

<img src="https://s29.postimg.org/yibo1if7r/Bing_Key.png" width="1150px" height="210px" />

## Installation

##### Python 2.x
```sh
$ pip install musicrepair
```

##### Python 3.x
```sh
$ pip3 install musicrepair
```
(If it doesn't work for Windows users, check [this](https://github.com/lakshaykalbhor/MusicRepair/issues/9) out)

## Options

```
$ musicrepair -h
usage: musicrepair [-h] [-d REPAIR_DIRECTORY] [-R] [-r REVERT_DIRECTORY] [-n]
                   [--format RENAME_FORMAT]

Fix .mp3 files in any directory (Adds song details, album art)

optional arguments:

  -h, --help            show this help message and exit
  
  -d , --dir 
                        Specifies the directory where the music files are
                        located
                        
  -R, --recursive       Specifies whether or not to run recursively in the
                        given music directory
                        
  -r , --revert
                        Specifies the directory where music files that need to
                        be reverted are located
                        
  -n, --norename        Does not rename files to song title
  
  --format
                        Specify the title format used in renaming, these
                        keywords will be replaced respectively:
                        {title}{artist}{album}
```

## Usage

```sh
$ musicrepair
```

[![Usage](https://s18.postimg.org/53imrt015/Screen_Shot_2016_12_11_at_1_42_02_AM.png)](https://www.youtube.com/watch?v=UqsmRIIeTpg "MusicRepair - Usage")

License
----
The MIT License (MIT)
Copyright (c) 2017 Lakshay Kalbhor
