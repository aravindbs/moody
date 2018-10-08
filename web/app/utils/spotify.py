import requests 
import yaml
import json
import sys
import pymongo
from app.utils import config

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody

def get_token():
    url = 'https://accounts.spotify.com/api/token'

    headers = {'Authorization' : 'Basic ' + config['spotify']['SPOTIFY_KEY']}

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

def spotify(user):
    print ( 'spotify ' + user[0]['username'])
    preferences = list(db.preferences.find({})) 
    artists = {}
    
    genres = {}
    for pref in preferences: 
        artists[pref['username']] = pref['artists']
        #langs[pref['username']] = pref['langs']
        #genres[pref['username']] = pref['genres']
    
    access_token = get_token()
    #for user in users: 
   # print(user[0]['username'])
    #user_genres = genres[user['username']]
    artist_ids = get_artist_ids(artists[user[0]['username']])
    #print(artist_ids)
    try:
        emotions = list(db.emotions.find({'username' : user[0]['username']}))

        if emotions == None:
	        return True
        emotions = emotions[0]
        emotions.pop('_id', None)
        emotions = emotions['emotions']
        curr_emotion = None 
        for emotion in emotions: 
            if emotion['day'] == '0': 
                curr_emotion = emotion
                break 
        if curr_emotion == None: 
            return True
     #   print(curr_emotion)
        
        sadness = curr_emotion['sadness']
        anger = curr_emotion['anger'] 

        payload = {
            'seed_artists' : ','.join(artist_ids), 
            #'seed_genres' : ','.join(user_genres),
            'limit' : '5',
            'target_valence' : sadness if sadness > anger and sadness > 0.4 else 0.5 ,
            'taget_energy' : sadness if sadness > anger and sadness > 0.4 else 0.2,
            'target_instrumentalness' : 0.7 if anger > sadness and anger > 0.4 else 0.3, #instrumental music in angry
            'target_danceability': 0.2 if anger > sadness and anger > 0.4 else 0.5,
            'min_popularity' : '50', 
            'market' : 'US'
        }


        url = 'https://api.spotify.com/v1/recommendations'

        headers = {'Authorization' : 'Bearer ' + access_token }

        r = requests.get(url, params=payload, headers=headers).json()
        tracks = r['tracks']
        suggest = {}
        all_suggestions = []
        for track in tracks: 
            suggest['name'] = track['name']
            url = track['external_urls']['spotify']
           # print(url)
            index = url.find('/track') 
            url = url[:index] + '/embed' + url[index:]
           # print(url)
            suggest['url'] = url
            suggest['artist'] = track['artists'][0]['name']
            all_suggestions.append(suggest)
            suggest = {}
        query = { 'username' : user[0]['username'] }
        update = { 'username' : user[0]['username'] , 'suggestion' : all_suggestions }
        db.music_suggestions.update(query, update, upsert=True)
    
    except Exception as e: 
        return e 

    return True 