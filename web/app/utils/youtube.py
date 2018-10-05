import argparse
import yaml,json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pymongo
from app.utils import config

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody


DEVELOPER_KEY = config['youtube']['YOUTUBE_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(users):
    	
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	preferences = list(db.preferences.find({})) 
	
	langs = {}

	for pref in preferences: 
		langs[pref['username']] = pref['langs']

	for user in users:
		print (user['username'])
		emotions = list(db.emotions.find({'username' : user['username']}))
		try:
			emotions = emotions[0]
			emotions.pop('_id', None)
			
			keywords = emotions['keywords']
			emotions = emotions['emotions']
			curr_emotion = None 
			for emotion in emotions: 
				if emotion['day'] == '0': 
					curr_emotion = emotion
					break 
			if curr_emotion == None: 
				continue
			print(curr_emotion)
			
			sadness = curr_emotion['sadness']
			anger = curr_emotion['anger']
			joy = emotion['joy']

			suggest = {}
			all_suggestions = []
			print(user['username']) 
			
					
			for lang in langs: 
				curr_langs = langs[user['username']]
			
			if sadness > joy:
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
			else: 
				for keyword in keywords: 
					search_response = youtube.search().list(
						q= keyword,
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


			print(json.dumps(all_suggestions, indent=2))

			query = { 'username' : user['username'] }
			update = { 'username' : user['username'] , 'suggestion' : all_suggestions }
			db.video_suggestions.update(query, update, upsert=True)   
		except: 
			pass

	return True 