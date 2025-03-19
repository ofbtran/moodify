from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recommendation import Recommendation, RecommendationEngine
from models.mood import MoodEntry
from models.music import Track
from app import db
import requests
from datetime import datetime

recommendations_bp = Blueprint('recommendations', __name__)
recommendation_engine = RecommendationEngine()

@recommendations_bp.route('/get', methods=['GET'])
@jwt_required()
def get_recommendations():
    current_user_id = get_jwt_identity()
    
    # Get current context
    context = request.args.get('context', {})
    
    # Get user's latest mood entry
    latest_mood = MoodEntry.query.filter_by(user_id=current_user_id)\
        .order_by(MoodEntry.timestamp.desc())\
        .first()
    
    if latest_mood:
        context.update({
            'mood_score': latest_mood.mood_score,
            'energy_level': latest_mood.energy_level,
            'activity_type': latest_mood.activity_type,
            'weather': latest_mood.weather
        })
    
    # Get recommendations from engine
    recommendations = recommendation_engine.get_recommendations(
        current_user_id,
        context,
        n_recommendations=10
    )
    
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
    
    return jsonify(response)

@recommendations_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    recommendation = Recommendation.query.get(data['recommendation_id'])
    
    if not recommendation or recommendation.user_id != current_user_id:
        return jsonify({'error': 'Recommendation not found'}), 404
    
    recommendation.feedback = data['feedback']
    db.session.commit()
    
    return jsonify({'message': 'Feedback recorded successfully'})

@recommendations_bp.route('/train', methods=['POST'])
@jwt_required()
def train_recommendation_engine():
    # This endpoint should be called periodically to retrain the recommendation engine
    # with new user data
    
    # Get all user listening history
    from models.music import ListeningHistory
    listening_history = ListeningHistory.query.all()
    
    # Prepare training data
    user_tracks = []
    context_data = []
    
    for history in listening_history:
        track = history.track
        user_tracks.append([
            track.tempo,
            track.energy,
            track.danceability,
            track.valence
        ])
        
        context_data.append(history.context)
    
    # Train the engine
    recommendation_engine.train(user_tracks, context_data)
    
    # Save the trained model
    recommendation_engine.save_model('models/recommendation_model.pkl')
    
    return jsonify({'message': 'Recommendation engine trained successfully'}) 