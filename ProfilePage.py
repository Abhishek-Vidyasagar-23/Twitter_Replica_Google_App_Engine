
import webapp2
import jinja2
from myuser import MyUser
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from pictureHandler import PictureHandler

from google.appengine.api import images
import mimetypes
import logging

from TwitterTweets import TwitterTweets
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        userNameLength = ""
        statues=""
        userinfo=""
        response=False
        userKey=""
        followersresponse=False
        userQueryunfollow=''
        following=[]
        follower=[]
        statues = "Follow"
        userUnFollow=[]
        userFollowers=[]
        u=''
        val=0
        updateResponse=0



        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()

        if my_user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.response.write(template.render(template_values))
        else:
             username= self.request.get('username')
             userFollowing = self.request.get('userFollowing')
             userUnfollowing=self.request.get('unfollowing')
             deleteTweet=self.request.get('deleteTweet')
             query = MyUser.query(MyUser.username == my_user.username).get()

             if len(username) > 0:
                userQuery = MyUser.query(MyUser.username == username).fetch()
                userNameLength = username
                for i in userQuery:
                    userinfo = i

             if len(userFollowing) > 0:
                userQueryfollow = MyUser.query(MyUser.username == userFollowing).fetch()
                userNameLength = userFollowing
                for i in userQueryfollow:
                    userinfo = i

             if len(userUnfollowing) > 0:
                 userQueryunfollow = MyUser.query(MyUser.username == my_user.username).fetch()
                 userNameLength =  userQueryunfollow

             if len(userNameLength) == 0 or username == my_user.username:

                myuser_key = ndb.Key('tweets', my_user.username)
                userProfile = myuser_key.get()


                if userProfile is not None:

                     val=range(len(userProfile.userTweets))

                elif userProfile is None:
                    val=0

                template_values = {
                    'logout_url': users.create_logout_url(self.request.uri),
                    'user': query,
                    'userHeader': query,
                    'userTitle': query.username,  #
                    'test': 0,
                    'following': len(query.userFollowing),
                    'follower': len(query.userFollowers),
                    'followStatues': 'Edit Profile',
                    'unfollowstatues': '',
                    'range': val,
                    'userTweets': userProfile,
                    'option': 'block',
                    'upload_url': format(blobstore.create_upload_url('/upload')),
                    'img': query.file_name,
                    'imgCover': query.coverPhoto

                }
                template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
                self.response.write(template.render(template_values))
             else:
                 if len(username) > 0:
                     for i in  query.userFollowing:

                         if i == username:
                             statues="Following"
                             break;
                     myuser_key = ndb.Key('TwitterTweets', username)
                     userProfile = myuser_key.get()
                     template_values = {
                         'logout_url': users.create_logout_url(self.request.uri),
                         'user': userinfo,
                         'userHeader': query,
                         'userTitle':username,
                         'test': len(username),
                         'following': len(query.userFollowing),
                         'follower': len(query.userFollowers),
                         'followStatues':statues,
                         'range': range(len(userProfile.userTweets)),
                         'unfollowstatues':'Unfollow ',
                         'userTweets': userProfile,
                         'option': 'none',
                         'img': query.file_name,
                         'imgCover': query.coverPhoto

                     }
                     template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
                     self.response.write(template.render(template_values))

                 if len(userFollowing) > 0:
                     if userFollowing:
                        query = MyUser.query(MyUser.username == my_user.username).get()
                        userretrieve=MyUser.query(MyUser.username == userFollowing).fetch()
                        myuser_key = ndb.Key('TwitterTweets', userFollowing)
                        userProfile = myuser_key.get()

                        if userProfile is not None:
                            updateResponse = range(len(userProfile.userTweets))

                        for i in userretrieve:
                            userKey=i

                        if len(query.userFollowing) == 0:

                            wordInfo = MyUser(id=user.user_id(), username=query.username, userbio=query.userbio,
                                              location=query.location, userBirthDate=query.userBirthDate, coverPhoto=query.coverPhoto, file_name=query.file_name)
                            wordInfo.userFollowing.append(userFollowing.capitalize())
                            wordInfo.put()

                            userKey.userFollowers.append(query.username)
                            userKey.put()
                        else:
                            for i in query.userFollowing:
                                if i == userFollowing:
                                    response = True
                                    break
                            for j in userKey.userFollowers:
                              if j == query.username:
                                 followersresponse=True
                                 break

                            if response == False:
                                query.userFollowing.append(userFollowing.capitalize())
                                query.put()

                            if followersresponse == False:
                                userKey.userFollowers.append(query.username)
                                userKey.put()


                        template_values = {
                            'logout_url': users.create_logout_url(self.request.uri),
                            'user': userinfo,
                            'userHeader': query,
                            'userTitle': userFollowing,
                            'following': len(query.userFollowing),
                            'follower': len(query.userFollowers),
                            'test': len(userFollowing),
                            'followStatues': 'Following',
                            'range': updateResponse,
                            'unfollowstatues': 'Unfollow ',
                            'userTweets': userProfile,
                            'option': 'none',
                            'img': query.file_name,
                            'imgCover': query.coverPhoto

                        }
                        template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
                        self.response.write(template.render(template_values))

                 if len(userUnfollowing) > 0:
                     userUnfollowRetrieve = MyUser.query(MyUser.username == my_user.username).fetch()
                     retrieveUnfollowUserInfo = MyUser.query(MyUser.username == userUnfollowing).get()
                     myuser_key = ndb.Key('TwitterTweets', userUnfollowing)
                     userProfile = myuser_key.get()

                     if userProfile is not None:
                         updateResponse = range(len(userProfile.userTweets))

                     for i in userUnfollowRetrieve:
                         userUnFollow = i.userFollowing

                     userFollowers=retrieveUnfollowUserInfo.userFollowers
                     userUnFollow.remove(userUnfollowing)
                     userFollowers.remove(my_user.username)
                     wordInfo = MyUser(id=user.user_id(), username=my_user.username, userbio=my_user.userbio,
                                       location=my_user.location, userBirthDate=my_user.userBirthDate, userFollowing=userUnFollow, userFollowers=my_user.userFollowers, coverPhoto=my_user.coverPhoto, file_name=my_user.file_name)
                     wordInfo.put()

                     friendInfo = MyUser(id=retrieveUnfollowUserInfo.key.id(), username=retrieveUnfollowUserInfo.username, userbio=retrieveUnfollowUserInfo.userbio,
                                         location=retrieveUnfollowUserInfo.location, userBirthDate=retrieveUnfollowUserInfo.userBirthDate,
                                         userFollowing=retrieveUnfollowUserInfo.userFollowing, userFollowers=userFollowers, coverPhoto=retrieveUnfollowUserInfo.coverPhoto, file_name=retrieveUnfollowUserInfo.file_name)
                     friendInfo.put()


                     query = MyUser.query(MyUser.username == userUnfollowing).fetch()
                     for i in query:
                         following = i.userFollowing
                         follower = i.userFollowers
                         userinfo=i
                     template_values = {
                         'logout_url': users.create_logout_url(self.request.uri),
                         'user': userinfo,
                         'userHeader': my_user,
                         'userTitle': userUnfollowing,
                         'following': len(following),
                         'follower': len(follower),
                         'test': len(userUnfollowing),
                         'followStatues': 'Follow',
                         'range': updateResponse,
                         'unfollowstatues':'',
                         'userTweets': userProfile,
                         'option': 'none'

                     }
                     template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
                     self.response.write(template.render(template_values))


    def post(self):

        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()
        updateResponse = 0

        query = MyUser.query(MyUser.username == my_user.username).get()
        if action == 'UPDATE':
            myuser_key = ndb.Key('TwitterTweets', my_user.username)
            userProfile = myuser_key.get()

            if userProfile is not None:
                updateResponse=range(len(userProfile.userTweets))
            userName = self.request.get('username')
            userLocation = self.request.get('location')
            userBirthday = self.request.get('birthday')
            userBio = self.request.get('bio')

            userInfo = MyUser(id=user.user_id(), username=userName.capitalize(), userbio=userBio.capitalize(),
                              userBirthDate=userBirthday, location=userLocation.capitalize(), coverPhoto=query.coverPhoto, file_name=query.file_name)
            userInfo.put()

            template_values = {
                'response': "Edit Successful",
                'logout_url': users.create_logout_url(self.request.uri),
                'userHeader': query,
                'userTitle': userName,
                'user': query,
                'following': len(query.userFollowing),
                'follower': len(query.userFollowers),
                'followStatues': 'Edit Profile',
                'range': updateResponse,
                'test': 0,
                'userTweets': userProfile,
                'bio': query.userbio,
                'img': query.file_name,
                'imgCover': query.coverPhoto

            }
            template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
            self.response.write(template.render(template_values))

        if action=='Edit':
            tweetNumber = self.request.get('hidden')
            val=int(tweetNumber)
            queryTweet = TwitterTweets.query(TwitterTweets.username == my_user.username).get()
            template_values = {
                'response': "Edit Successful",
                'logout_url': users.create_logout_url(self.request.uri),
                'userHeader': query,
                'userTitle': query.username,
                'user': query,
                'following': len(query.userFollowing),
                'follower': len(query.userFollowers),
                'followStatues': 'Edit Profile',
                'range': range(len(queryTweet.userTweets)),
                'test': 0,
                'userTweets': queryTweet,
                'tweetEdit':queryTweet.userTweets[val],
                'bio': query.userbio,
                'showEditTweet':'block',
                'tweetnumber':tweetNumber,
                'img': query.file_name,
                'imgCover': query.coverPhoto
            }
            template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
            self.response.write(template.render(template_values))
        if action =='Update Tweet':
            temp = []
            tweetNumber = self.request.get('tweetnumber')
            val=int(tweetNumber)
            editedTweet=self.request.get('tweetEdit')

            queryTweet = TwitterTweets.query(TwitterTweets.username == my_user.username).get()
            temp=queryTweet.userTweets
            temp[val]=editedTweet
            usertweet = TwitterTweets(id=my_user.username, userTweets=temp, username=my_user.username)
            usertweet.put()
            template_values = {
                'response': "Edit Successful",
                'logout_url': users.create_logout_url(self.request.uri),
                'userHeader': query,
                'userTitle':query.username ,
                'user': query,
                'following': len(query.userFollowing),
                'follower': len(query.userFollowers),
                'followStatues': 'Edit Profile',
                'range': range(len(queryTweet.userTweets)),
                'test': 0,
                'userTweets': queryTweet,
                'tweetEdit': queryTweet.userTweets[val],
                'bio': query.userbio,
                'showEditTweet': 'none',
                'tweetnumber': tweetNumber,
                'img': query.file_name,
                'imgCover': query.coverPhoto
            }
            template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
            self.response.write(template.render(template_values))
        if action =='Delete':
            temp = []
            tweetNumber = self.request.get('deleteTweet')
            val = int(tweetNumber)
            queryTweet = TwitterTweets.query(TwitterTweets.username == my_user.username).get()
            temp = queryTweet.userTweets
            temptweet = temp[val]

            temp.remove(temptweet)
            if not temp:
                self.redirect('/ProfilePage')
            else:
                usertweet = TwitterTweets(id=my_user.username, userTweets=temp, username=my_user.username)
                usertweet.put()
                template_values = {
                    'response': "Edit Successful",
                    'logout_url': users.create_logout_url(self.request.uri),
                    'userHeader': query,
                    'userTitle': query.username,
                    'user': query,
                    'following': len(query.userFollowing),
                    'follower': len(query.userFollowers),
                    'followStatues': 'Edit Profile',
                    'range': range(len(queryTweet.userTweets)),
                    'test': 0,
                    'userTweets': queryTweet,
                    'tweetEdit': queryTweet.userTweets[val],
                    'bio': query.userbio,
                    'showEditTweet': 'none',
                    'tweetnumber': tweetNumber,
                    'img': query.file_name,
                    'imgCover': query.coverPhoto
                }
                template = JINJA_ENVIRONMENT.get_template('ProfilePage.html')
                self.response.write(template.render(template_values))


