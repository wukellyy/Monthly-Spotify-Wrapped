from flask import Flask, request, session, redirect, url_for, render_template

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

from dotenv import load_dotenv

import os

from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# REDIRECT_URI = "http://KEWWWY.pythonanywhere.com/callback"
REDIRECT_URI = "http://localhost:5000/callback"
SCOPE = "user-top-read"

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_handler=cache_handler,
)
sp = Spotify(auth_manager=sp_oauth)

@app.route("/")
def index():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('top_artists'))

@app.route("/callback")
def callback():
    sp_oauth.get_access_token(request.args["code"])
    return redirect(url_for('top_artists'))

@app.route("/top_artists")
def top_artists():
    # Check if the token is valid
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    # Get the current month and year
    now = datetime.now()
    current_month = now.strftime("%B")
    current_year = now.year

    # User's Top 5 Artists this month
    top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")
    artists = [{"name": artist["name"], "img": artist["images"][0]["url"]} for artist in top_artists["items"]]

    return render_template("top_artists.html", current_month=current_month, current_year=current_year, top_artists=artists)

@app.route("/top_songs")
def top_songs():
    # Check if the token is valid
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
    # Get the current month and year
    now = datetime.now()
    current_month = now.strftime("%B")
    current_year = now.year

    # User's Top 5 Songs this month
    top_tracks = sp.current_user_top_tracks(limit=5, time_range="short_term")
    tracks = []
    for track in top_tracks["items"]:
        artists_names = ", ".join(artist["name"] for artist in track["artists"])
        album_image_url = track["album"]["images"][0]["url"]
        tracks.append({"name": track["name"], "artist": artists_names, "img": album_image_url})

    return render_template("top_songs.html", current_month=current_month, current_year=current_year, top_tracks=tracks)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)