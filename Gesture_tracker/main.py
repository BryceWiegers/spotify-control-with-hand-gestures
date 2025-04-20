import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="user-modify-playback-state user-read-playback-state"
))

current = sp.current_playback()

if current and current.get("is_playing"):
    track = current["item"]["name"]
    artist = current["item"]["artists"][0]["name"]
    print(f"Now playing: {track} by {artist}")
else:
    print("Nothing's playing right now.")
