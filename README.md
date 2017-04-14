<img src="https://s28.postimg.org/wibuzmq8d/Music_Repair_GIF.gif" width="800px" height="270px" />

# MusicRepair

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square)](LICENSE)
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square)](https://gitter.im/MusicRepair/Lobby)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

> MusicRepair is a python script that fixes your music by adding important tags such as : album name, artist name, lyrics and album art.

## Social:

[![GitHub stars](https://img.shields.io/github/stars/kalbhor/musicrepair.svg?style=social&label=Star)](https://github.com/kalbhor/musicrepair)
[![GitHub followers](https://img.shields.io/github/followers/kalbhor.svg?style=social&label=Follow)](https://github.com/kalbhor)  
[![Twitter Follow](https://img.shields.io/twitter/follow/lakshaykalbhor.svg?style=social)](https://twitter.com/lakshaykalbhor)


## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation](#installation)
  - [PyPI](#pypi)
  - [Source](#source)
- [Usage](#usage)
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
3. Set access token in config file

```sh 
$ musicrepair --config                                               
     
Enter Genius key : <enter genius key>                                 
```

## Installation

### PyPI
```sh
$ pip install musicrepair
```

### Source
```sh
$ git clone https://github.com/kalbhor/MusicRepair
$ cd MusicRepair
$ python setup.py install
```

Windows users, check [this](https://github.com/kalbhor/MusicRepair/issues/9) out

## Usage

```sh
$ musicrepair
```

[![Usage](https://s18.postimg.org/53imrt015/Screen_Shot_2016_12_11_at_1_42_02_AM.png)](https://www.youtube.com/watch?v=UqsmRIIeTpg "MusicRepair - Usage")

### Options
```
$ musicrepair -h
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
| https://github.com/kalbhor/MusicRepair                     |
|____________________________________________________________|

optional arguments:
  -h, --help            show this help message and exit
  
  -c, --config          Add API keys to config

  -d, --dir             Specifies the directory where the music files are located

  -R, --recursive       Specifies whether or not to run recursively
                        in the given music directory

  -r, --revert          Specifies the directory where music files
                        that need to be reverted are located

  -n, --norename        Does not rename files to song title

  --format              Specify the title format used in renaming,
                        these keywords will be replaced respectively:
                        {title}{artist}{album}
```

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/kalbhor/MusicRepair/issues). <br> 
Want to add another awesome feature? [Fork](https://github.com/kalbhor/MusicRepair/fork) this repository and add your feature, then send a pull request.
The core features of this project are based on [MusicTools](https://github.com/kalbhor/MusicTools); contribute to it if you'd like.

## License
The MIT License (MIT)
Copyright (c) 2017 Lakshay Kalbhor

