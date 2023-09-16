from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time
from collections import Counter


app = Flask(__name__)


def categorize_song_mood(song_features):
    tempo = song_features.get("tempo", 0)  # Tempo in BPM
    valence = song_features.get("valence", 0)  # Valence (positiveness) ranging from 0 to 1
    energy = song_features.get("energy", 0)  # Energy ranging from 0 to 1
    
    mood_categories = {
        "Energetic": {"tempo": (100, 200), "valence": (0.5, 1.0), "energy": (0.5, 1.0)},
        "Happy": {"tempo": (80, 160), "valence": (0.5, 1.0), "energy": (0.4, 1.0)},
        "Sad": {"tempo": (40, 100), "valence": (0.1, 0.5), "energy": (0.1, 0.6)},
        "Calm": {"tempo": (40, 100), "valence": (0.3, 0.7), "energy": (0.1, 0.5)},
        "Angry": {"tempo": (80, 160), "valence": (0.1, 0.5), "energy": (0.7, 1.0)},
        "Relaxed": {"tempo": (40, 100), "valence": (0.4, 0.8), "energy": (0.1, 0.4)},
    }

    for mood, thresholds in mood_categories.items():
        if (
            thresholds["tempo"][0] <= tempo <= thresholds["tempo"][1]
            and thresholds["valence"][0] <= valence <= thresholds["valence"][1]
            and thresholds["energy"][0] <= energy <= thresholds["energy"][1]
        ):
            return mood
    return "Unknown"


from collections import Counter

# Function to calculate overall mood
def calculate_overall_mood(all_songs_mood):
    # Count the occurrences of each mood
    mood_counts = Counter(all_songs_mood)
    
    # Sort mood counts in descending order
    sorted_mood_counts = mood_counts.most_common()
    
    # Iterate through sorted mood counts
    for mood, count in sorted_mood_counts:
        if mood != "Unknown":
            return mood  # Return the first non-unknown mood
    # If all moods are unknown, return "Unknown" (or another default mood)
    return "Unknown"


app.secret_key = os.environ.get("SECRET_KEY") 
app.config['SESSION_COOKIE_NAME'] = 'spotify-login-session'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

# Checks to see if token is valid and gets a new token if not
@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])

    user_profile = sp.current_user() # retriving user name
    username = user_profile['id']
    
    return render_template("mood_analysis.html", username=username)

@app.route('/getMood')
def getMood():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect("/")
    sp = spotipy.Spotify(auth=token_info['access_token'])

    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)['items']
        iter += 1
        all_songs += items
        if (len(items) < 50):
            break
    all_songs_mood = []
    song_data = []
    for song in all_songs:
        song_id = song["track"]["id"]
        song_name = song["track"]["name"]
        artist_name = song["track"]["artists"][0]["name"]
        song_image = song["track"]["album"]["images"][0]["url"]


        song_features = sp.audio_features(song_id)[0]

        mood = categorize_song_mood(song_features)
        all_songs_mood.append(mood)

        song_data.append({"name" : song_name, "artist": artist_name, "image" : song_image, "mood": mood})
    common_mood = calculate_overall_mood(all_songs_mood)

    return render_template("get_mood.html", common_mood=common_mood, song_data=song_data)



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="id",
        client_secret="secret",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-email"
    )

