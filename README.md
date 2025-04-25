# Spotify Control with Hand Gestures

A webcam-based app that lets you control Spotify using simple hand gestures. This project uses MediaPipe to detect your hand movements and Spotipy to control playback — no mouse or keyboard needed.

Keep reading for setup instructions and how to get started locally.

## How it works

Once the program launches, it opens a fullscreen webcam feed and starts tracking your hand using MediaPipe. The camera view is flipped like a mirror so gestures feel natural. The app detects which fingers are up or down, and uses that info to trigger different Spotify actions.

Here’s how the main gestures work:

- Fist gesture  
  - If your wrist is in the center: toggles play or pause  
  - If your wrist is near the left edge: previous track  
  - If your wrist is near the right edge: next track

- Thumb + Index finger up (others down)  
  - Moving your fingers closer or farther apart adjusts the volume  
  - The current volume shows up right between your fingers

- Single index finger pointing down (near the bottom of the screen)  
  - Lets you scrub through the current track by pointing horizontally across the screen  
  - The farther right you point, the further into the song it jumps

You’ll also see a live progress bar and song info (like title and artist) on screen while music is playing.

## How to run locally

This project is built with Python 3 and uses libraries like MediaPipe, OpenCV, and Spotipy. A webcam and a Spotify account with developer credentials are required.

Make sure you have Python 3.10 or higher installed.

1. Set up a virtual environment  
python -m venv venv  
.\venv\Scripts\activate

2. Install dependencies  
pip install -r requirements.txt

3. Add your Spotify credentials  
Create a .env file in the root of the project and add the following:

SPOTIPY_CLIENT_ID=your_client_id  
SPOTIPY_CLIENT_SECRET=your_client_secret  
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback

You can get these by registering a free app at https://developer.spotify.com/dashboard

4. Run the app  
python main.py