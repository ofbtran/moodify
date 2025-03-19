from app import db
from datetime import datetime

class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    mood_score = db.Column(db.Float, nullable=False)  # 1-10 scale
    energy_level = db.Column(db.Float)  # 1-10 scale
    activity_type = db.Column(db.String(64))  # e.g., 'working', 'exercising', 'relaxing'
    weather = db.Column(db.JSON)  # temperature, conditions, etc.
    notes = db.Column(db.Text)  # Optional text notes about mood
    location = db.Column(db.JSON)  # Optional location data
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'timestamp': self.timestamp.isoformat(),
            'mood_score': self.mood_score,
            'energy_level': self.energy_level,
            'activity_type': self.activity_type,
            'weather': self.weather,
            'notes': self.notes,
            'location': self.location
        } 