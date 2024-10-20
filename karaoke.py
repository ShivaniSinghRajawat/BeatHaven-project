import librosa
import numpy as np
from spotify_utils import get_audio_features

def analyze_pitch(audio_data, spotify_track_id):
    # Load the audio file
    y, sr = librosa.load(audio_data)
    
    # Extract pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
    # Get the pitch with the highest magnitude for each frame
    pitch = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch.append(pitches[index, t])
    
    # Remove zero frequencies
    pitch = [p for p in pitch if p > 0]
    
    # Calculate pitch accuracy
    if len(pitch) > 0:
        mean_pitch = np.mean(pitch)
        pitch_std = np.std(pitch)
        pitch_range = max(pitch) - min(pitch)
        
        # Get Spotify audio features
        spotify_features = get_audio_features(spotify_track_id)
        
        # Calculate pitch accuracy score
        pitch_accuracy = max(0, 100 - pitch_std)
        
        # Calculate rhythm accuracy using Spotify's tempo
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        rhythm_accuracy = 100 - min(100, abs(tempo - spotify_features['tempo']))
        
        # Calculate energy match
        energy_match = 100 - abs(librosa.feature.rms(y=y).mean() * 100 - spotify_features['energy'] * 100)
        
        # Calculate overall score
        final_score = (pitch_accuracy * 0.4 + rhythm_accuracy * 0.4 + energy_match * 0.2)
    else:
        final_score = 0
    
    return round(final_score, 2)

def get_lyrics_timing(spotify_track_id):
    # This is a placeholder function. Spotify doesn't provide lyrics timing.
    # You might need to use a third-party service or manually sync lyrics.
    pass