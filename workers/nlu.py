import json,yaml
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from watson_developer_cloud import ToneAnalyzerV3
import pymongo
import datetime

from __init__ import config, db 

tone_analyzer = ToneAnalyzerV3(
    version=config['watson_tone']['TONE_VERSION'],
    username=config['watson_tone']['TONE_USERNAME'],
    password=config['watson_tone']['TONE_PASSWORD'], 
    url=config['watson_tone']['TONE_URL']
)

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=config['watson_nlu']['NLU_USERNAME'],
  password=config['watson_nlu']['NLU_PASSWORD'],
  version=config['watson_nlu']['NLU_VERSION'])

while(1): 
    today = datetime.datetime.now()
    tweets = list(db.tweets.find({}))
    users = list(db.users.find({}))

    for user in users:
        db_keywords = [] 
        print(user['username'])
        anger = fear = disgust = joy = sadness = count = 0
        for tweet in tweets: 
            if(tweet['screen_name'] == user['twitter_handle']):
                text = tweet['text']
                time = tweet['created_at']
                diff = datetime.datetime.now() - time 
                
                for i in range(0,4):
                    while diff.days == i: 
                        emotions = {}
                        anger = disgust = fear = joy = sadness = count = 0
                        tone = tone_analyzer.tone({'text': text},'application/json').get_result()
                        anger = anger + tone['document_tone']['tone_categories'][0]['tones'][0]['score']
                        disgust = disgust + tone['document_tone']['tone_categories'][0]['tones'][1]['score']
                        fear = fear + tone['document_tone']['tone_categories'][0]['tones'][2]['score']
                        joy = joy + tone['document_tone']['tone_categories'][0]['tones'][3]['score']
                        sadness = sadness + tone['document_tone']['tone_categories'][0]['tones'][4]['score']
                        count = count + 1
                    emotions['anger'] = anger = anger / count 
                    emotions['disgust'] = disgust = disgust / count 
                    emotions['fear'] = fear = fear / count 
                    emotions['joy'] = joy = joy / count 
                    emotions['sadness'] = sadness = sadness / count
                    emotions['day'] = i
                try:
                    response = natural_language_understanding.analyze(text=text,features=Features(entities=EntitiesOptions(emotion=True,sentiment=True,limit=2),keywords=KeywordsOptions(emotion=True,sentiment=True,limit=5))).get_result()
                except: 
                    continue
                keywords = response['keywords']
                for keyword in keywords: 
                    db_keywords.append(keyword['text'])
                
        query = { 'screen_name' : user['twitter_handle']}
        update = { 'username' : user['username'] , 'screen_name' : user['twitter_handle'] , 'emotions' : emotions, 'keywords' : db_keywords }
        db.emotions.update(query, update, upsert=True)
            
                #print(text, json.dumps(response, indent=2))




