# Moodify - Context-Aware Music Recommendation System

Moodify is an intelligent music recommendation system that generates personalized playlists based on user mood, weather, time of day, and activity levels. The system uses a hybrid recommendation approach combining collaborative filtering with context-based weighting to provide the perfect soundtrack for any moment.

## Features

- **Smart Recommendations**: Hybrid recommendation engine using SVD (collaborative filtering) and Random Forest (context-based)
- **Mood Tracking**: Record and track your mood with context (weather, activity, time)
- **Weather Integration**: Real-time weather data from OpenWeatherMap API
- **Spotify Integration**: Seamless music playback and track information
- **User Preferences**: Customize your music preferences (genres, artists, tempo, energy)
- **Listening History**: Track your music listening habits and patterns
- **Feedback Loop**: Like/skip feedback to improve recommendations

## Project Structure

```
moodify/
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Application configuration
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   │   ├── music_controller.py
│   │   ├── recommendation_controller.py
│   │   └── user_controller.py
│   ├── helpers/
│   │   ├── __init__.py
│   │   ├── spotify_helper.py
│   │   └── weather_helper.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── music.py
│   │   ├── mood.py
│   │   └── recommendation.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── music_service.py
│   │   ├── recommendation_service.py
│   │   └── user_service.py
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
└── frontend/                  # React/Next.js frontend (coming soon)
```

### Directory Structure Explanation

1. **config/**
   - Contains application configuration
   - Environment variables and settings
   - Database and API configurations

2. **controllers/**
   - Handles HTTP requests and responses
   - Route definitions and request validation
   - Maps routes to appropriate services

3. **helpers/**
   - Utility functions and external API integrations
   - Spotify API helper for music data
   - Weather API helper for context data

4. **models/**
   - Database models and schemas
   - SQLAlchemy model definitions
   - Data structure definitions

5. **services/**
   - Business logic implementation
   - Database operations
   - Complex operations and algorithms

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user profile

### User Profile
- `GET/PUT /api/v1/profile/preferences` - Get/Update user preferences
- `POST/GET /api/v1/profile/mood` - Record/Get mood entries
- `GET /api/v1/profile/history` - Get listening history

### Music
- `GET /api/v1/music/search` - Search tracks
- `GET /api/v1/music/track/<spotify_id>` - Get track details
- `POST /api/v1/music/track/<spotify_id>/play` - Record track play

### Recommendations
- `GET /api/v1/recommendations/get` - Get personalized recommendations
- `POST /api/v1/recommendations/feedback` - Submit recommendation feedback
- `POST /api/v1/recommendations/train` - Retrain recommendation engine

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/moodify.git
   cd moodify
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Set up the database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. **Run the development server**
   ```bash
   flask run
   ```

## Required Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database configuration
DATABASE_URL=postgresql://username:password@localhost/moodify

# JWT configuration
JWT_SECRET_KEY=your-secret-key-here

# Spotify API configuration
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret

# Weather API configuration
WEATHER_API_KEY=your-openweathermap-api-key

# Flask configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
```

## External Services Required

1. **Spotify Developer Account**
   - Create an account at [Spotify Developer Dashboard](https://developer.spotify.com)
   - Create a new application
   - Get Client ID and Client Secret

2. **OpenWeatherMap API**
   - Sign up at [OpenWeatherMap](https://openweathermap.org)
   - Get an API key

3. **PostgreSQL Database**
   - Local installation or cloud service (e.g., Amazon RDS)

## Development

### Running Tests
```bash
python -m pytest
```

### Database Migrations
```bash
flask db migrate -m "description"
flask db upgrade
```

### Code Style
```bash
flake8
black .
```

## Deployment

The application is designed to be deployed on AWS with:
- Amazon RDS for PostgreSQL
- AWS ECS/EKS for container orchestration
- AWS S3 for model storage
- AWS CloudWatch for monitoring

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
