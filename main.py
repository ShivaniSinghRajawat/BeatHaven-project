from flask import Flask, render_template
from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, login_required, current_user, logout_user
from models import db, User, Song, Playlist, UserSongInteraction, QuizQuestion, UserQuizResponse
from recommendation import get_quiz_based_recommendations
from karaoke import analyze_pitch
from auth import spotify_login, spotify_callback, refresh_token
from datetime import datetime
import os
from config import Config
from s3_utils import upload_file_to_s3, get_s3_url
from spotify_utils import search_tracks, get_audio_features, get_user_top_tracks, get_user_recently_played
import requests

app = Flask(__name__)


recently_played = [
    {"id": f"song-{i}", "title": f"Song Title {i}", "artist": f"Artist {i}", "album": f"Album {i}"} 
    for i in range(1, 9)
]

playlists = [
    {"id": f"playlist-{i}", "name": f"Playlist {i}", "song_count": 10} 
    for i in range(1, 9)
]

leaderboard = [
    {"id": "1", "name": "User1", "score": 950},
    {"id": "2", "name": "User2", "score": 880},
    {"id": "3", "name": "User3", "score": 750},
]

@app.route('/')
def hello_world():
    return render_template('home.html'
                        )

@app.route('/DiscoverMore')
def ello():
    return render_template('base.html',
                          recently_played=recently_played, 
                           playlists=playlists, 
                           leaderboard=leaderboard)
    
@app.route('/about')
def hello():
    return render_template('about.html')

@app.route('/contactus')
def hell():
    return render_template('contact us.html')

@app.route('/profile')
def hllo():
    return render_template('profile.html')

@app.route('/login')
def helo():
    return render_template('log in.html')

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)

