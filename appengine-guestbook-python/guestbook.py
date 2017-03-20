#!/usr/bin/env python

# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START imports]
import os
import urllib
import binascii
from google.appengine.ext import ndb

import jinja2
import webapp2
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'hogehoge'
}

# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    sessionID = ndb.StringProperty()
    userID = ndb.StringProperty()
    password = ndb.StringProperty()


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START basehandler]
class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()
# [END basehandler]


# [START main_page]
class MainPage(BaseHandler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        author_id = self.request.get('author_id')
        sessionID = self.session.get('sessionID')
        if sessionID == '':
            new_sessionID = binascii.hexlify(os.urandom(8))
            author = Author(sessionID=new_sessionID,
                            userID='GUEST',
                            password='')
            ndb.transaction_async(author.put())
            self.session['sessionID'] = new_sessionID

        if not guestbook_name:
            guestbook_name = DEFAULT_GUESTBOOK_NAME

        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch_async(10)

        if author_id != '':
            author = Author.get_by_id(long(author_id))
            if author is not None:
                if author.sessionID == sessionID:
                    url = '/api/user/logout/' + author_id
                    url_linktext = 'Logout'
                else:
                    url = '/user/loginpage'
                    url_linktext = 'Login'

        else:
            author = Author.query(Author.userID == 'GUEST').get()
            if author is None:
                author = Author(sessionID=binascii.hexlify(os.urandom(8)),
                                userID='GUEST',
                                password='')
                ndb.transaction_async(author.put())

            url = '/user/loginpage'
            url_linktext = 'Login'

        template_values = {
            'author': author,
            'greetings': greetings.get_result(),
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
# [END main_page]


# [START login_page]
class LoginPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render())
# [END login_page]


# [START Register_page]
class RegisterPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render())
# [END Register_page]


# [START guestbook]
class Guestbook(BaseHandler):
    @ndb.toplevel
    def post(self, author_id):
        guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        author = Author.get_by_id_async(long(author_id))
        greeting.author = author.get_result().userID

        greeting.content = self.request.get('content')
        ndb.transaction_async(greeting.put())

        guestbook = {'guestbook_name': guestbook_name}
        authorid = {'author_id': author_id}
        self.redirect('/?' + urllib.urlencode(guestbook) + '&' + urllib.urlencode(authorid))
# [END guestbook]

# [START register]
class Register(BaseHandler):
    def post(self):
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        new_sessionID = binascii.hexlify(os.urandom(8))
        author = Author(
                sessionID=new_sessionID,
                userID=user_id,
                password=password)
        ndb.transaction_async(author.put())
        author_id = author.key.id()
        self.session['sessionID'] = new_sessionID
        query_params = {'author_id': author_id}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END register]

# [START login]
class Login(BaseHandler):
    def post(self):
        user_id = self.request.get('user_id')
        password = self.request.get('password')
        new_sessionID = binascii.hexlify(os.urandom(8))
        author = Author.query(Author.userID == user_id).get()
        if author is None:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>User is None.</h1>')
            self.response.out.write('</body></html>')
            return
        if author.password != password:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>Password is wrong.</h1>')
            self.response.out.write('</body></html>')
            return
        author.sessionID = new_sessionID
        ndb.transaction_async(author.put())
        author_id = author.key.id()
        self.session['sessionID'] = new_sessionID
        query_params = {'author_id': author_id}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END login]


# [START logout]
class Logout(webapp2.RequestHandler):
    def get(self, author_id):
        author = Author.get_by_id(long(author_id))
        author.sessionID = None
        author.put()
        self.redirect('/')
# [END logout]

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/user/registerpage', RegisterPage),
    ('/user/loginpage', LoginPage),
    ('/api/greeting/sign/user/(\d+)', Guestbook),
    ('/api/user/register', Register),
    ('/api/user/login', Login),
    ('/api/user/logout/(\d+)', Logout)
    ], debug=True, config=config)
# [END app]
