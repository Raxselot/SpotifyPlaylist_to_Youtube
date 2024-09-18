import os
import logging
import google.auth.exceptions
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

class YouTubeService:
    def __init__(self, client_secrets_file):
        self.creds = None
        self.total_quota_usage = 0
        try:
            self.creds = self._load_credentials()
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(google.auth.transport.requests.Request())
                else:
                    self.creds = self._get_new_credentials(client_secrets_file)
                self._save_credentials()
            self.youtube = build('youtube', 'v3', credentials=self.creds)
        except (FileNotFoundError, google.auth.exceptions.RefreshError) as e:
            print(f"Error during authentication: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def _load_credentials(self):
        if os.path.exists('token.json'):
            try:
                return Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.force-ssl'])
            except Exception as e:
                print(f"Error loading credentials: {e}")
        return None

    def _get_new_credentials(self, client_secrets_file):
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, ['https://www.googleapis.com/auth/youtube.force-ssl']
            )
            return flow.run_local_server(port=0)
        except FileNotFoundError:
            print("Client secrets file not found.")
        except Exception as e:
            print(f"Error during OAuth flow: {e}")
        return None

    def _save_credentials(self):
        try:
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        except Exception as e:
            print(f"Error saving credentials: {e}")

    def create_playlist(self, title, description):
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
            logging.info(f"Created YouTube playlist with ID: {response['id']}, quota used: 50 points")
            return response['id']
        except HttpError as e:
            print(f"Error creating playlist: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None

    def search_and_add_to_playlist(self, query, playlist_id):
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=1
            ).execute()

            self.total_quota_usage += 100  
            logging.info(f"Search for query '{query}', quota used: 100 points")

            if search_response['items']:
                video_id = search_response['items'][0]['id']['videoId']
                self.add_video_to_playlist(video_id, playlist_id)
            else:
                print(f"No video found for query: {query}")
        except HttpError as e:
            print(f"Error during video search: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def add_video_to_playlist(self, video_id, playlist_id):
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
            logging.info(f"Added video {video_id} to playlist {playlist_id}, quota used: 50 points")
        except HttpError as e:
            print(f"Error adding video to playlist: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def get_total_quota_usage(self):
        return self.total_quota_usage
