from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.user_service import UserService
from datetime import datetime

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/preferences', methods=['GET', 'PUT'])
@jwt_required()
def manage_preferences():
    current_user_id = get_jwt_identity()
    
    if request.method == 'GET':
        try:
            preferences = UserService.get_user_preferences(current_user_id)
            return jsonify(preferences)
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
    
    data = request.get_json()
    try:
        user = UserService.update_preferences(current_user_id, data)
        return jsonify({'message': 'Preferences updated successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@user_profile_bp.route('/mood', methods=['POST', 'GET'])
@jwt_required()
def manage_mood():
    current_user_id = get_jwt_identity()
    
    if request.method == 'POST':
        data = request.get_json()
        try:
            mood_entry = UserService.record_mood(current_user_id, data)
            return jsonify(mood_entry.to_dict()), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
    
    # GET request - get mood history
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)
        
        mood_entries = UserService.get_mood_history(
            current_user_id,
            start_date=start_date,
            end_date=end_date
        )
        return jsonify([entry.to_dict() for entry in mood_entries])
    except ValueError as e:
        return jsonify({'error': str(e)}), 400 