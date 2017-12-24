
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

## Features

1. Fixes songs in nested directories recursively.
2. Fetches metadata from [Spotify](https://www.spotify.com)
3. Multiple options to format file (Options to revert file back)
4. Simple binary

## Dependencies  

### [Spotify API](https://developer.spotify.com/my-applications)

1. Create an account and register an application.
2. Copy the Client ID and Client Secret.
3. Set them in *config file* after running ```musicrepair -config```

###### *config file* will be created after running `musicrepair -config`, and located at `$HOME/.musicrepair/config.json`

### Set them using ```-config```
```sh 
$ musicrepair -config                                               
Enter Spotify client ID : <enter Spotify client ID>  
Enter Spotify client secret : <enter Spotify client secret>                                     
```

## Installing

### Via Binary

Download the latest binary from the [releases page](https://github.com/kalbhor/MusicRepair/releases).

Make sure to add the binary to your `$PATH`

### Via Go
```sh
$ go get -u -v github.com/kalbhor/musicrepair
$ which musicrepair
$ $GOPATH/bin/musicrepair
```

## Usage

Initially, you'll have to add the Spotify credentials. 
```sh
$ musicrepair -config
```

After that, always a simple command
```sh
$ musicrepair
✨ 🍰
```


### Options
```
$ musicrepair -help

Usage of musicrepair:
  -config
    	If set, MusicRepair will ask for credentials
  -dir string
    	Specifies the directory where the music files are located (default "./")
  -recursive
    	If set, Musicrepair will run recursively in the given directory
  -revert
    	If set, Musicrepair will revert the files
  -threads int
    	Specify the number of threads to use (default 1)
```

## Contribute

Found an issue? Post it in the [issue tracker](https://github.com/kalbhor/MusicRepair/issues).

Want to add another awesome feature? [Fork](https://github.com/kalbhor/MusicRepair/fork) this repository and add your feature, then send a pull request.

## License
The MIT License (MIT)
Copyright (c) 2017 Lakshay Kalbhor
