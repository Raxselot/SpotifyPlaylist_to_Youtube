Projekt: 


The Spotify to Youtube Playlist Konverter is a Python Script das is able to konvert Spotify Playlist to Youtube Playlists. 

The Tool uses the Spotify API and the Youtube V4 API

Functions

Authentication: Save Acces to bouth apis of Youtube and Spotify
Playlist-Creation: Autmatic Creation of Youtube Playlists
Track Search and Adding: Searches the tracks out of Spotify Playlists, and adds it into the Created Youtube Playlists
Quota-Manegment: See how much Quota of the Youtube API is being used
Logging: Detailed Logging and Error Handling

Dependencies

Python 3.7 or Higher
Google API Accesdata
Sptofiy API Accesdata

Instalation 

Clone Repository
git clone https://github.com/Raxselot/SpotifyPlaylist_to_Youtube.git
cd SpotifyPlaylist_to_Youtube

Change the variables value in the .env
add your Client_secrets.json

Add your Playlist 

    spotify_playlist_id = ""     --> https://open.spotify.com/playlist/5FghkTTuq4SNdFJAp5uHQa  <--       !! 5FghkTTuq4SNdFJAp5uHQa !!THAT PART 
    youtube_playlist_title = "Push Youor Luck"         --> Chose name of your new Playlist 
    youtube_playlist_description = "Diese Playlist wurde von Spotify zu YouTube konvertiert."  --> Description for the New Playlist 


Logs you will see if code rund successfull: 
![image](https://github.com/user-attachments/assets/6a947e2d-3343-48f6-8748-d5bef003d352)


