import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, EmotionOptions
from watson_developer_cloud import ToneAnalyzerV3
import pymongo
import datetime

from app.utils import config

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody


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

def nlu(user): 
    print ( 'nlu ' + user[0]['username'])
    #print (list(users) )
    today = datetime.datetime.now()
    #tweets = list(db.tweets.find({}))
    
    #for user in users:
    db_keywords = []
    emotions = {}
    all_emotions = []
    print(user[0]['username'])
    anger = fear = disgust = joy = sadness = count = 0
    tweets = db.tweets.find_one({'username' : user[0]['username']})
    #print(tweets)
    try:
        #print(tweets)
        tweets.pop('_id', None)
        tweets = tweets['tweets']
        #print(type(tweets))
        
        for key in tweets: 
            if int(key) < 30: 
                values = tweets[key]
                #print(values)
                anger = disgust = fear = joy = sadness = count = 0
                for tweet in values: 
                    text = tweet['text']
                    #time = tweet['created_at']
                    tone = tone_analyzer.tone({'text': text},'application/json').get_result()
                    if tone is None:
                        continue 
                    anger = anger + tone['document_tone']['tone_categories'][0]['tones'][0]['score']
                    disgust = disgust + tone['document_tone']['tone_categories'][0]['tones'][1]['score']
                    fear = fear + tone['document_tone']['tone_categories'][0]['tones'][2]['score']
                    joy = joy + tone['document_tone']['tone_categories'][0]['tones'][3]['score']
                    sadness = sadness + tone['document_tone']['tone_categories'][0]['tones'][4]['score']
                    count = count + 1
                try:
                    response = natural_language_understanding.analyze(text=text,features=Features(entities=EntitiesOptions(emotion=True,sentiment=True,limit=2),keywords=KeywordsOptions(emotion=True,sentiment=True,limit=5))).get_result()
                except: 
                    continue
                keywords = response['keywords']
                for keyword in keywords: 
                    db_keywords.append(keyword['text'])
                emotions = {}
                emotions['anger'] = anger / count 
                emotions['disgust'] = disgust / count 
                emotions['fear'] = fear / count 
                emotions['joy'] = joy / count 
                emotions['sadness'] = sadness / count
                emotions['day'] = key
                #print(emotions['day'])
                all_emotions.append(emotions)
                    
                print(all_emotions)
    except Exception as e:
        return e
        pass        
    query = { 'screen_name' : user[0]['twitter_handle']}
    update = { 'username' : user[0]['username'] , 'screen_name' : user[0]['twitter_handle'] , 'emotions' : all_emotions, 'keywords' : db_keywords }
    db.emotions.update(query, update, upsert=True)

    return True 
