import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config

def get_spotify_client(token_info=None):
    if token_info:
        return spotipy.Spotify(auth=token_info['access_token'])
    else:
        return spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope="user-library-read user-top-read user-read-recently-played"
        ))

def search_tracks(query, limit=10, token_info=None):
    sp = get_spotify_client(token_info)
    results = sp.search(q=query, type='track', limit=limit)
    tracks = results['tracks']['items']
    return [
        {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'preview_url': track['preview_url'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
        for track in tracks
    ]

def get_audio_features(track_id, token_info=None):
    sp = get_spotify_client(token_info)
    features = sp.audio_features(track_id)[0]
    return {
        'danceability': features['danceability'],
        'energy': features['energy'],
        'key': features['key'],
        'loudness': features['loudness'],
        'mode': features['mode'],
        'speechiness': features['speechiness'],
        'acousticness': features['acousticness'],
        'instrumentalness': features['instrumentalness'],
        'liveness': features['liveness'],
        'valence': features['valence'],
        'tempo': features['tempo'],
    }

def get_user_top_tracks(limit=20, time_range='medium_term', token_info=None):
    sp = get_spotify_client(token_info)
    top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return [
        {
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'preview_url': track['preview_url'],
            'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
        }
        for track in top_tracks['items']
    ]

def get_user_recently_played(limit=20, token_info=None):
    sp = get_spotify_client(token_info)
    recent_tracks = sp.current_user_recently_played(limit=limit)
    return [
        {
            'id': track['track']['id'],
            'name': track['track']['name'],
            'artist': track['track']['artists'][0]['name'],
            'album': track['track']['album']['name'],
            'preview_url': track['track']['preview_url'],
            'image_url': track['track']['album']['images'][0]['url'] if track['track']['album']['images'] else None,
            'played_at': track['played_at']
        }
        for track in recent_tracks['items']
    ]