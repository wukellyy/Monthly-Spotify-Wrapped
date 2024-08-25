# Monthly Spotify Wrapped

A Flask application that utilizes the Spotify Web API to create a mini Spotify Wrapped, allowing Spotify users to see their top artists and top songs for the current month.

~~You can access the live version of this application at [this link](https://kewwwy.pythonanywhere.com/top_artists).~~

Note: I seems like users need to have their Spotify account email manually added in the User Management tab of the Spotify Developer Dashboard to access the live version of this application. I am currently working on a solution to streamline this process.

## Features

- Authenticate Spotify users via OAuth
- Display the top 5 artists for the current month
- Display the top 5 songs for the current month
- User-friendly interface with a simple and clean design

## Installation

### Prerequisites

- Python 3.7+
- Spotify Developer Account

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/KellyWu8/Monthly-Spotify-Wrapped.git
   cd Monthly-Spotify-Wrapped
   ```

2. **Create and activate a virtual environment:**

   - **macOS/Linux**
     ```bash
     $ python3 -m venv .venv
     $ . .venv/bin/activate
     ```
   - **Windows**
     ```bash
     > py -3 -m venv .venv
     > .venv\Scripts\activate
     ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   - Create a `.env` file in the root directory of the project and add your Spotify Client ID and Client Secret:
     ```
     CLIENT_ID="your_spotify_client_id"
     CLIENT_SECRET="your_spotify_client_secret"
     ```
     <sub>To get the `CLIENT_ID` and `CLIENT_SECRET`, you must create an app from the [Spotify Developer Dashboard](https://developer.spotify.com/).</sub>

5. **Run the application:**
   ```bash
   python main.py
   ```

## Using the Spotify API

I used a Python library called [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/), which makes interacting with the [Spotify Web API](https://developer.spotify.com/documentation/web-api) much easier.

### Authorization

Since we need to retrieve the user's top artists and top songs, we are using the [Authorization Code Flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow). Spotipy makes this whole process more simple and convenient by having `SpotifyOAuth`, which helps to authenticate users and gain access to their Spotify data.

An instance of `SpotifyOAuth` can be initialized with the following parameters:

- **client_id**: The Client ID provided by Spotify for your application.
- **client_secret**: The Client secret provided by Spotify for your application.
- **redirect_uri**: The URL to which Spotify will redirect users after they have logged in. This should match the Redirect URI you have configured in your Spotify application settings.
- **scope**: Comma separated string of scopes that specify the access privileges your application is requesting. See [Scopes Documentation](https://developer.spotify.com/documentation/web-api/concepts/scopes) for more information.
- **cache_handler**: An object that handles caching of the access and refresh tokens.

```python
sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_handler=cache_handler,
)
```

### Access Token

When a user visits the application for the first time, they will be redirected to Spotify to log in and authorize the application. After authorization, Spotify will redirect the user back to the app with an authorization code, which can be exchanged for an `access token`.

In this application, the `access token` is stored into the Flask session. We use Spotipy's `FlaskSessionCacheHandler` for this.

```python
cache_handler = FlaskSessionCacheHandler(session)
```

`Access tokens` have a limited lifespan. When an access token expires, you can use the refresh token to get a new access token without requiring the user to log in again. Thus, before making requests to the Spotify API, it’s important to validate that the access token is still valid. If it’s not, you should refresh it using the refresh token.

```python
if not sp_oauth.validate_token(cache_handler.get_cached_token()):
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)
```

### Fetching Spotify Data

Once authenticated, you can use the Spotify Web API to fetch various data such as the user's top artists, top tracks, playlists, and more. For example:

- **Fetching Top Artists:**

  ```python
  top_artists = sp.current_user_top_artists(limit=5, time_range="short_term")
  for artist in top_artists['items']:
      print(artist['name'])
  ```

- **Fetching Top Tracks:**
  ```python
  top_tracks = sp.current_user_top_tracks(limit=5, time_range="short_term")
  for track in top_tracks['items']:
      print(track['name'])
  ```

Check out both [Spotipy Documentation](https://spotipy.readthedocs.io/en/2.22.1/) and [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api) to see what methods are offered, and how the returned results are formatted.
