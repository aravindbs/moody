import json
from app import mongo, APP_UTILS
import os
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

