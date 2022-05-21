from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
date = input("Which year you want to travel to? The format must be YYYY-MM-DD: ")
web = requests.get(f"{URL}{date}")
soup = BeautifulSoup(web.text, "html.parser")
songs = [a.getText().strip() for a in soup.select("li #title-of-a-story")]

print(songs)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                               client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
                                               redirect_uri="http://example.com",
                                               scope="user-library-read playlist-modify-private playlist-modify-public playlist-read-private"))

user_id = sp.current_user().get('id')
tracks =[]
YYYY = date[0:4]
for song in songs:
    result = sp.search(q=f"track:{song} year:{YYYY}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        tracks.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(tracks)
playlist = sp.user_playlist_create(user_id, f"time-machine-{date}")

sp.playlist_add_items( playlist_id=playlist['id'], items=tracks)