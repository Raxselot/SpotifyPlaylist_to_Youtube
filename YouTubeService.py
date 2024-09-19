import os
import logging
from typing import Optional
import google.auth.exceptions
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

class YouTubeService:
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'client_secrets.json'

    def __init__(self, client_secrets_file: Optional[str] = None):
        self.creds: Optional[Credentials] = None
        self.total_quota_usage: int = 0
        self.youtube = None

        client_secrets = client_secrets_file or self.CREDENTIALS_FILE
        try:
            self.creds = self._load_credentials()
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(google.auth.transport.requests.Request())
                else:
                    self.creds = self._get_new_credentials(client_secrets)
                self._save_credentials()
            self.youtube = build('youtube', 'v3', credentials=self.creds)
            logging.info("YouTubeService erfolgreich initialisiert.")
        except (FileNotFoundError, google.auth.exceptions.RefreshError) as e:
            logging.error(f"Authentifizierungsfehler: {e}")
            raise
        except Exception as e:
            logging.error(f"Unerwarteter Fehler: {e}")
            raise

    def _load_credentials(self) -> Optional[Credentials]:
        if os.path.exists(self.TOKEN_FILE):
            try:
                creds = Credentials.from_authorized_user_file(self.TOKEN_FILE, YOUTUBE_SCOPES)
                logging.info("Anmeldeinformationen erfolgreich geladen.")
                return creds
            except Exception as e:
                logging.warning(f"Fehler beim Laden der Anmeldeinformationen: {e}")
        return None

    def _get_new_credentials(self, client_secrets_file: str) -> Optional[Credentials]:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)
            logging.info("Neue Anmeldeinformationen erhalten.")
            return creds
        except FileNotFoundError:
            logging.error("Client-Geheimnisse-Datei nicht gefunden.")
        except Exception as e:
            logging.error(f"Fehler während des OAuth-Flows: {e}")
        return None

    def _save_credentials(self):
        try:
            with open(self.TOKEN_FILE, 'w') as token:
                token.write(self.creds.to_json())
            logging.info("Anmeldeinformationen erfolgreich gespeichert.")
        except Exception as e:
            logging.error(f"Fehler beim Speichern der Anmeldeinformationen: {e}")

    def create_playlist(self, title: str, description: str) -> Optional[str]:
        try:
            request = self.youtube.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                }
            )
            response = request.execute()
            self.total_quota_usage += 50 
            logging.info(f"Playlist erstellt: ID={response['id']}, Quota genutzt: 50 Punkte")
            return response['id']
        except HttpError as e:
            logging.error(f"Fehler beim Erstellen der Playlist: {e}")
        except Exception as e:
            logging.error(f"Unerwarteter Fehler beim Erstellen der Playlist: {e}")
        return None

    def search_and_add_to_playlist(self, query: str, playlist_id: str):
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=1
            ).execute()

            self.total_quota_usage += 100  
            logging.info(f"Suche nach '{query}', Quota genutzt: 100 Punkte")

            if search_response['items']:
                video_id = search_response['items'][0]['id']['videoId']
                self.add_video_to_playlist(video_id, playlist_id)
            else:
                logging.warning(f"Kein Video gefunden für die Suche: '{query}'")
        except HttpError as e:
            logging.error(f"Fehler bei der Videosuche: {e}")
        except Exception as e:
            logging.error(f"Unerwarteter Fehler bei der Videosuche: {e}")

    def add_video_to_playlist(self, video_id: str, playlist_id: str):
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            request.execute()
            self.total_quota_usage += 50  
            logging.info(f"Video {video_id} zur Playlist {playlist_id} hinzugefügt, Quota genutzt: 50 Punkte")
        except HttpError as e:
            logging.error(f"Fehler beim Hinzufügen des Videos zur Playlist: {e}")
        except Exception as e:
            logging.error(f"Unerwarteter Fehler beim Hinzufügen des Videos: {e}")

    def get_total_quota_usage(self) -> int:
        return self.total_quota_usage
