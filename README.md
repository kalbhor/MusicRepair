
<p align="center">
    <img src="https://s28.postimg.org/wibuzmq8d/Music_Repair_GIF.gif" width="800">    
</p>
<p align="center">
  <b>Adds Metadata to Music files</b>
</p>

<p align="center">
    <a href="https://github.com/kalbhor/musicrepair/LICENSE">
		<img alt="License"  src="https://img.shields.io/github/license/mashape/apistatus.svg?style=flat-square"/>
	</a>    
	<a href="https://gitter.im/MusicRepair/Lobby">
		<img alt="gitter" src="https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square "/>
	</a>        
	<a href="https://github.com/kalbhor/musicrepair">
		<img alt="stars" src="https://img.shields.io/github/stars/kalbhor/musicrepair.svg?style=social&label=Star"/>
	</a>            
</p>


## Media
<p align="left">
    <a href="https://mavielinux.com/2016/12/11/musicrepair-pour-corriger-les-titresajouter-les-metadonnees-et-les-pochettes-de-vos-musiques/">
		<img width="70px" src="http://i.imgur.com/TklsaII.png"/>
	</a>
	&nbsp;&nbsp;&nbsp;
    <a href="http://blog.desdelinux.net/reparar-archivos-de-musica/">
		<img width="160px" src="http://i.imgur.com/eV1WxYZ.png"/>
	</a>
	&nbsp;&nbsp;&nbsp;
    <a href="https://www.reddit.com/r/learnpython/comments/5gzvcb/i_made_a_script_that_would_fix_your_music_files/">
		<img width="160px" src="http://i.imgur.com/Jk8PgIb.png"/>
	</a>
	&nbsp;&nbsp;&nbsp;
</p>

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installing](#installing)
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

##### (Optional)
### [Genius API](https://genius.com/api-clients) 

1. Create an account and register an application 
2. Grab Access Token
3. Set access token in config file

```sh 
$ musicrepair --config                                               
     
Enter Genius key : <enter genius key>                                 
```

## Installing

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
