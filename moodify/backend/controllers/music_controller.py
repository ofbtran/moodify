from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.music_service import MusicService

music_bp = Blueprint('music', __name__)

@music_bp.route('/search', methods=['GET'])
@jwt_required()
def search_tracks():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    
    try:
        tracks = MusicService.search_tracks(query)
        return jsonify(tracks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@music_bp.route('/track/<spotify_id>', methods=['GET'])
@jwt_required()
def get_track_details(spotify_id):
    try:
        track = MusicService.get_or_create_track(spotify_id)
        return jsonify(track.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@music_bp.route('/track/<spotify_id>/play', methods=['POST'])
@jwt_required()
def record_track_play(spotify_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        history = MusicService.record_track_play(
            user_id=current_user_id,
            spotify_id=spotify_id,
            duration_listened=data.get('duration_listened', 0),
            context=data.get('context', {})
        )
        return jsonify(history.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@music_bp.route('/history', methods=['GET'])
@jwt_required()
def get_listening_history():
    current_user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    try:
        history = MusicService.get_user_history(
            user_id=current_user_id,
            page=page,
            per_page=per_page
        )
        return jsonify({
            'items': [entry.to_dict() for entry in history.items],
            'total': history.total,
            'pages': history.pages,
            'current_page': history.page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 