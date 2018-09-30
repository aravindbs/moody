from tweepy import OAuthHandler
from tweepy import API
import requests 
import json, yaml, datetime, time 
import pymongo

with open("../config.yml", "r") as f:
    config = yaml.load(f)

SLEEP_TIME = 2

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody

with open("../config.yml", "r") as f:
    config = yaml.load(f)

def calculate_age(tweet):
    now = datetime.datetime.now()
    return ( now.hour - tweet.hour )*60 + (now.minute - tweet.minute)
    
auth = OAuthHandler(config['twitter']['CONSUMER_KEY'], config['twitter']['CONSUMER_SECRET'])
auth.set_access_token(config['twitter']['ACCESS_TOKEN'], config['twitter']['ACCESS_TOKEN_SECRET'])

api = API(auth, wait_on_rate_limit = True)


print("Getting Tweets...")
users = list(db.users.find({}))

#print(most_recent)
for i in range(2):
    most_recent = list(db.most_recent_tweet.find({})) 
    for user in users: 
        screen_name = user['twitter_handle']
        print(screen_name)
        if len(most_recent) == 0: 
            print("none")
            result = list(api.user_timeline(screen_name=screen_name, count=10))
        else: 
            since_id = db.most_recent_tweet.find_one({'screen_name' : screen_name})
            print(since_id)
            if len(since_id) == 0:
                result = list(api.user_timeline(screen_name=screen_name, count=10)) 
            else:
                result = list(api.user_timeline(screen_name=screen_name, count=10, since_id=since_id['id']))

        if result: 
            query = { 'screen_name' : screen_name}
            update = { 'screen_name' : screen_name, 'id' : result[0].id}
            db.most_recent_tweet.update(query, update, upsert=True)
        
        tweets = {}
        for r in result: 
            tweets['screen_name'] = screen_name
            tweets['tweet_id'] = r.id
            tweets['created_at'] = r.created_at 
            tweets['text'] = r.text
            tweets.pop('_id', None)
            db.tweets.insert_one(tweets).inserted_id

        #time.sleep(SLEEP_TIME) 

    

        
