import json
from app import mongo
import re 

def get_prefs():
    with open('utils/lists.json', 'r') as f:
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
    except KeyError:
        pass
    return suggestions


