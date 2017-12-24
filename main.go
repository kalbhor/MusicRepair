package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

var (
	root        = flag.String("dir", "./", "Specifies the directory where the music files are located")
	isRecursive = flag.Bool("recursive", false, "If set, Musicrepair will run recursively in the given directory")
	setConfig   = flag.Bool("config", false, "If set, MusicRepair will ask for credentials")
	isRevert    = flag.Bool("revert", false, "If set, Musicrepair will revert the files")
	threads     = flag.Int("threads", 1, "Specify the number of threads to use")
)

func main() {
	flag.Parse()

	if *setConfig {
		SetConfig()
		fmt.Println("Your config has been saved.")
		os.Exit(1)
	}

	config, err := LoadConfig()
	if err != nil {
		log.Fatal(err)
	}

	client, err := SpotifyAuth(config.ID, config.Secret)
	if err != nil {
		log.Fatal("Invalid spotify credentials. Error : %v", err)
	}

	fileList := WalkDir(*root) // List of all files to work on

	jobs := make(chan string)
	results := make(chan string)

	for w := 1; w <= *threads; w++ {
		if *isRevert {
			go RevertWorker(jobs, results)
		} else {
			go RepairWorker(client, jobs, results)
		}
	}

	for _, job := range fileList {
		jobs <- job
	}
	close(jobs)

	for r := 1; r <= len(fileList); r++ {
		fmt.Printf("[%v] %v\n", r, <-results)
	}

}
