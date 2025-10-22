# spotify-alldisc
Get the full discography of an artist into a single playlist. Made for those who want to listen to all songs of an artist instead of the select few Spotify lets you!

# Usage
You need Python installed on your machine.

## Making a Spotify App
First, you should create an app following [this official tutorial](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

## Defining Environment Variables
Create a `.env` file in the root of your project and add the following variables:
```
SPOTIPY_CLIENT_ID=<your_client_id>
SPOTIPY_CLIENT_SECRET=<your_client_secret>
SPOTIPY_REDIRECT_URI=<your_redirect_uri>
```
Replace `<your_client_id>`, `<your_client_secret>`, and `<your_redirect_uri>` with the values from your Spotify app.

## Installing Dependencies
Make sure you have the required dependencies installed. You can do this by running:
```
pip install -r requirements.txt
```

## Running the Script
Run the script using Python:
```python main.py
```

When you run the app for the first time, a browser window will open and ask you to log in to your Spotify account and authorize the app.

After authorization, you will be prompted to enter the Spotify Artist URL. The script will then create a private playlist in your Spotify account containing the full discography of the specified artist. The name of the playlist, by default, will be "<Artist Name> Discography".