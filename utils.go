package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path"
	"path/filepath"

	"github.com/bogem/id3v2"
)

type Config struct {
	ID     string
	Secret string
}

var configFolder string = path.Join(os.Getenv("HOME"), ".musicrepair")
var configPath string = path.Join(configFolder, "config.json")

func LoadConfig() (*Config, error) {
	file, err := os.Open(configPath)
	if err != nil {
		return nil, err
	}
	decoder := json.NewDecoder(file)
	config := new(Config)
	err = decoder.Decode(&config)
	if err != nil {
		return nil, err
	}
	return config, nil
}

func SetConfig() error {
	var id, secret string
	fmt.Print("Enter Spotify ID : ")
	fmt.Scanln(&id)
	fmt.Print("Enter Spotify Secret : ")
	fmt.Scanln(&secret)

	config := Config{id, secret}
	b, err := json.Marshal(config)
	if err != nil {
		return err
	}
	if err := os.Mkdir(configFolder, os.ModePerm); err != nil {
		return err
	}
	if err := ioutil.WriteFile(configPath, b, os.ModePerm); err != nil {
		return err
	}

	return nil
}

func WalkDir(root string) (fileList []string) {

	filepath.Walk(root, func(path string, fi os.FileInfo, err error) error {
		// Fills fileList with all mp3 files in the `root` file tree
		if err != nil {
			return err
		}
		if !*isRecursive && filepath.Dir(path) != filepath.Dir(root) {
			return filepath.SkipDir
		}
		if filepath.Ext(path) == ".mp3" {
			fileList = append(fileList, path)
		}
		return nil
	})
	return
}

// Checks if a file already contains metadata
func CheckFrames(frames map[string][]id3v2.Framer) bool {
	if _, ok := frames["TALB"]; !ok {
		return false
	}
	if _, ok := frames["TIT2"]; !ok {
		return false
	}
	if _, ok := frames["APIC"]; !ok {
		return false
	}
	if _, ok := frames["TRCK"]; !ok {
		return false
	}
	if _, ok := frames["TPOS"]; !ok {
		return false
	}
	return true
}
