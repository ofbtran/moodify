from models import Track, ListeningHistory
from helpers.spotify_helper import get_track_details
from app import db

class MusicService:
    @staticmethod
    def search_tracks(query):
        from helpers.spotify_helper import search_tracks
        return search_tracks(query)
    
    @staticmethod
    def get_or_create_track(spotify_id):
        track = Track.query.filter_by(spotify_id=spotify_id).first()
        
        if not track:
            track_data = get_track_details(spotify_id)
            track = Track(**track_data)
            db.session.add(track)
            db.session.commit()
        
        return track
    
    @staticmethod
    def record_track_play(user_id, spotify_id, duration_listened=0, context=None):
        track = MusicService.get_or_create_track(spotify_id)
        
        history = ListeningHistory(
            user_id=user_id,
            track_id=track.id,
            duration_listened=duration_listened,
            context=context or {}
        )
        
        db.session.add(history)
        db.session.commit()
        
        return history
    
    @staticmethod
    def get_user_history(user_id, page=1, per_page=20):
        return ListeningHistory.query.filter_by(user_id=user_id)\
            .order_by(ListeningHistory.listened_at.desc())\
            .paginate(page=page, per_page=per_page) 