import requests
from config.settings import Config

def get_weather_data(location):
    """Get weather data from OpenWeatherMap API"""
    lat, lon = location['latitude'], location['longitude']
    url = f"{Config.WEATHER_API_URL}?lat={lat}&lon={lon}&appid={Config.WEATHER_API_KEY}"
    
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch weather data")
    
    data = response.json()
    return {
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'wind_speed': data['wind']['speed']
    } 