import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/moodify')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # API configuration
    API_TITLE = 'Moodify API'
    API_VERSION = 'v1'
    
    # Weather API configuration
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
    
    # Music API configuration (e.g., Spotify)
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    # Recommendation engine configuration
    RECOMMENDATION_MODEL_PATH = os.getenv('RECOMMENDATION_MODEL_PATH', 'models/recommendation_model.pkl') 