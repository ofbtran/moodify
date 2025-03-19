from models import User
from app import db
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered")
        
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already taken")
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def login_user(email, password):
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            raise ValueError("Invalid email or password")
        
        access_token = create_access_token(identity=user.id)
        return access_token, user
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id) 