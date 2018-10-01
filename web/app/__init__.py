from flask_pymongo import PyMongo
from flask import Flask
from flask_login import LoginManager
import json
import yaml 

def load_config ():
    with open ('../config.yml') as f:
        config = yaml.load(f)
        return config

config = load_config()

app = Flask(__name__)
app.config["MONGO_URI"] = config['mongodb']['MONGO_URI']
app.secret_key = config['flask']['SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
mongo = PyMongo(app)
#print ( config)
from app import views


