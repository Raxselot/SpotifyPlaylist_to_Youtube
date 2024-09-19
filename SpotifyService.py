import os
import logging
from typing import List
import requests
from requests.exceptions import HTTPError

class SpotifyService:
    TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: str = self.get_access_token()

    def get_access_token(self) -> str:
        try:
            response = requests.post(
                self.TOKEN_URL,
                data={'grant_type': 'client_credentials'},
                auth=(self.client_id, self.client_secret)
            )
            response.raise_for_status()
            auth_data = response.json()
            logging.info("Spotify-Zugriffstoken erfolgreich abgerufen.")
            return auth_data['access_token']
        except HTTPError as http_err:
            logging.error(f"HTTP-Fehler beim Abrufen des Zugriffstokens: {http_err}")
            raise
        except Exception as e:
            logging.error(f"Fehler beim Abrufen des Zugriffstokens: {e}")
            raise

    def get_playlist_tracks(self, playlist_id: str) -> List[str]:
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        tracks = []
        try:
            while url:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

                for item in data.get('items', []):
                    track = item.get('track')
                    if track:
                        track_name = track.get('name', 'Unbekannter Titel')
                        artists = ", ".join(artist.get('name', 'Unbekannter Künstler') for artist in track.get('artists', []))
                        tracks.append(f"{track_name} {artists}")

                url = data.get('next') 
                logging.info(f"Abgerufene Tracks: {len(tracks)}")
        except HTTPError as http_err:
            logging.error(f"HTTP-Fehler beim Abrufen der Playlist-Tracks: {http_err}")
        except Exception as e:
            logging.error(f"Fehler beim Abrufen der Playlist-Tracks: {e}")

        return tracks
