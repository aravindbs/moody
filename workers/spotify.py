import requests 
import yaml
import json
import sys
with open("../config.yml", "r") as f:
    config = yaml.load(f)

def get_token():
    url = 'https://accounts.spotify.com/api/token'

    headers = {'Authorization' : 'Basic ' + config['SPOTIFY']}

    data = {'grant_type' : 'client_credentials'}

    token = requests.post(url, headers=headers, data= data).json()

    access_token = token["access_token"]

    return access_token

def get_artist_ids():
    artist_ids = [] 
    url = 'https://api.spotify.com/v1/search'
    access_token = get_token()
    payload1 = { 
        'q' : 'sia',
        'type' : 'artist',
        'market' : 'US'
    }
    payload2 = { 
        'q' : 'drake',
        'type' : 'artist',
        'market' : 'US'
    }
    headers = {'Authorization' : 'Bearer ' + access_token, 'Content-Type' : 'application/json' }

    r1 = requests.get(url, params=payload2, headers=headers).json()
    r2 = requests.get(url, params=payload2, headers=headers).json()

    artist_ids.append(r1['artists']['items'][0]['id'])
    artist_ids.append(r2['artists']['items'][0]['id'])
    
    return artist_ids

if __name__ == '__main__': 

    access_token = get_token()
    artist_id = get_artist_ids()

    payload = {
        'seed_artists' : ','.join(artist_id), 
        'limit' : '10', 
        
        'min_energy' : '0.4', 
        'min_popularity' : '50', 
        'market' : 'US'
    }

    url = 'https://api.spotify.com/v1/recommendations'

    headers = {'Authorization' : 'Bearer ' + access_token }

    r = requests.get(url, params=payload, headers=headers)

    