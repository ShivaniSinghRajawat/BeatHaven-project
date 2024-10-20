from models import db, User, Song, UserQuizResponse, QuizQuestion
from spotify_utils import get_audio_features
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_quiz_based_recommendations(user_id, n_recommendations=5):
    user = User.query.get(user_id)
    if not user:
        return []

    # Get user's quiz responses
    user_responses = UserQuizResponse.query.filter_by(user_id=user_id).all()
    
    if not user_responses:
        return []  # User hasn't taken the quiz yet

    # Create a feature vector based on user's quiz responses
    user_features = create_feature_vector(user_responses)

    # Get all songs
    songs = Song.query.all()

    # Calculate similarity between user features and song features
    song_similarities = []
    for song in songs:
        song_features = create_song_feature_vector(song)
        
        # Combine quiz-based features with Spotify audio features
        combined_user_features = np.concatenate([user_features, get_spotify_features(song.spotify_id)])
        combined_song_features = np.concatenate([song_features, get_spotify_features(song.spotify_id)])
        
        similarity = cosine_similarity([combined_user_features], [combined_song_features])[0][0]
        song_similarities.append((song, similarity))

    # Sort songs by similarity
    song_similarities.sort(key=lambda x: x[1], reverse=True)

    # Return top N recommendations
    recommendations = [
        {'id': song.id, 'title': song.title, 'artist': song.artist}
        for song, _ in song_similarities[:n_recommendations]
    ]

    return recommendations

def create_feature_vector(user_responses):
    feature_vector = []
    for response in user_responses:
        question = QuizQuestion.query.get(response.question_id)
        if question:
            # Convert response to a numerical value
            feature_value = question.options.index(response.response) / len(question.options)
            feature_vector.append(feature_value)
    return feature_vector

def create_song_feature_vector(song):
    # This function should create a feature vector for a song
    # The features should correspond to the quiz questions
    features = [
        genre_to_value(song.genre),
        tempo_to_value(song.tempo),
        # Add more features based on your quiz questions
    ]
    return features

def genre_to_value(genre):
    # Convert genre to a numerical value
    genres = ['Pop', 'Rock', 'Hip Hop', 'Classical', 'Jazz', 'Electronic']
    return genres.index(genre) / len(genres) if genre in genres else 0.5

def tempo_to_value(tempo):
    # Convert tempo to a numerical value between 0 and 1
    return (tempo - 60) / (180 - 60)  # Assuming tempo range is 60-180 BPM

def get_spotify_features(spotify_id):
    features = get_audio_features(spotify_id)
    return [
        features['danceability'],
        features['energy'],
        features['valence'],
        features['acousticness'],
        features['instrumentalness'],
        features['liveness'],
        features['speechiness']
    ]

# Normalize features
scaler = StandardScaler()

def normalize_features(features):
    return scaler.fit_transform([features])[0]