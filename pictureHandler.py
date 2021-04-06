
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.api import users
from myuser import MyUser


import mimetypes
import logging

class PictureHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        action= self.request.get('action')
        if action == 'UPLOAD COVER':

           upload_files = self.request.POST.get("cover", None)

           if upload_files == None:
                self.redirect('/ProfilePage')
           else:
               wordInfo = MyUser(id=user.user_id(), username=myuser.username, userbio=myuser.userbio,
                                 location=myuser.location, userBirthDate=myuser.userBirthDate,
                                 file_name=myuser.file_name)

               wordInfo.coverPhoto = upload_files.filename
               wordInfo.blob = upload_files.file.read()
               wordInfo.put()

               self.redirect('/ProfilePage')

        if action == 'UPLOAD PROFILE PICTURE':
                upload_files = self.request.POST.get("file", None)

                if upload_files == None:
                    self.redirect('/ProfilePage')
                else:
                    wordInfo = MyUser(id=user.user_id(), username=myuser.username, userbio=myuser.userbio,
                                      location=myuser.location, userBirthDate=myuser.userBirthDate, coverPhoto=myuser.coverPhoto)


                    wordInfo.file_name=upload_files.filename
                    wordInfo.blob = upload_files.file.read()
                    wordInfo.put()

                    self.redirect('/ProfilePage')