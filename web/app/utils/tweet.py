from tweepy import OAuthHandler
from tweepy import API
import requests 
import json, yaml, datetime, time 
import pymongo

from collections import defaultdict

from app.utils import config

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody



def calculate_age(tweet):
    now = datetime.datetime.now()
    return ( now.hour - tweet.hour )*60 + (now.minute - tweet.minute)
    
auth = OAuthHandler(config['twitter']['CONSUMER_KEY'], config['twitter']['CONSUMER_SECRET'])
auth.set_access_token(config['twitter']['ACCESS_TOKEN'], config['twitter']['ACCESS_TOKEN_SECRET'])

api = API(auth, wait_on_rate_limit = True)


def get_tweets(user):
    print("hi")
    most_recent = list(db.most_recent_tweet.find({})) 
    #for user in users: 
    try: 
        screen_name = user[0]['twitter_handle']
        print(screen_name)
        if most_recent and len(most_recent) == 0: 
            print("none")
            result = list(api.user_timeline(screen_name=screen_name, count=10))
        else: 
            since_id = db.most_recent_tweet.find_one({'screen_name' : screen_name})
            #print(since_id)
            if since_id is None:
                result = list(api.user_timeline(screen_name=screen_name, count=30)) 
            else:
                result = list(api.user_timeline(screen_name=screen_name, count=30, since_id=since_id['id']))

        if result: 
            query = { 'screen_name' : screen_name}
            update = { 'screen_name' : screen_name, 'id' : result[0].id }
            db.most_recent_tweet.update(query, update, upsert=True)
        
            all_tweets = []
            tweets = {}
            db_tweets = defaultdict(list)
            for r in result: 
                print("yes")
                tweets = {}
                tweets['screen_name'] = screen_name
                tweets['tweet_id'] = r.id
                tweets['created_at'] = r.created_at 
                tweets['text'] = r.text
                diff = datetime.datetime.now() - r.created_at
                
                (db_tweets[str(diff.days)]).append(tweets)

            print(db_tweets)
            query = { 'username' : user[0]['username'] }
            update = { 'username' : user[0]['username'] , 'tweets' : dict(db_tweets) }
            db.tweets.update(query, update, upsert=True)

    except Exception as e: 
        return e 


    return True  

    

        

