from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.recommendation_service import RecommendationService

recommendations_bp = Blueprint('recommendations', __name__)
recommendation_service = RecommendationService()

@recommendations_bp.route('/get', methods=['GET'])
@jwt_required()
def get_recommendations():
    current_user_id = get_jwt_identity()
    context = request.args.get('context', {})
    
    try:
        recommendations = recommendation_service.get_recommendations(
            user_id=current_user_id,
            context=context,
            n_recommendations=10
        )
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        recommendation = recommendation_service.record_feedback(
            user_id=current_user_id,
            recommendation_id=data['recommendation_id'],
            feedback=data['feedback']
        )
        return jsonify({'message': 'Feedback recorded successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@recommendations_bp.route('/train', methods=['POST'])
@jwt_required()
def train_recommendation_engine():
    try:
        recommendation_service.train_engine()
        return jsonify({'message': 'Recommendation engine trained successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 