from google.appengine.ext import ndb


class TwitterTweets(ndb.Model):
    username = ndb.StringProperty()
    userTweets= ndb.StringProperty(repeated=True)
    
    timestamp = ndb.DateTimeProperty(auto_now=True)
