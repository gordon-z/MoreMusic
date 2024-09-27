import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7a45f115736c4d6e8e31ecaf6b03f2a9",
                                                           client_secret="206a8900c2e64d908d6e1beaf44c501a"))

data = sp.search(q="Fireflies", type=["track"], market="ca")
song_id = data['tracks']['items'][0]['id']

output = sp.recommendations(seed_tracks=[song_id], limit=1)
recommendations = []

for recc in output['tracks']:
    recommendations.append({"track_id" : recc['id'], "track_name" : recc['name'], "track_uri" : recc['uri'], "album_name" : recc['album']['name'], 
                                             "album_art" : recc['album']['images'][0]['url'], "album_release_date" : recc['album']['release_date'], "artist_id" : recc['artists'][0]['id'],
                                             "artist_name" : recc['artists'][0]['name'], "artist_uri" : recc['artists'][0]['uri']})

print(recommendations)