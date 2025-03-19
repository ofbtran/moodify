from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    try:
        user = AuthService.register_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    try:
        access_token, user = AuthService.login_user(
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 401

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    
    try:
        user = AuthService.get_user_by_id(current_user_id)
        return jsonify(user.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 404 