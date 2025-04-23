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

while True:
    cmd = input(
        "\nType a command (play, pause, next, back, up, down, quit): ").strip().lower()

    if cmd == "play" or cmd == "pause":
        pause_or_play(sp)
    elif cmd == "next":
        next_track(sp)
    elif cmd == "back":
        previous_track(sp)
    elif cmd == "up":
        volume_up(sp)
    elif cmd == "down":
        volume_down(sp)
    elif cmd == "quit":
        print("Exiting.")
        break
    else:
        print("Didn't recognize that. Try again.")
