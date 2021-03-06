from app import app
from app import mongo
from app import config
from flask import Flask, render_template,request, Response, url_for,flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.login import User
import os
from .utils import get_prefs, get_suggestions, get_mood_colors, get_emoji,get_chart_data, get_signup_form
from app.utils.spotify import spotify
from app.utils.tweet import get_tweets,api
from app.utils.youtube import youtube_search
from app.utils.nlu import nlu
from .utils  import init_user

GENRES = ['']

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', user=current_user.username))
    return render_template('index.html',
                           title='Moody | Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_data = request.form.to_dict()
        print(login_data)
        user = mongo.db.users.find_one({'email': login_data['email']})
        print(user)
        if user:
            if check_password_hash(user['password'], login_data['password']):
                user_obj = User(user)
                login_user(user_obj)
                flash('Login Successful')
                return redirect(url_for('dashboard', user=user['username']))
            else:
                flash("Incorrect Password")
                return redirect(url_for('login'))
        else:
            flash("Invalid Username. Try Again")
            return redirect(url_for('login'))
    return render_template('login.html',
                           title='Moody | Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  
    if request.method == 'POST':
        form_data = request.form.to_dict()
        
        pwd = form_data['password']
        hashed_pwd = generate_password_hash(pwd)
    
        if form_data['repeat-password'] != form_data['password']:
            flash ('Passwords do not match')
            return redirect(url_for('signup'))
        form_data['password'] = hashed_pwd
        if mongo.db.users.find_one({ 'email' : form_data['email']}) or mongo.db.users.find_one({ 'username' : form_data['username']}):
            flash("Username Exists, Try Again")
            print ('here')
            return redirect ( url_for('signup'))
        else :
            mongo.db.users.update({ 'username' : form_data['username']},form_data, upsert= True)
            user = User (mongo.db.users.find_one({'username' : form_data['username']}) )
            login_user(user)
            return redirect (url_for('preferences', user=current_user.username))  

    args = request.args
    form = get_signup_form()
    form_data = {}
    title = 'Moody | Sign Up'
    if args:
        title = 'Moody | Edit Profile'
        user = args.get('user')
        form_data = mongo.db.users.find_one({'username' : user})    
        form_data.pop('password')
        print (form_data)
    return render_template('signup.html',  
                            title = title, 
                            form = form,
                            form_data = form_data
                            )

@login_required
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    
    query = {'username': current_user.username}
    if request.method == 'POST':
        artists = request.form.getlist('artists')
        langs = request.form.getlist('langs')
        genres = request.form.getlist('genres')
        twitter = request.form.get('twitter_handle')
        blogger = request.form.get('blogger_handle')
        update = { 'username' : current_user.username, 'langs' : langs, 'artists' : artists, 'genres' : genres }
       

        try : 
            api.get_user(twitter)
        
        except Exception as e:
            flash ('twiiter handle does not exist\n'+ str(e))
            return redirect(url_for('preferences'))
        mongo.db.preferences.update ( query, update, upsert =True)
        profile = mongo.db.users.find_one (query)
        profile['twitter_handle'] = twitter
        profile['blogger_handle'] = blogger
        mongo.db.users.update (query, profile, upsert = True)
        user = mongo.db.users.find_one({'username' : current_user.username})
        print(type(user))
        _user = [user]
        
    #    if get_tweets(_user) is not True or nlu(_user) is not True or spotify(_user) is not True or youtube_search(_user) is not True:  
        status = init_user(_user)
        if status is not True:
            flash("Please try again.\n" + str(status))
            return redirect (url_for('preferences', user=current_user.username)) 
        
        flash ('Preferences Updated')
        return redirect (url_for('dashboard', user=current_user.username))

    profile = mongo.db.users.find_one(query)
    preferences = mongo.db.preferences.find_one(query)
    pref_list = get_prefs()
    langs_values = []
    artists_values = []
    genres_values = []
    form_data = { 'twitter_handle' : '', 'blogger_handle' : ''}
    try:
        form_data ['twitter_handle'] = profile['twitter_handle']
        form_data ['blogger_handle'] = profile['blogger_handle']
    
    except Exception as e:
        print(str(e))
        pass
    if preferences:
        try:
            genres_values = preferences['genres']
            langs_values = preferences['langs']
            artists_values = preferences['artists']
        except KeyError:
            pass
    return render_template('preferences.html',  
                            title = 'Moody | Edit Prefs',
                            pref_list = pref_list, 
                            genres_values = genres_values, 
                            langs_values =langs_values ,
                            artists_values = artists_values,
                            form_data = form_data)
@login_required
@app.route('/dashboard/<user>')
def dashboard(user):
    profile = mongo.db.users.find_one({'email': current_user.email})
    emotions = mongo.db.emotions.find_one({'username': current_user.username})
    cur_emotion = {}
    if emotions:
        emotions = dict(emotions)
        emotions = emotions['emotions']  # list
        for emotion in emotions:
            for k, v in emotion.items():
                if k == 'day' and v == '0':
                    cur_emotion = emotion
                    break
    suggestions = get_suggestions(current_user.username)    
    emoji = get_emoji()
    mood_color = get_mood_colors()
    payload = get_chart_data(emotions,mood_color)
    moods = cur_emotion
    payload = get_chart_data(emotions,mood_color)
    if emotions:
        for k, v in moods.items():
            if type(v) is float:
                moods[k] = float(v) * 100 
    moods.pop('day', None)
    return render_template('dashboard.html', 
                            title = 'Moody | {}'.format(profile['first_name']), 
                            payload= payload, 
                            user=user, 
                            profile = dict(profile), 
                            moods = moods, 
                            mood_color = mood_color, 
                            emoji = emoji ,
                            suggestions=suggestions,
                            data = payload['data'],
                            options = payload['options'])




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
