from oauth2client import client
from googleapiclient import sample_tools
import sys
import pymongo, json
from __init__ import config, db 
from datetime import datetime, timedelta


myclient = pymongo.MongoClient(config['mongodb']['MONGO_URI'])
db = myclient.testmoody

def auth(argv):
    service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')

#def blogs(): 
    try:
        username = 'gagan'
        most_recent = db.most_recent_blog.find_one({'username' : username})
        print (most_recent)
        users = service.users()    #googleapiclient.discovery.Resource object
        blogs = service.blogs()   #googleapiclient.discovery.Resource object

    # Retrieve the list of Blogs this user has write privileges on
        thisusersblogs = blogs.listByUser(userId='self').execute()  #retrieves all blogs from the user (you = self) 
        posts = service.posts()    #googleapiclient.discovery.Resource object for posts

    # List the posts for each blog this user has
        for blog in thisusersblogs['items']:
            print('The posts for %s:' % blog['name'])  
            if most_recent is not None: 
                print("hey")
                request = posts.list(blogId=blog['id'], startDate=most_recent['date']) 
            else: 
                print("hi")
                request = posts.list(blogId=blog['id'])
            

            #uses #googleapiclient.discovery.Resource object for posts to get blog by id
        if request != None:
            posts_doc = request.execute()
            query = { 'username' : username }
            update = { 'username' : username , 'date' : posts_doc['items'][0]['published'] }
            db.most_recent_blog.update(query, update, upsert=True) 
            
            content = db.blogs.find_one({'username' : username })['content']
            if 'items' in posts_doc and not (posts_doc['items'] is None):
                for post in posts_doc['items']:
                    if most_recent and post['published'] == most_recent['date']:
                        continue 
                    #print(post['content'])
                    print('  %s (%s)' % (post['title'], post['url']))
                    content.append(post['content'])
            
                query = { 'username' : username }
                update = { 'username' : username ,  'content' : content }
                db.blogs.update(query, update, upsert=True)

            #request = posts.list_next(request, posts_doc)

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run'
            'the application to re-authorize')

if __name__ == '__main__':
    auth(sys.argv)
    #blogs()
