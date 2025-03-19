from app import db
from datetime import datetime
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
import joblib

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False)  # Recommendation score
    context = db.Column(db.JSON)  # Context used for recommendation
    feedback = db.Column(db.String(16))  # 'like', 'skip', or None
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'track_id': self.track_id,
            'created_at': self.created_at.isoformat(),
            'score': self.score,
            'context': self.context,
            'feedback': self.feedback
        }

class RecommendationEngine:
    def __init__(self):
        self.svd = TruncatedSVD(n_components=100)
        self.context_model = RandomForestClassifier()
        self.is_trained = False
    
    def train(self, user_tracks, context_data):
        """
        Train the recommendation engine using user listening history and context data
        
        Args:
            user_tracks: List of track features (tempo, energy, etc.)
            context_data: List of context features (weather, time, etc.)
        """
        # Train SVD for collaborative filtering
        self.svd.fit(user_tracks)
        
        # Train context model
        self.context_model.fit(context_data, user_tracks)
        self.is_trained = True
    
    def get_recommendations(self, user_id, context, n_recommendations=10):
        """
        Generate personalized recommendations based on user history and current context
        
        Args:
            user_id: ID of the user
            context: Current context (weather, time, etc.)
            n_recommendations: Number of recommendations to generate
            
        Returns:
            List of recommended track IDs with scores
        """
        if not self.is_trained:
            raise ValueError("Recommendation engine not trained")
        
        # Get collaborative filtering scores
        cf_scores = self.svd.transform(user_tracks)
        
        # Get context-based scores
        context_scores = self.context_model.predict_proba(context)
        
        # Combine scores with weights
        final_scores = 0.6 * cf_scores + 0.4 * context_scores
        
        # Get top N recommendations
        top_indices = np.argsort(final_scores)[-n_recommendations:][::-1]
        
        return [(track_ids[i], final_scores[i]) for i in top_indices]
    
    def save_model(self, path):
        """Save the trained models to disk"""
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        joblib.dump({
            'svd': self.svd,
            'context_model': self.context_model
        }, path)
    
    def load_model(self, path):
        """Load trained models from disk"""
        models = joblib.load(path)
        self.svd = models['svd']
        self.context_model = models['context_model']
        self.is_trained = True 