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
    if emotions:
        for emotion in emotions:
            try:
                if emotion['day']:
                    labels.append(str(datetime.datetime.now().date() - datetime.timedelta(int(emotion['day']))))
                    for mood, value in emotion.items():
                        if mood != 'day':
                           # print (value)
                            datasets[mood]['data'].append(value * 100)
            except:
                pass


    data = []
    for k, v in datasets.items():
        data.append(v)
    data.reverse()
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


def get_signup_form():
    with open (os.path.join(APP_UTILS, 'signup_form.json'), 'r') as f:
        return json.load(f)
