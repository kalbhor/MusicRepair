<img src="https://s28.postimg.org/wibuzmq8d/Music_Repair_GIF.gif" width="800px" height="270px" />

# MusicRepair

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](LICENSE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square)](https://gitter.im/MusicRepair/Lobby)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> MusicRepair is a python script that fixes your music by adding important tags such as : album name, artist name, lyrics and album art.

## Show :heart:

[![GitHub stars](https://img.shields.io/github/stars/lakshaykalbhor/musicrepair.svg?style=social&label=Star)](https://github.com/lakshaykalbhor/musicrepair)
[![GitHub followers](https://img.shields.io/github/followers/lakshaykalbhor.svg?style=social&label=Follow)](https://github.com/lakshaykalbhor)  
[![Twitter Follow](https://img.shields.io/twitter/follow/lakshayisfunny.svg?style=social)](https://twitter.com/lakshayisfunny)


## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
  - [PyPI](#pypi)
  - [Source](#source)
  - [Options](#options)
- [Contribute](#contribute)
- [License](#license)

## Features

1. Fixes songs in nested directories recursively.
2. Fetches lyrics from [Genius](https://www.genius.com)
3. Fetches metadata from [Spotify](https://www.spotify.com)
4. Multiple options to format file name. eg : {artist}{title} results in : Pink Floyd - Time

## Dependencies  

### [Genius API](https://genius.com/api-clients)

1. Create an account and register an application 
2. Grab Access Token
3. Set environment variable in your bashrc/zshrc file

```sh 
export GENIUS_LYRICS_KEY=YOUR KEY 
```

### [Bing Search API](https://www.microsoft.com/cognitive-services/en-us/bing-image-search-api)

1. Create an account
2. Grab Access Token
3. Set environment variable in your bashrc/zshrc file

```sh
export BING_IMG_KEY=YOUR KEY 
```

## Installation

### PyPI
```sh
$ pip install musicrepair
```

### Source
```sh
$ git clone https://github.com/lakshaykalbhor/MusicRepair
$ cd MusicRepair
$ python setup.py install
```

Windows users, check [this](https://github.com/lakshaykalbhor/MusicRepair/issues/9) out

## Usage

```sh
$ musicrepair
```

[![Usage](https://s18.postimg.org/53imrt015/Screen_Shot_2016_12_11_at_1_42_02_AM.png)](https://www.youtube.com/watch?v=UqsmRIIeTpg "MusicRepair - Usage")

### Options
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

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/lakshaykalbhor/MusicRepair/issues). <br> 
Want to add another awesome feature? [Fork](https://github.com/lakshaykalbhor/MusicRepair/fork) this repository and add your feature, then send a pull request.

## License
The MIT License (MIT)
Copyright (c) 2017 Lakshay Kalbhor

