from app import login_manager,mongo
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self,user):
        self.id = user['username']
        self.username = user['username']
        self.email = user['email']
        self.password = user['password']
        #self.logged_in = False

@login_manager.user_loader
def load_user(user_id):
    user = User (mongo.db.users.find_one({ 'username' : user_id}))
    return user