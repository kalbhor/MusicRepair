# MusicRepair
[![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)](https://pypi.python.org/pypi/musicrepair)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
##### Fix .mp3 files in the current directory (Adds song details,album art)

* Fixes .mp3 files in the current working directory.
* Adds lyrics to song.
* Ignores songs already containing metadata.
* Changes file name to correct song title.

<br>
___

##### > Adds artist name, album name, album art
<img src="https://s19.postimg.org/tll7uil4j/Before_After.png" width="689px" height="432px" />
<br>
##### > Adds Lyrics
<img src="https://s19.postimg.org/3rbf4ql4j/Screen_Shot_2016_11_28_at_2_37_00_AM.png" width="317px" height="350px" />
<br>
___
### Installation

##### Python 2.x
```sh
$ pip install musicrepair
```

##### Python 3.x
```sh
$ pip3 install musicrepair
```
<br>
___
### Options

```
$ musicrepair -h
usage: musicrepair [-h] [-d DIRECTORY]

Fix .mp3 files in any directory (Adds song details,album art)

optional arguments:
  -h, --help    show this help message and exit
  -d DIRECTORY  Specifies the directory where the music files are located
```
___
### How to use
```sh
$ musicrepair
```

<img src="https://s19.postimg.org/vspgifqer/ezgif_com_34cbcee901.gif" width="853px" height="480px" />

___
### Resources 
[Spotipy](https://github.com/plamere/spotipy)
<br>
[Mutagen](https://pypi.python.org/pypi/mutagen)
<br>
[BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4)
<br>

___
License
----
The MIT License (MIT)
Copyright (c) 2016 Lakshay Kalbhor



