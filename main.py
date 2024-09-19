import os
import logging
from SpotifyService import SpotifyService
from YouTubeService import YouTubeService
from PlaylistConverter import PlaylistConverter
from dotenv import load_dotenv

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    load_dotenv()

    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    if not spotify_client_id or not spotify_client_secret:
        logging.error("Spotify-Client-ID und/oder -Secret sind nicht gesetzt.")
        return

    youtube_client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE", "client_secrets.json")
    if not os.path.exists(youtube_client_secrets_file):
        logging.error(f"YouTube-Client-Geheimnisse-Datei '{youtube_client_secrets_file}' nicht gefunden.")
        return

    try:
        spotify_service = SpotifyService(spotify_client_id, spotify_client_secret)
        youtube_service = YouTubeService(youtube_client_secrets_file)
    except Exception as e:
        logging.error(f"Fehler bei der Initialisierung der Dienste: {e}")
        return

    converter = PlaylistConverter(spotify_service, youtube_service, delay_between_requests=1)

    spotify_playlist_id = "5FghkTTuq4SNdFJAp5uHQa" 
    youtube_playlist_title = "Push Youor Luck"
    youtube_playlist_description = "Diese Playlist wurde von Spotify zu YouTube konvertiert."

    youtube_playlist_id = converter.convert(spotify_playlist_id, youtube_playlist_title, youtube_playlist_description)
    if youtube_playlist_id:
        logging.info(f"YouTube-Playlist erfolgreich erstellt: {youtube_playlist_id}")
    else:
        logging.error("Fehler bei der Erstellung der YouTube-Playlist.")

if __name__ == "__main__":
    main()
