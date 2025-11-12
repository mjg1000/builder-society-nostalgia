import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from songModel import Song
from typing import List
from datetime import datetime

clientId = "bfe252e3e114469dad79efd1eeb441a9"
clientSecret = "6bce723b685e477cb9595f5909a3b6df"

client_credentials_manager = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def searchSongs(query: str) -> List[Song]:
    year = datetime.strptime(query, "%Y-%m-%d").year
    searchResults = sp.search(q=f"year:{year}", limit=1, type='track')

    songs = []
    for track in searchResults["tracks"]["items"]:
        song = Song(
            title = track["name"],
            artist = track["artists"][0]["name"],
            album = track["album"]["name"],
            date = track["album"]["release_date"],
            uri = track["uri"],
            spotify_id = track["id"]
        )

        songs.append(song)

    return songs

if __name__ == "__main__":

    while True:
        choice = input("Enter \ns - search \nq - quit")

        choice = choice.lower()

        if choice == 'q':
            break

        elif choice == 's':
            searchQuery = input("Enter search query: ")
            songs = searchSongs(searchQuery)

            if len(songs) > 0:
                print(f"Search Results: {len(songs)}")

                for i, song in enumerate(songs, start=1):
                    print(f"{i}: \nTitle - {song.title} \nArtist - {song.artist} \nURI - {song.uri} \nDate - {song.date}")

                print(songs[0].uri)
            else:
                print("No songs found")
