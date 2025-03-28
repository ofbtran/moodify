import requests
from config import Config

def get_weather_data(location):
    """Get weather data from OpenWeatherMap API"""
    lat, lon = location['latitude'], location['longitude']
    
    if lat is None or lon is None:
        raise ValueError("Invalid location")
    
    url = f"{Config.WEATHER_API_URL}?lat={lat}&lon={lon}&appid={Config.WEATHER_API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch weather data")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching weather data: {e}")
    
    data = response.json()
    
    return {
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
        'condition': data['weather'][0]['main'],
        'wind_speed': data['wind']['speed']
    } 