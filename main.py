import dotenv
dotenv.load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyOauthError, SpotifyException
import sys

def get_ids(item_list):
    ids = []
    for item in item_list:
        ids.append(item["id"])

    return ids


def main():
    scope = 'playlist-modify-private'
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    except SpotifyOauthError as err:
        print(err)
        print()
        print("Error during Spotify authentication. Please check your environment variables.")
        sys.exit(1)

    artist_url = input("Artist URL or ID: ")
    try:
        artist_albums = sp.artist_albums(artist_url)["items"]
        artist_name = sp.artist(artist_url)["name"]
    except SpotifyException as err:
        print(err)
        print()
        print(f"Error fetching artist information. URL '{artist_url}' may be invalid.")
        sys.exit(1)
    
    playlist_name = f"{artist_name} Discography"

    playlist = sp.user_playlist_create(user=sp.me()["id"], name=playlist_name, public=False)

    for album in artist_albums:
        album_tracks = sp.album_tracks(album["id"])["items"]
        tracks_ids = get_ids(album_tracks)
        sp.playlist_add_items(playlist["id"], tracks_ids)
        
if __name__ == "__main__":
    main()
    