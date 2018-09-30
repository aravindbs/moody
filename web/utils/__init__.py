from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from app import config

CONSUMER_KEY = config['tweepy']['CONSUMER_KEY']
CONSUMER_SECRET = config['tweepy']['CONSUMER_SECRET']

ACCESS_TOKEN = config['tweepy']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = config['tweepy']['ACCESS_TOKEN_SECRET']
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = API(auth)