from flask import redirect, request, url_for, session
from flask_login import login_user
from spotipy.oauth2 import SpotifyOAuth
from models import db, User
from config import Config

sp_oauth = SpotifyOAuth(
    Config.SPOTIFY_CLIENT_ID,
    Config.SPOTIFY_CLIENT_SECRET,
    Config.SPOTIFY_REDIRECT_URI,
    scope="user-library-read user-top-read user-read-recently-played"
)

def spotify_login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    
    if token_info:
        session['token_info'] = token_info
        spotify_user = sp_oauth.get_cached_token()
        
        # Get or create user
        user = User.query.filter_by(spotify_id=spotify_user['id']).first()
        if not user:
            user = User(
                spotify_id=spotify_user['id'],
                username=spotify_user['display_name'],
                email=spotify_user['email'],
                spotify_token=token_info['access_token'],
                spotify_refresh_token=token_info['refresh_token']
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    else:
        return 'Failed to get token', 400

def refresh_token():
    token_info = session.get('token_info', None)
    if token_info:
        if sp_oauth.is_token_expired(token_info):
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = token_info
            user = User.query.filter_by(spotify_id=token_info['id']).first()
            if user:
                user.spotify_token = token_info['access_token']
                user.spotify_refresh_token = token_info['refresh_token']
                db.session.commit()
    return token_info