from oauth2client import client
from googleapiclient import sample_tools
import sys
import pymongo

def auth(argv):
    service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')

#def blogs(): 
    try:
        users = service.users()    #googleapiclient.discovery.Resource object
        blogs = service.blogs()   #googleapiclient.discovery.Resource object

    # Retrieve the list of Blogs this user has write privileges on
        thisusersblogs = blogs.listByUser(userId='self').execute()  #retrieves all blogs from the user (you = self) 
        posts = service.posts()    #googleapiclient.discovery.Resource object for posts

    # List the posts for each blog this user has
        for blog in thisusersblogs['items']:
            print('The posts for %s:' % blog['name'])  
            request = posts.list(blogId=blog['id'])   
             #uses #googleapiclient.discovery.Resource object for posts to get blog by id
        while request != None:
            posts_doc = request.execute()
            if 'items' in posts_doc and not (posts_doc['items'] is None):
                for post in posts_doc['items']:
                    print(post['published'])
                    print(post['content'])
                    print('  %s (%s)' % (post['title'], post['url']))
            request = posts.list_next(request, posts_doc)

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run'
            'the application to re-authorize')

if __name__ == '__main__':
    auth(sys.argv)
    #blogs()
