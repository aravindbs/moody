from flask_pymongo import PyMongo
from flask import Flask
from flask_login import LoginManager
import json
import yaml 
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
def load_config ():
    with open("config.json", "r") as f:
       # load_dotenv()
        #os.system('pwd')
        config = json.load(f)
        for key, value in config.items():
            for _key, _value in value.items():
                value[_key] = os.environ[_key]
               # print (value[_key])
        return config

config = load_config()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_UTILS = os.path.join(APP_ROOT, 'utils')

app = Flask(__name__)
app.config["MONGO_URI"] = config['mongodb']['MONGO_URI']
app.secret_key = config['flask']['SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
mongo = PyMongo(app)
#print ( config)
from app import views


