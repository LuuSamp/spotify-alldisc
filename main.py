import dotenv
dotenv.load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_ids(item_list):
    ids = []
    for item in item_list:
        ids.append(item["id"])

    return ids

scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

artist_url = input("Artist URL: ")
artist_albums = sp.artist_albums(artist_url)["items"]
artist_name = sp.artist(artist_url)["name"]

playlist_name = f"{artist_name} Discography"

playlist = sp.user_playlist_create(user=sp.me()["id"], name=playlist_name, public=False)

for album in artist_albums:
    album_tracks = sp.album_tracks(album["id"])["items"]
    tracks_ids = get_ids(album_tracks)
    sp.playlist_add_items(playlist["id"], tracks_ids)
    
    

