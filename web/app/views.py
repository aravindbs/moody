from app import app
from app import mongo
from flask import Flask, render_template,request, Response, url_for,flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.login import User
import os
from .utils import get_prefs, get_suggestions, get_mood_colors, get_emoji
from app.utils.spotify import spotify
from app.utils.tweet import get_tweets
from app.utils.youtube import youtube_search
from app.utils.nlu import nlu

GENRES = ['']

@app.route('/')
def index():
    if current_user.is_authenticated :
        return redirect (url_for('dashboard', user=current_user.username))
    
    return render_template('index.html', title = 'Moody | Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        print (login_data)
        user = mongo.db.users.find_one({'email' : login_data['email']})
        print (user)
        if user:
            if check_password_hash(user['password'], login_data['password']):
                user_obj = User(user)
                login_user (user_obj)
                flash('Login Successful')
                return redirect(url_for('dashboard', user= user['username']))
            else:
                flash("Incorrect Password")
                return redirect (url_for('login'))
        else:
            flash("Invalid Username. Try Again")
            return redirect (url_for('login'))
    return render_template ('login.html',  title = 'Moody | Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('login'))

@app.route('/signup', methods= ['GET','POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        pwd = form_data['password']
        hashed_pwd = generate_password_hash(pwd)
        form_data['password'] = hashed_pwd

        if mongo.db.users.find_one({ 'email' : form_data['email']}) or mongo.db.users.find_one({ 'username' : form_data['username']}):
            flash("Username Exists, Try Again")
            print ('here')
            return redirect ( url_for('signup'))
        else :
            mongo.db.users.insert_one(form_data)
            user = User (mongo.db.users.find_one({'username' : form_data['username']}) )
            login_user(user)
            return redirect (url_for('preferences', user=current_user.username))  
    return render_template('signup.html',  title = 'Moody | Sign Up')

@login_required
@app.route('/preferences', methods= ['GET','POST'])
def preferences(): 
    query = { 'username' : current_user.username }
    if request.method == 'POST':
        artists = request.form.getlist('artists')
        langs = request.form.getlist('langs')
        genres = request.form.getlist('genres')
        update = { 'username' : current_user.username, 'langs' : langs, 'artists' : artists, 'genres' : genres }
        mongo.db.preferences.update ( query, update, upsert =True)
        
        user = mongo.db.users.find_one({'username' : current_user.username})
        print(type(user))
        _user = [user]
        
        if get_tweets(_user) is not True or nlu(_user) is not True or spotify(_user) is not True or youtube_search(_user) is not True:  
            flash("Please try again.")
            return redirect (url_for('preferences', user=current_user.username)) 
        
        flash ('Preferences Updated')
        return redirect (url_for('dashboard', user=current_user.username))

    preferences = mongo.db.preferences.find_one(query)
    pref_list = get_prefs()
    langs_values =[]
    artists_values = []
    genres_values = []
    if preferences:
        try:
            genres_values = preferences['genres']
            langs_values = preferences['langs']
            artists_values = preferences['artists']
        except KeyError:
            pass
    return render_template('preferences.html',  title = 'Moody | Edit Prefs',pref_list = pref_list, genres_values = genres_values, langs_values =langs_values , artists_values = artists_values)

@login_required
@app.route('/dashboard/<user>')
def dashboard (user):
    profile = mongo.db.users.find_one({'email' : current_user.email })
    emotions = mongo.db.emotions.find_one({'username' : current_user.username})
    cur_emotion = {}
    if emotions:
        emotions = dict(emotions)
        emotions = emotions['emotions'] #list 
       
        for emotion in emotions: 
            for k,v in emotion.items():
                if k == 'day' and v == '0': 
                    cur_emotion = emotion
                    break 
    moods = cur_emotion
    moods.pop('day', None)

    if emotions:
        for k, v in moods.items():
            if type(v) is float:
                moods[k] = float (v) * 100     
    suggestions = get_suggestions(current_user.username)
    mood_color = get_mood_colors()
    emoji = get_emoji()
    return render_template('dashboard.html', title = 'Moody | {}'.format(profile['first_name']), user=user, profile = dict(profile), moods = moods, mood_color = mood_color, emoji = emoji ,suggestions=suggestions)




#######Prevents cacehing of static files in the browser#######
@app.context_processor
#@cross_origin(supports_credentials=True)
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
##############################################################
