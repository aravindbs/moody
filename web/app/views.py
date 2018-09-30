from app import app
from app import mongo
from flask import Flask, render_template,request, Response, url_for,flash, redirect
from flask_login import login_user, login_required,current_user, logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from app.login import User
import os


@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template ('login.html')

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

        print (json.dumps (form_data, indent=3))
    return render_template('signup.html')

@app.route('/preferences', methods= ['GET','POST'])
def preferences(): 
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print (form_data)
        
        return redirect (url_for('dashboard', user=current_user.username))
    else : 
        return render_template('preferences.html')



@login_required
@app.route('/dashboard/<user>')
def dashboard (user):
    profile = mongo.db.users.find_one({'email' : current_user.email })
    moods = dict(mongo.db.emotions.find_one({'screen_name' : dict(profile)['twitter_handle']}))
    for k, v in moods.items():
        if type(v) is float:
            moods[k] = float (v) * 100     
    return render_template('dashboard.html', user=user, profile = dict(profile), moods = moods)



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
