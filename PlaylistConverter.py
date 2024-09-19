import logging
import time
from typing import Optional
from SpotifyService import SpotifyService
from YouTubeService import YouTubeService

class PlaylistConverter:
    def __init__(self, spotify_service: SpotifyService, youtube_service: YouTubeService, delay_between_requests: int = 1):
        self.spotify_service = spotify_service
        self.youtube_service = youtube_service
        self.delay_between_requests = delay_between_requests

    def convert(self, spotify_playlist_id: str, youtube_playlist_title: str, youtube_playlist_description: str) -> Optional[str]:
        tracks = self.spotify_service.get_playlist_tracks(spotify_playlist_id)
        if not tracks:
            logging.warning("Keine Tracks in der Spotify-Playlist gefunden.")
            return None

        youtube_playlist_id = self.youtube_service.create_playlist(youtube_playlist_title, youtube_playlist_description)
        if not youtube_playlist_id:
            logging.error("YouTube-Playlist konnte nicht erstellt werden.")
            return None

        logging.info(f"Verarbeite {len(tracks)} Tracks aus der Spotify-Playlist.")

        for i, track in enumerate(tracks, start=1):
            logging.info(f"Verarbeite Track {i}/{len(tracks)}: {track}")
            self.youtube_service.search_and_add_to_playlist(track, youtube_playlist_id)
            logging.debug(f"Warte {self.delay_between_requests} Sekunde(n) vor der nächsten Anfrage.")
            time.sleep(self.delay_between_requests)

        total_quota = self.youtube_service.get_total_quota_usage()
        logging.info(f"Konvertierung abgeschlossen. Gesamte YouTube-API-Quota genutzt: {total_quota} Punkte")
        return youtube_playlist_id
