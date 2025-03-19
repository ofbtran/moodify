from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.music import Track, ListeningHistory
from app import db
import requests
import base64
from datetime import datetime

music_bp = Blueprint('music', __name__)

def get_spotify_token():
    """Get Spotify access token using client credentials"""
    from config import Config
    
    auth_string = f"{Config.SPOTIFY_CLIENT_ID}:{Config.SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']

@music_bp.route('/search', methods=['GET'])
@jwt_required()
def search_tracks():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return jsonify({'error': 'Failed to search tracks'}), 500
    
    tracks = response.json()['tracks']['items']
    return jsonify(tracks)

@music_bp.route('/track/<spotify_id>', methods=['GET'])
@jwt_required()
def get_track_details(spotify_id):
    # First check if track exists in our database
    track = Track.query.filter_by(spotify_id=spotify_id).first()
    
    if not track:
        # If not, fetch from Spotify and store in database
        token = get_spotify_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        url = f"https://api.spotify.com/v1/tracks/{spotify_id}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return jsonify({'error': 'Track not found'}), 404
        
        spotify_data = response.json()
        
        # Get audio features
        features_url = f"https://api.spotify.com/v1/audio-features/{spotify_id}"
        features_response = requests.get(features_url, headers=headers)
        features = features_response.json()
        
        track = Track(
            spotify_id=spotify_id,
            title=spotify_data['name'],
            artist=spotify_data['artists'][0]['name'],
            album=spotify_data['album']['name'],
            duration_ms=spotify_data['duration_ms'],
            tempo=features['tempo'],
            energy=features['energy'],
            danceability=features['danceability'],
            valence=features['valence'],
            genres=[]  # Would need to fetch artist genres separately
        )
        
        db.session.add(track)
        db.session.commit()
    
    return jsonify(track.to_dict())

@music_bp.route('/track/<spotify_id>/play', methods=['POST'])
@jwt_required()
def record_track_play(spotify_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get or create track
    track = Track.query.filter_by(spotify_id=spotify_id).first()
    if not track:
        return jsonify({'error': 'Track not found'}), 404
    
    # Record listening history
    history = ListeningHistory(
        user_id=current_user_id,
        track_id=track.id,
        duration_listened=data.get('duration_listened', 0),
        context=data.get('context', {})
    )
    
    db.session.add(history)
    db.session.commit()
    
    return jsonify(history.to_dict()) 