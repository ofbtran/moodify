from app import db
from datetime import datetime

class Track(db.Model):
    __tablename__ = 'tracks'
    
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(256), nullable=False)
    artist = db.Column(db.String(256), nullable=False)
    album = db.Column(db.String(256))
    duration_ms = db.Column(db.Integer)
    tempo = db.Column(db.Float)  # BPM
    energy = db.Column(db.Float)  # 0-1 scale
    danceability = db.Column(db.Float)  # 0-1 scale
    valence = db.Column(db.Float)  # 0-1 scale (musical positiveness)
    genres = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    listening_history = db.relationship('ListeningHistory', backref='track', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'spotify_id': self.spotify_id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration_ms': self.duration_ms,
            'tempo': self.tempo,
            'energy': self.energy,
            'danceability': self.danceability,
            'valence': self.valence,
            'genres': self.genres,
            'created_at': self.created_at.isoformat()
        }

class ListeningHistory(db.Model):
    __tablename__ = 'listening_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    listened_at = db.Column(db.DateTime, default=datetime.utcnow)
    duration_listened = db.Column(db.Integer)  # in seconds
    context = db.Column(db.JSON)  # weather, time of day, activity, etc.
    feedback = db.Column(db.String(16))  # 'like', 'skip', or None
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'track_id': self.track_id,
            'listened_at': self.listened_at.isoformat(),
            'duration_listened': self.duration_listened,
            'context': self.context,
            'feedback': self.feedback
        } 