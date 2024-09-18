import requests
import logging

class SpotifyService:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_access_token()

    def _get_access_token(self):
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        auth_response_data = auth_response.json()
        return auth_response_data['access_token']

    def get_playlist_tracks(self, playlist_id):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(url, headers=headers)
        response_data = response.json()

        tracks = []
        for item in response_data['items']:
            track_name = item['track']['name']
            artist_name = item['track']['artists'][0]['name']
            tracks.append(f"{track_name} {artist_name}")
        
        logging.info(f"Fetched {len(tracks)} tracks from Spotify")
        return tracks
