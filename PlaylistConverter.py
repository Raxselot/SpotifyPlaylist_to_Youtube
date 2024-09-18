import logging
import time

class PlaylistConverter:
    def __init__(self, spotify_service, youtube_service, delay_between_requests=1):
        self.spotify_service = spotify_service
        self.youtube_service = youtube_service
        self.delay_between_requests = delay_between_requests  

    def convert(self, spotify_playlist_id, youtube_playlist_title, youtube_playlist_description):
        tracks = self.spotify_service.get_playlist_tracks(spotify_playlist_id)
        youtube_playlist_id = self.youtube_service.create_playlist(youtube_playlist_title, youtube_playlist_description)
        
        logging.info(f"Processing {len(tracks)} tracks from the Spotify playlist.")
        
        for i, track in enumerate(tracks):
            logging.info(f"Processing track {i + 1}: {track}")
            self.youtube_service.search_and_add_to_playlist(track, youtube_playlist_id)
            
            logging.info(f"Waiting for {self.delay_between_requests} second(s) before the next request...")
            time.sleep(self.delay_between_requests)
        
        logging.info(f"Total YouTube API quota used: {self.youtube_service.get_total_quota_usage()} points")
