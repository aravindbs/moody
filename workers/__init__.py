import pymongo
import yaml

with open("../config.yml", "r") as f:
    config = yaml.load(f)

myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody