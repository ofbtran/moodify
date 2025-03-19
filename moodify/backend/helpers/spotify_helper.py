import base64
import requests
from config.settings import Config

def get_spotify_token():
    """Get Spotify access token using client credentials"""
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

def search_tracks(query, limit=10):
    """Search for tracks using Spotify API"""
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit={limit}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Failed to search tracks")
    
    return response.json()['tracks']['items']

def get_track_details(spotify_id):
    """Get detailed track information from Spotify"""
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get track details
    url = f"https://api.spotify.com/v1/tracks/{spotify_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Track not found")
    
    track_data = response.json()
    
    # Get audio features
    features_url = f"https://api.spotify.com/v1/audio-features/{spotify_id}"
    features_response = requests.get(features_url, headers=headers)
    features = features_response.json()
    
    return {
        'spotify_id': spotify_id,
        'title': track_data['name'],
        'artist': track_data['artists'][0]['name'],
        'album': track_data['album']['name'],
        'duration_ms': track_data['duration_ms'],
        'tempo': features['tempo'],
        'energy': features['energy'],
        'danceability': features['danceability'],
        'valence': features['valence']
    } 