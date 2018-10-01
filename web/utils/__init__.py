import json
def get_prefs():
    with open('utils/lists.json', 'r') as f:
        pref_list = json.load (f)
        return pref_list