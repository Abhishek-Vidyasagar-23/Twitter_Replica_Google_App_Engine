import webapp2
from google.appengine.ext import ndb
from google.appengine.api import images
import mimetypes
import logging

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    userbio= ndb.StringProperty()
    userBirthDate=ndb.StringProperty()
    location=ndb.StringProperty()
    userFollowers=ndb.StringProperty(repeated=True)
    userFollowing=ndb.StringProperty(repeated=True)
    file_name = ndb.StringProperty()
    coverPhoto=ndb.StringProperty()
    blob = ndb.BlobProperty()