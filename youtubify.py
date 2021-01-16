import spotipy
from spotipy.oauth2 import SpotifyOAuth

if __name__ == "__main__":
    client_id = input('Enter your Spotify clientId: ')
    client_secret = input('Enter your Spotify clientSecret: ')

    scope = "playlist-read-collaborative"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='https://localhost', scope=scope))

    playlistId = input('Enter the PlaylistId: ')

    results = sp.playlist_items(playlistId)

    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])