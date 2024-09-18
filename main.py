from SpotifyService import SpotifyService
from YouTubeService import YouTubeService
from PlaylistConverter import PlaylistConverter

def main():
    spotify_client_id = ""
    spotify_client_secret = "" 

    youtube_client_secrets_file = "client_secrets.json"

    spotify_service = SpotifyService(spotify_client_id, spotify_client_secret)
    youtube_service = YouTubeService(youtube_client_secrets_file)
    
    converter = PlaylistConverter(spotify_service, youtube_service)
    
    spotify_playlist_id = "37i9dQZF1DXcBWIGoYBM5M"     # https://open.spotify.com/playlist/              --->     5FghkTTuq4SNdFJAp5uHQa   <--- That part
    
    youtube_playlist_title = "Converted Spotify Playlist"
    youtube_playlist_description = "This playlist was converted from Spotify to YouTube"
    
    converter.convert(spotify_playlist_id, youtube_playlist_title, youtube_playlist_description)

if __name__ == "__main__":
    main()
