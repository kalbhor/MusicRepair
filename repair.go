package main

import (
	"fmt"
	"path/filepath"
	"strconv"
	"strings"

	"github.com/bogem/id3v2"
	"github.com/headzoo/surf/errors"
	"github.com/zmb3/spotify"
)


func RepairWorker(client spotify.Client, job <-chan string, results chan<- string) {
	for filePath := range job {
		_, fileName := filepath.Split(filePath)
		results <- fmt.Sprintf("Fixing : %v\n", fileName)
		if err := Repair(client, filePath); err != nil {
			results <- fmt.Sprintf("Error : %v\n", err)
		}
	}
}

func RevertWorker(job <-chan string, results chan<- string) {
	for filePath := range job {
		_, fileName := filepath.Split(filePath)
		results <- fmt.Sprintf("Reverting : %v\n", fileName)
		if err := Revert(filePath); err != nil {
			results <- fmt.Sprintf("Error : %v\n", err)
		}
	}
}


func Revert(path string) error {
	tag, err := id3v2.Open(path, id3v2.Options{Parse: true})
	if err != nil {
		return err
	}
	defer tag.Close()

	tag.DeleteAllFrames()
	if err = tag.Save(); err != nil {
		return err
	}

	return nil
}

func Repair(client spotify.Client, path string) error {
	tag, err := id3v2.Open(path, id3v2.Options{Parse: true})
	if err != nil {
		return err
	}

	if CheckFrames(tag.AllFrames()) {
		return errors.New("Already contains tags")
	}

	_, filename := filepath.Split(path)
	metadata, err := GetMetadata(client, filename[0:len(filename)-4])
	if err != nil {
		return err
	}

	tag.SetTitle(metadata.Title)
	tag.SetAlbum(metadata.Album)
	tag.SetArtist(strings.Join(metadata.Artists, ","))

	TrackNumber := strconv.Itoa(metadata.TrackNumber)
	tag.AddFrame("TRCK", id3v2.TextFrame{id3v2.EncodingUTF8, TrackNumber})

	DiscNumber := strconv.Itoa(metadata.DiscNumber)
	tag.AddFrame("TPOS", id3v2.TextFrame{id3v2.EncodingUTF8, DiscNumber})

	pic := id3v2.PictureFrame{
		Encoding:    id3v2.EncodingUTF8,
		MimeType:    "image/jpeg",
		PictureType: id3v2.PTFrontCover,
		Description: "Front cover",
		Picture:     metadata.Image,
	}

	tag.AddAttachedPicture(pic)
	if err = tag.Save(); err != nil {
		return err
	}

	return nil
}
