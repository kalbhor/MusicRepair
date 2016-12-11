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
(If it doesn't work for Windows users, check [this](https://github.com/lakshaykalbhor/MusicRepair/issues/9) out)
<br>
___
### Options

```
$ musicrepair -h
usage: musicrepair [-h] [-d REPAIR_DIRECTORY] [--revert REVERT_DIRECTORY]
                   [--norename]

Fix .mp3 files in any directory (Adds song details,album art)

optional arguments:
  -h, --help            Show this help message and exit
  
  -d                    Specifies the directory where the music files are
                        located
                        
  --revert              Specifies the directory where music files that need to
                        be reverted are located
                        
  --norename            Does not rename files to song title
  
  --format              Specify the title format used in renaming, these keywords
                        will be replaced respectively: {title}{artist}{album}
```
___
### How to use
```sh
$ musicrepair
```

[![Usage](https://s18.postimg.org/53imrt015/Screen_Shot_2016_12_11_at_1_42_02_AM.png)](https://www.youtube.com/watch?v=CjJ0wHR3r2Y "MusicRepair - Usage")

___
### To do 
- [ ] Add view mode (Doesn't change metadata, just shows changes)
- [x] Add a revert mode (Removes all metadata from songs)
- [x] Add a no rename mode (Doesn't change file name)

___
License
----
The MIT License (MIT)
Copyright (c) 2016 Lakshay Kalbhor



