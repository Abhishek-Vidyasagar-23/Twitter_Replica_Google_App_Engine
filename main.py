
import webapp2
import jinja2
from myuser import MyUser
from google.appengine.api import users
from google.appengine.ext import ndb
from ProfilePage import ProfilePage
from pictureHandler import PictureHandler
from TwitterTweets import TwitterTweets
import datetime


import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)




class MainPage(webapp2.RequestHandler):

    def get(self):

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser_temp = myuser_key.get()

        query = TwitterTweets.query().fetch()

        if myuser_temp == None:

            template_values = {
                'login_url': users.create_login_url(self.request.uri)
            }
            template = JINJA_ENVIRONMENT.get_template('loginpage.html')
            self.response.write(template.render(template_values))
        else:
            template_values = {
                'logout_url' : users.create_logout_url(self.request.uri),
                'user':myuser_temp,
                'userHeader': myuser_temp,
                'query':query,
                'img': myuser_temp.file_name

            }
            template = JINJA_ENVIRONMENT.get_template('mainpage.html')
            self.response.write(template.render(template_values))


    def post(self):
        statues='follow'
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        my_user = myuser_key.get()



        if action == 'SUBMIT':
             username=self.request.get('username')
             location = self.request.get('location')
             birthday = self.request.get('birthday')
             bio = self.request.get('bio')


             #self.response.write(myuser_temp)
             if username=='' or location==''or birthday=='':
                 template_values = {
                     'errorMessage':"Input Field is Empty"
                 }
                 template = JINJA_ENVIRONMENT.get_template('loginpage.html')
                 self.response.write(template.render(template_values))

             elif username!='' or location!=''or birthday!='' :


                 query=MyUser.query(MyUser.username == username).fetch()

                 if len(query)==0:

                     my_user = MyUser(id=user.user_id(), username=username.capitalize(), location=location.capitalize(),
                                          userBirthDate=birthday, userbio=bio.capitalize())
                     my_user.put()
                     template_values = {
                         'user': username,
                         'userHeader': my_user,
                         'logout_url': users.create_logout_url(self.request.uri)
                     }
                     template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                     self.response.write(template.render(template_values))
                 else:

                     template_values = {
                         'login_url': users.create_login_url(self.request.uri),
                         'errorMessage': "Username Already Exist."
                     }
                     template = JINJA_ENVIRONMENT.get_template('loginpage.html')
                     self.response.write(template.render(template_values))

        if action == 'Tweet':

            userTweet = self.request.get('tweet')
            if userTweet == '':
               self.redirect('/')
            else:
                myuser_key = ndb.Key('TwitterTweets',my_user.username )
                myuser = myuser_key.get()

                if myuser == None:
                    self.response.write('new ')
                    wordInfo = TwitterTweets(id=my_user.username.capitalize(), username=my_user.username.capitalize(), timestamp=datetime.datetime.now())
                    wordInfo.userTweets.append(userTweet.lower())
                    wordInfo.put()
                    self.redirect('/')
                else:
                    myuser.userTweets.append(userTweet.lower())
                    myuser.put()
                    self.redirect('/')



        if action =='Search':
            list=[]
            response=[]
            search = self.request.get('search')

            if search == '':
                self.redirect('/')
            else:
                queryUser = MyUser.query(MyUser.username == search.capitalize()).get()
                queryTweet = TwitterTweets.query().fetch()
                if queryUser is not None or len(queryTweet) > 0:


                    for i in queryTweet:
                        for k in i.userTweets:
                            list.append(k)
                    for i in range(len(list)):
                        s1 = list[i].split(" ")
                        for x in s1:
                            if (x in search.lower()):
                                response.append(list[i])
                                break;


                    myuser_key = ndb.Key('MyUser', user.user_id())
                    myuserfollowing = myuser_key.get()

                    for i in myuserfollowing.userFollowing:

                        if i == queryUser.username:
                            statues = "Following"
                            break;

                    template_values = {
                        'user': my_user.username,
                        'userHeader': my_user,
                        'logout_url': users.create_logout_url(self.request.uri),
                        'queryUser': queryUser,
                        'followStatues':statues,
                        'queryTweet': response

                    }
                    template = JINJA_ENVIRONMENT.get_template('search.html')
                    self.response.write(template.render(template_values))

                elif len(queryUser)== 0 :


                    template_values = {
                        'user': my_user.username,
                        'userHeader': my_user,
                        'logout_url': users.create_logout_url(self.request.uri),
                        'queryError':'User Not Found'
                    }
                    template = JINJA_ENVIRONMENT.get_template('search.html')
                    self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([
    ('/' , MainPage),('/ProfilePage', ProfilePage),('/upload', PictureHandler),
    ], debug=True)