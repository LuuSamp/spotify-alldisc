from functools import wraps
import dotenv
dotenv.load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyOauthError, SpotifyException
import sys
import math

def get_ids(item_list):
    ids = []
    for item in item_list:
        ids.append(item["id"])

    return ids

def pagination(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        limit = 50
        offset = 0

        result = func(*args, limit=limit, offset=offset, **kwargs)
        items = result["items"]
        
        while len(items) > 0:
            offset += len(items)
            items = func(*args, limit=limit, offset=offset, **kwargs)["items"]
            result["items"].extend(items)

        return result

    return wrapper

spotipy.Spotify.artist_albums = pagination(spotipy.Spotify.artist_albums)
spotipy.Spotify.album_tracks = pagination(spotipy.Spotify.album_tracks)

def filter_artist(tracks, artist_id):
    filtered_tracks = []
    for track in tracks:
        for artist in track["artists"]:
            if artist["id"] == artist_id:
                filtered_tracks.append(track)
                break

    return filtered_tracks

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
        artist = sp.artist(artist_url)
        artist_name = artist["name"]
        artist_id = artist["id"]
    except SpotifyException as err:
        print(err)
        print()
        print(f"Error fetching artist information. URL '{artist_url}' may be invalid.")
        sys.exit(1)
    
    playlist_name = f"{artist_name} Discography"

    print(f"Creating playlist '{playlist_name}'...")
    playlist = sp.user_playlist_create(user=sp.me()["id"], name=playlist_name, public=False)

    for album in artist_albums:
        print(f"Adding album '{album['name']}' to playlist...")
        album_tracks = sp.album_tracks(album["id"])["items"]
        filtered_tracks = filter_artist(album_tracks, artist_id)
        tracks_ids = get_ids(filtered_tracks)
        sp.playlist_add_items(playlist["id"], tracks_ids)
        
    print()
    print(f"Playlist '{playlist_name}' created successfully!")
        
if __name__ == "__main__":
    main()
    