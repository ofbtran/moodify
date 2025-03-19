from .auth import auth_bp
from .music import music_bp
from .recommendations import recommendations_bp
from .user_profile import user_profile_bp

__all__ = [
    'auth_bp',
    'music_bp',
    'recommendations_bp',
    'user_profile_bp'
] 