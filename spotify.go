package main

import (
	"context"
	"errors"
	"io/ioutil"
	"net/http"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/clientcredentials"

	"github.com/zmb3/spotify"
)

//Metadata : Structure for one track's metadata
type Metadata struct {
	Title       string
	Artists     []string
	Album       string
	Image       []byte
	DiscNumber  int
	TrackNumber int
}

//Load : Sets values from search results
func (m *Metadata) Load(track spotify.FullTrack) error {
	m.Title = track.SimpleTrack.Name
	m.Album = track.Album.Name
	m.DiscNumber = track.SimpleTrack.DiscNumber
	m.TrackNumber = track.SimpleTrack.TrackNumber

	for _, artist := range track.SimpleTrack.Artists {
		m.Artists = append(m.Artists, artist.Name)
	}

	imageURL := track.Album.Images[0].URL
	resp, err := http.Get(imageURL)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return err
	}
	m.Image = b

	return nil
}

//GetMetadata : Searches spotify and returns a loaded metadata struct
func GetMetadata(client spotify.Client, query string) (*Metadata, error) {

	m := new(Metadata)

	results, err := client.Search(query, spotify.SearchTypeTrack)
	if err != nil {
		return nil, err
	} else if len(results.Tracks.Tracks) == 0 { // Search results were empty
		return nil, errors.New("Couldn't fetch metadata")
	}

	err = m.Load(results.Tracks.Tracks[0]) // Pass in the top result
	if err != nil {
		return m, err
	}
	return m, nil

}

//Auth : Returns a usable spotify "client" that can request spotify content
func SpotifyAuth(Id, Secret string) (spotify.Client, error) {
	config := &clientcredentials.Config{
		ClientID:     Id,
		ClientSecret: Secret,
		TokenURL:     spotify.TokenURL,
	}
	token, err := config.Token(context.Background())
	if err != nil {
		return spotify.Authenticator{}.NewClient(&oauth2.Token{}), err
	}

	client := spotify.Authenticator{}.NewClient(token)

	return client, nil
}
