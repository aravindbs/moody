import json,yaml
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from watson_developer_cloud import ToneAnalyzerV3
import pymongo
from __init__ import config, db 

tone_analyzer = ToneAnalyzerV3(
    version=config['watson']['version'],
    username=config['watson']['username'],
    password=config['watson']['password'], 
    url=config['watson']['url']
)

tweets = list(db.tweets.find({}))
users = list(db.users.find({}))
anger = fear = disgust = joy = sadness = 0 

for user in users:
    count = 0
    for tweet in tweets: 
        if(tweet['screen_name'] == user['twitter_handle']):
            text = tweet['text']
            tone = tone_analyzer.tone({'text': text},'application/json').get_result()

            anger = anger + tone['document_tone']['tone_categories'][0]['tones'][0]['score']
            disgust = disgust + tone['document_tone']['tone_categories'][0]['tones'][1]['score']
            fear = fear + tone['document_tone']['tone_categories'][0]['tones'][2]['score']
            joy = joy + tone['document_tone']['tone_categories'][0]['tones'][3]['score']
            sadness = sadness + tone['document_tone']['tone_categories'][0]['tones'][4]['score']
            count = count + 1

    anger = anger / count 
    disgust = disgust / count 
    fear = fear / count 
    joy = joy / count 
    sadness = sadness / count 

    query = { 'screen_name' : user['twitter_handle']}
    update = { 'username' : user['username'] , 'screen_name' : user['twitter_handle'], 'anger' : anger, 'disgust' : disgust, 'fear' : fear, 'joy' : joy, 'sadness' : sadness }
    db.emotions.update(query, update, upsert=True)
            





