import pandas as pd
import requests
import spotipy
import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials

# Parameters
CLIENT_ID = "9d513243ba43424f9588e7d353c5ec76"
CLIENT_SECRET = "e487c0e2f1b047249e200bdaa8d8be43"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
SCOPE = "user-follow-modify user-follow-read user-library-modify user-library-read " \
        "user-top-read playlist-read-collaborative playlist-read-private "


auth = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
token = auth.get_access_token()
token = token["access_token"]

track_name = 'Lucy'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ' + token,
}
params = [
    ('q', track_name),
    ('type', 'track'),
]
response = requests.get('https://api.spotify.com/v1/search',
                        headers=headers, params=params, timeout=5)
json = response.json()



token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)


sp = spotipy.Spotify(client_credentials_manager=auth)
track_results = sp.search(q='year:2020', type='track', limit=50, offset=0)

# create empty lists where the results are going to be stored
artist_name = []
track_name = []
popularity = []
track_id = []

for i in range(0,100,50):
    track_results = sp.search(q='year:2020', type='track', limit=50,offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])
df_tracks = pd.DataFrame({'artist_name':artist_name,'track_name':track_name,'track_id':track_id,'popularity':popularity})
print(df_tracks.shape)

token = util.prompt_for_user_token(username, SCOPE, client_id='client_id_number', client_secret='client_secret',
                                   redirect_uri='https://localhost.com/callback/')













CLIENT_SIDE_URL = "http://127.0.0.1:8050/"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
SCOPE = "user-top-read user-follow-modify user-library-read playlist-read-private " \
        "playlist-read-collaborative user-follow-read user-library-modify"
REDIRECT_URI = f"{CLIENT_SIDE_URL}/callback"
AUTH_DICT = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

url_args = "&".join([f"{key}={quote(val)}" for key, val in AUTH_DICT.items()])
auth_url = f"{SPOTIFY_AUTH_URL}/?{url_args}"
redirect(auth_url)