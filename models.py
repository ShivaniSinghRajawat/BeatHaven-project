from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from s3_utils import get_s3_url

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    spotify_id = db.Column(db.String(50), unique=True)
    spotify_token = db.Column(db.String(220))
    spotify_refresh_token = db.Column(db.String(220))
    playlists = db.relationship('Playlist', backref='user', lazy='dynamic')
    quiz_responses = db.relationship('UserQuizResponse', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    s3_key = db.Column(db.String(200), unique=True, nullable=False)
    spotify_id = db.Column(db.String(22), unique=True)
    tempo = db.Column(db.Float)
    energy = db.Column(db.Float)
    danceability = db.Column(db.Float)
    valence = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    release_year = db.Column(db.Integer)
    is_instrumental = db.Column(db.Boolean)
    dominant_instrument = db.Column(db.String(50))
    lyrical_content = db.Column(db.String(50))
    mood = db.Column(db.String(50))
    artist_type = db.Column(db.String(20))
    experimental_score = db.Column(db.Float)
    language = db.Column(db.String(20))

    @property
    def stream_url(self):
        return get_s3_url(self.s3_key)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary='playlist_songs', backref='playlists')

playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class UserSongInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    interaction_type = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    options = db.Column(db.JSON, nullable=False)

class UserQuizResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('quiz_question.id'), nullable=False)
    response = db.Column(db.String(100), nullable=False)