from models import User, MoodEntry
from helpers.weather_helper import get_weather_data
from app import db

class UserService:
    @staticmethod
    def get_user_preferences(user_id):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        return {
            'preferred_genres': user.preferred_genres,
            'preferred_artists': user.preferred_artists,
            'preferred_tempo': user.preferred_tempo,
            'preferred_energy': user.preferred_energy
        }
    
    @staticmethod
    def update_preferences(user_id, preferences):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        user.preferred_genres = preferences.get('preferred_genres', user.preferred_genres)
        user.preferred_artists = preferences.get('preferred_artists', user.preferred_artists)
        user.preferred_tempo = preferences.get('preferred_tempo', user.preferred_tempo)
        user.preferred_energy = preferences.get('preferred_energy', user.preferred_energy)
        
        db.session.commit()
        return user
    
    @staticmethod
    def record_mood(user_id, mood_data):
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Get weather data if location is provided
        weather_data = None
        if mood_data.get('location'):
            weather_data = get_weather_data(mood_data['location'])
        
        mood_entry = MoodEntry(
            user_id=user_id,
            mood_score=mood_data['mood_score'],
            energy_level=mood_data.get('energy_level'),
            activity_type=mood_data.get('activity_type'),
            weather=weather_data,
            notes=mood_data.get('notes'),
            location=mood_data.get('location')
        )
        
        db.session.add(mood_entry)
        db.session.commit()
        
        return mood_entry
    
    @staticmethod
    def get_mood_history(user_id, start_date=None, end_date=None):
        query = MoodEntry.query.filter_by(user_id=user_id)
        
        if start_date:
            query = query.filter(MoodEntry.timestamp >= start_date)
        if end_date:
            query = query.filter(MoodEntry.timestamp <= end_date)
        
        return query.order_by(MoodEntry.timestamp.desc()).all() 