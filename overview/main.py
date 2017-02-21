# Copyright 2015 Google Inc. All rights reserved.
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

"""Cloud Datastore NDB API guestbook sample.

This sample is used on this page:
    https://cloud.google.com/appengine/docs/python/ndb/

For more information, see README.md
"""

# [START all]
import cgi
import urllib

from google.appengine.ext import ndb

import webapp2

# [START book]
class Book(ndb.Model):
    name = ndb.StringProperty()  # guestbook's name
    number = ndb.IntegerProperty()  # the number of contents in book
# [END book]

# [START query]
    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)


# [START greeting]
class Greeting(ndb.Model):  # Make the "Greeting" model
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()  # Define the string property "content"
    date = ndb.DateTimeProperty(auto_now_add=True)  # Add the date property when Greeting instance made (auto_now_add)
# [END greeting]

# [START query]
    @classmethod
    def query_greeting(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)
# [END query]


class BookPage(webapp2.RequestHandler):
    def get(self, guestbook_id):
        self.response.out.write('<html><body>')
        book = Book.get_by_id(long(guestbook_id))

        if book is None:
            self.response.out.write('<h1>Not Found</h1>')
            self.response.out.write('</body></html>')
            return

        ancestor_key = book.key
        greetings = Greeting.query_greeting(ancestor_key).fetch(20)

        for greeting in greetings:
            self.response.out.write('<blockquote>%s</blockquote>' %
                                    cgi.escape(greeting.content))

        self.response.out.write("""
          <hr>
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
        </body>
      </html>""" % urllib.urlencode({'guestbook_id': guestbook_id}))


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')

        self.response.out.write('<ul>')
        for book in Book.query_book():
            book_item = '<li><a href="/books/{id}">{name} : {greeting_num}</a></li>'.format(
                id=book.key.id(),
                name=cgi.escape(book.name),
                greeting_num=cgi.escape(str(book.number))
            )
            self.response.out.write(book_item)
        self.response.out.write('</ul>')
# [END query]

        self.response.out.write("""
          <hr>
          <form action="/addbook?%s" method="post">
            <form>Guestbook name to add: <input value="" name="guestbook_name">
            <input type="submit" value="add book"></form>
          </form>
        </body>
      </html>""")

# [START add book]
class AddBook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')  # Get guestbook name from user's post data
        book = Book(
            name=guestbook_name,
            number=0
        )
        book.put()
        # [END submit]

        self.redirect('/')
# [END add book]


# [START submit]
class SubmitForm(webapp2.RequestHandler):
    def post(self):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        guestbook_id = self.request.get('guestbook_id')  # Get guestbook name from user's post data
        book = Book.get_by_id(long(guestbook_id))
        book.number += 1
        book.put()
        greeting = Greeting(parent=book.key,
                            content=self.request.get('content'))
        greeting.put()

# [END submit]
        self.redirect('/books/' + str(guestbook_id))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/books/(\d+)', BookPage),
    ('/sign', SubmitForm),
    ('/addbook', AddBook)
])
# [END all]
