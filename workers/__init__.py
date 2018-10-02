import pymongo
import json
import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
load_dotenv(dotenv_path='.env')
with open("config.json", "r") as f:
    config = json.load(f)
    #load_dotenv()
    for key, value in config.items():
        for _key, _value in value.items():
            value[_key] = os.environ[_key]

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody
