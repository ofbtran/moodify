from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # User preferences and context
    preferred_genres = db.Column(db.JSON)
    preferred_artists = db.Column(db.JSON)
    preferred_tempo = db.Column(db.Float)  # BPM
    preferred_energy = db.Column(db.Float)  # 0-1 scale
    
    # Relationships
    listening_history = db.relationship('ListeningHistory', backref='user', lazy=True)
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'preferred_genres': self.preferred_genres,
            'preferred_artists': self.preferred_artists,
            'preferred_tempo': self.preferred_tempo,
            'preferred_energy': self.preferred_energy
        } 