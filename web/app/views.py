from app import app
from app import mongo
from flask import Flask, render_template,request, Response, url_for,flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.login import User
import os
from utils import get_prefs

GENRES = ['']

@app.route('/')
def index():
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
    moods = mongo.db.emotions.find_one({'screen_name' : dict(profile)['twitter_handle']})
    if moods:
        for k, v in dict(moods).items():
            if type(v) is float:
                moods[k] = float (v) * 100     
    tracks = [ 'https://open.spotify.com/embed/track/73TXMz1i41sGfOuDg8gH4L', 'https://open.spotify.com/embed/track/6ZANrVuAMp2rpjhfbOuJly', 'https://open.spotify.com/embed/track/73TXMz1i41sGfOuDg8gH4L', 'https://open.spotify.com/embed/track/73TXMz1i41sGfOuDg8gH4L']
    return render_template('dashboard.html', title = 'Moody | {}'.format(profile['first_name']), user=user, profile = dict(profile), moods = moods, tracks = tracks)



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
