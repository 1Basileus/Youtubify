import spotipy
from spotipy.oauth2 import SpotifyOAuth
import httplib2
import os
import sys
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import apiclient

from youtubesearchpython import VideosSearch

CLIENT_SECRETS_FILE = "secret.json"
MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the secret.json file
    found at:

    %s

    with information from the Cloud Console
    https://cloud.google.com/console

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                               CLIENT_SECRETS_FILE))

YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service():
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_SCOPE,
        message=MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return apiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
            http=credentials.authorize(httplib2.Http()))

def add_video_to_playlist(youtube,videoID,playlistID):
      youtube.playlistItems().insert(
      part="snippet",
      body={
            'snippet': {
              'playlistId': playlistID, 
              'resourceId': {
                      'kind': 'youtube#video',
                  'videoId': videoID
                }
            }
    }
     ).execute()

def search_video(youtube,artist,song):
    search_string = artist + ' ' + song
    videosSearch = VideosSearch(search_string, limit = 10)
    try:
        result = videosSearch.result()['result'][0]
        print(result)
        return result['id']
    except:
        print('Song not found on Youtube: ', search_string)
        return ""

if __name__ == "__main__":
    with open('spotify.json') as json_file:
        data = json.load(json_file)
    client_id = data['client_id']
    client_secret = data['client_secret']
    playlistId = input('Enter the Spotify Playlist Id: ')
    yt_playlist_id = input('Enter the Youtube Playlist Id: ')
    print('')

    scope = "playlist-read-collaborative"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://127.0.0.1:9090', scope=scope))

    results = sp.playlist_items(playlistId)

    youtube = get_authenticated_service()

    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    print('')
    print('Starting...')
    for idx, item in enumerate(results['items']):
        track = item['track']
        artist = track['artists'][0]['name']
        song = track['name']
        print('Searching Song on Youtube: ', artist, " ", song)
        video_id = search_video(youtube,artist,song)
        if(video_id == ""):
            continue
        add_video_to_playlist(youtube,video_id,yt_playlist_id)