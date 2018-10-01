import requests 
import yaml
import json
import sys
import pymongo
with open("../config.yml", "r") as f:
    config = yaml.load(f)

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody

def get_token():
    url = 'https://accounts.spotify.com/api/token'

    headers = {'Authorization' : 'Basic ' + config['SPOTIFY']}

    data = {'grant_type' : 'client_credentials'}

    token = requests.post(url, headers=headers, data= data).json()

    access_token = token["access_token"]

    return access_token

def get_artist_ids(artists):
    artist_ids = [] 
    url = 'https://api.spotify.com/v1/search'
    access_token = get_token()
    
    for artist in artists: 
        payload = { 
            'q' : artist,
            'type' : 'artist',
            'market' : 'US'
        }
        headers = {'Authorization' : 'Bearer ' + access_token, 'Content-Type' : 'application/json' }

        r = requests.get(url, params=payload, headers=headers).json()

        artist_ids.append(r['artists']['items'][0]['id'])
            
    return artist_ids

if __name__ == '__main__': 

    users = list(db.users.find({}))
    preferences = list(db.preferences.find({})) 
    emotions = list(db.emotions.find({}))

    artists = {}
    langs = {}
    genres = {}
    for pref in preferences: 
        artists[pref['username']] = pref['artists']
        langs[pref['username']] = pref['langs']
        #genres[pref['username']] = pref['genres']
    
    access_token = get_token()
    for user in users: 
        #user_genres = genres[user['username']]
        artist_ids = get_artist_ids(artists[user['username']])
        print(artist_ids)

        for emotion in emotions:
            if emotion['username'] == user['username']: 
                sadness = emotion['sadness']
                anger = emotion['anger'] 

        payload = {
            'seed_artists' : ','.join(artist_ids), 
            #'seed_genres' : ','.join(user_genres),
            'limit' : '5',
            'target_valence' : sadness if sadness > anger else 0.5 ,
            'taget_energy' : sadness if sadness > anger else 0.2,
            'target_instrumentalness' : 0.7 if anger > sadness else 0.3, #instrumental music in angry
            'target_danceability': 0.2 if anger > sadness else 0.5,
            'min_popularity' : '50', 
            'market' : 'US'
        }

        url = 'https://api.spotify.com/v1/recommendations'

        headers = {'Authorization' : 'Bearer ' + access_token }

        r = requests.get(url, params=payload, headers=headers).json()
        tracks = r['tracks']
        urls = []
        names = []
        for track in tracks: 
            print (track['external_urls']['spotify'])
            urls.append(track['external_urls']['spotify'])
            print (track['name'])
            names.append(track['name'])



        query = { 'username' : user['username'] }
        update = { 'username' : user['username'] , 'urls' : urls, 'names' : names }
        db.music_suggestions.update(query, update, upsert=True)


