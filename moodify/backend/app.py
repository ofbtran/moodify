from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.settings import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints from controllers
    from controllers.auth_controller import auth_bp
    from controllers.music_controller import music_bp
    from controllers.recommendation_controller import recommendations_bp
    from controllers.user_controller import user_profile_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(music_bp, url_prefix='/api/v1/music')
    app.register_blueprint(recommendations_bp, url_prefix='/api/v1/recommendations')
    app.register_blueprint(user_profile_bp, url_prefix='/api/v1/profile')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 