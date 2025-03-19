from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.mood import MoodEntry
from models.music import ListeningHistory
from app import db
from datetime import datetime
import requests

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/preferences', methods=['GET', 'PUT'])
@jwt_required()
def manage_preferences():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if request.method == 'GET':
        return jsonify({
            'preferred_genres': user.preferred_genres,
            'preferred_artists': user.preferred_artists,
            'preferred_tempo': user.preferred_tempo,
            'preferred_energy': user.preferred_energy
        })
    
    data = request.get_json()
    user.preferred_genres = data.get('preferred_genres', user.preferred_genres)
    user.preferred_artists = data.get('preferred_artists', user.preferred_artists)
    user.preferred_tempo = data.get('preferred_tempo', user.preferred_tempo)
    user.preferred_energy = data.get('preferred_energy', user.preferred_energy)
    
    db.session.commit()
    return jsonify({'message': 'Preferences updated successfully'})

@user_profile_bp.route('/mood', methods=['POST', 'GET'])
@jwt_required()
def manage_mood():
    current_user_id = get_jwt_identity()
    
    if request.method == 'POST':
        data = request.get_json()
        
        # Get weather data if location is provided
        weather_data = None
        if data.get('location'):
            weather_data = get_weather_data(data['location'])
        
        mood_entry = MoodEntry(
            user_id=current_user_id,
            mood_score=data['mood_score'],
            energy_level=data.get('energy_level'),
            activity_type=data.get('activity_type'),
            weather=weather_data,
            notes=data.get('notes'),
            location=data.get('location')
        )
        
        db.session.add(mood_entry)
        db.session.commit()
        
        return jsonify(mood_entry.to_dict()), 201
    
    # GET request - get mood history
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = MoodEntry.query.filter_by(user_id=current_user_id)
    
    if start_date:
        query = query.filter(MoodEntry.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(MoodEntry.timestamp <= datetime.fromisoformat(end_date))
    
    mood_entries = query.order_by(MoodEntry.timestamp.desc()).all()
    
    return jsonify([entry.to_dict() for entry in mood_entries])

@user_profile_bp.route('/history', methods=['GET'])
@jwt_required()
def get_listening_history():
    current_user_id = get_jwt_identity()
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    history = ListeningHistory.query.filter_by(user_id=current_user_id)\
        .order_by(ListeningHistory.listened_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': [entry.to_dict() for entry in history.items],
        'total': history.total,
        'pages': history.pages,
        'current_page': history.page
    })

def get_weather_data(location):
    """Helper function to get weather data from OpenWeatherMap API"""
    from config import Config
    
    lat, lon = location['latitude'], location['longitude']
    url = f"{Config.WEATHER_API_URL}?lat={lat}&lon={lon}&appid={Config.WEATHER_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None 