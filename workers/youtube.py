import argparse
import yaml,json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pymongo
from __init__ import config, db 

DEVELOPER_KEY = config['YOUTUBE']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

  users = list(db.users.find({}))
  preferences = list(db.preferences.find({})) 
  emotions = list(db.emotions.find({}))
  langs = {}

  for pref in preferences: 
        langs[pref['username']] = pref['langs']

  for user in users:
        suggest = {}
        all_suggestions = []
        print(user['username']) 
        for emotion in emotions:
            if emotion['username'] == user['username']: 
                sadness = emotion['sadness']
                anger = emotion['anger'] 
        for lang in langs: 
          curr_langs = langs[user['username']]
        if sadness > 0.1:
          for lang in curr_langs: 
            print(lang)
            search_response = youtube.search().list(
              q= lang + 'comedy',
              part='id,snippet',
              maxResults=3, 
              type='video', 
              videoEmbeddable='true'
            ).execute()

            
          
            for search_result in search_response.get('items', []):
              suggest['name'] = search_result['snippet']['title']
              suggest['url'] = 'https://www.youtube.com/watch?v=' + search_result['id']['videoId']
              all_suggestions.append(suggest)
              suggest = {}
              #print(json.dumps(all_suggestions, indent=2))

        print(json.dumps(all_suggestions, indent=2))

        query = { 'username' : user['username'] }
        update = { 'username' : user['username'] , 'suggestion' : all_suggestions }
        db.video_suggestions.update(query, update, upsert=True)   

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--max-results', help='Max results', default=25)
    args = parser.parse_args()


    youtube_search(args)
