from models import Recommendation, ListeningHistory, Track
from models.recommendation import RecommendationEngine
from app import db
import numpy as np

class RecommendationService:
    def __init__(self):
        self.engine = RecommendationEngine()
    
    def get_recommendations(self, user_id, context, n_recommendations=10):
        # Get user's listening history
        history = ListeningHistory.query.filter_by(user_id=user_id).all()
        
        # Prepare training data
        user_tracks = []
        context_data = []
        
        for entry in history:
            track = entry.track
            user_tracks.append([
                track.tempo,
                track.energy,
                track.danceability,
                track.valence
            ])
            context_data.append(entry.context)
        
        # Train the engine if we have data
        if user_tracks:
            self.engine.train(user_tracks, context_data)
        
        # Get recommendations
        recommendations = self.engine.get_recommendations(
            user_id,
            context,
            n_recommendations
        )
        
        # Create recommendation records
        for track_id, score in recommendations:
            recommendation = Recommendation(
                user_id=user_id,
                track_id=track_id,
                score=score,
                context=context
            )
            db.session.add(recommendation)
        
        db.session.commit()
        
        # Get track details
        track_ids = [rec[0] for rec in recommendations]
        tracks = Track.query.filter(Track.id.in_(track_ids)).all()
        
        # Create response
        response = []
        for track, (_, score) in zip(tracks, recommendations):
            response.append({
                'track': track.to_dict(),
                'score': score
            })
        
        return response
    
    def record_feedback(self, user_id, recommendation_id, feedback):
        recommendation = Recommendation.query.get(recommendation_id)
        
        if not recommendation or recommendation.user_id != user_id:
            raise ValueError("Recommendation not found")
        
        recommendation.feedback = feedback
        db.session.commit()
        
        return recommendation
    
    def train_engine(self):
        """Retrain the recommendation engine with all user data"""
        history = ListeningHistory.query.all()
        
        if not history:
            return
        
        # Prepare training data
        user_tracks = []
        context_data = []
        
        for entry in history:
            track = entry.track
            user_tracks.append([
                track.tempo,
                track.energy,
                track.danceability,
                track.valence
            ])
            context_data.append(entry.context)
        
        # Train the engine
        self.engine.train(user_tracks, context_data)
        
        # Save the trained model
        self.engine.save_model('models/recommendation_model.pkl') 