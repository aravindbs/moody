import json
from app import mongo, APP_UTILS
import os
import datetime
from app import config

def get_chart_data (emotions, mood_color):

    datasets = {}
    for k, v in mood_color.items():
        datasets[k] = {'label' : k, 
                       'backgroundColor' : v, 
                       'data' : [],  
                       'fill' : False, 
                       'borderColor' : v }
    labels = []
    emotions =  [
        {
            "sadness": 0.419976,
            "disgust": 0.206897,
            "day": "3",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.058889
        },
        {
            "sadness": 0.419976,
            "disgust": 0.20689700000000003,
            "day": "1",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.05888899999999999
        },
        {
            "sadness": 0.419976,
            "disgust": 0.20689700000000003,
            "day": "5",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.05888899999999999
        },
        {
            "sadness": 0.419976,
            "disgust": 0.206897,
            "day": "4",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.058889
        },
        {
            "sadness": 0.41997600000000007,
            "disgust": 0.20689700000000005,
            "day": "6",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.05888899999999998
        },
        {
            "sadness": 0.41997599999999996,
            "disgust": 0.206897,
            "day": "0",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.058889
        },
        {
            "sadness": 0.41997600000000007,
            "disgust": 0.20689700000000005,
            "day": "2",
            "anger": 0.528375,
            "fear": 0.048348,
            "joy": 0.05888899999999998
        }
    ]
    for emotion in emotions:
        labels.append(str(datetime.datetime.now().date() - datetime.timedelta(int(emotion['day']))))
        for mood, value in emotion.items():
            if mood != 'day':
                datasets[mood]['data'].append(value * 100)

    data = []
    for k, v in datasets.items():
        data.append(v)
    
    payload = { 'labels' : labels, 'datasets': data }
    options = {}
    with open(os.path.join(APP_UTILS, 'chart_options.json'), 'r') as f:
        options = json.load (f)
     
    return { 'data' : payload, 'options' : options }
    


    
def get_prefs():
    with open(os.path.join(APP_UTILS, 'lists.json'), 'r') as f:
        pref_list = json.load (f)
        return pref_list

def get_suggestions (user):
    query = { 'username' : user }
    music = mongo.db.music_suggestions.find_one(query)
    video = mongo.db.video_suggestions.find_one(query)

    suggestions = { 'music' : [], 'video' : []}
    try:
        for url in music['suggestion']:
            suggestions['music'].append(url['url'])
        for url in video['suggestion']:
            link = url['url']
            link = link.replace("watch?v=", "embed/")
            suggestions['video'].append(link)
    except:
        pass
    return suggestions

def get_mood_colors ():
    with open (os.path.join(APP_UTILS, 'mood_to_color.json'), 'r') as f:
        return json.load(f)
    
def get_emoji ():
    with open (os.path.join(APP_UTILS, 'mood_to_emoji.json'), 'r') as f:
        return json.load(f)

