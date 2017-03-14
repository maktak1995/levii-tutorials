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
import os
import cgi
import urllib

from google.appengine.ext import ndb

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# [START tag]
class Tag(ndb.Model):
    type = ndb.StringProperty()  # type of tag
# [END tag]

    # [START query]
    @classmethod
    def query_tag(cls):
        return cls.query().order()
    # [END query]


# [START book]
class Book(ndb.Model):
    name = ndb.StringProperty()  # guestbook's name
    number = ndb.IntegerProperty()  # the number of contents in book
    tag = ndb.KeyProperty(kind=Tag, repeated=True)  # the guestbook's tag
# [END book]

    # [START query]
    @classmethod
    def query_book(cls):
        return cls.query().order(cls.name)
    # [END query]

    @ndb.transactional
    @ndb.toplevel
    def add(self, contents):
        greeting = Greeting(parent=self.key, content=contents)
        greeting.put_async()
        self.number += 1
        self.put_async()
        return greeting

    @ndb.transactional
    @ndb.toplevel
    def delete(self, greeting):
        self.number -= 1
        self.put_async()
        greeting.key.delete_async()
        return

    @ndb.tasklet
    def get_greetings(self):
        greetings = yield Greeting.query_greeting(self.key).fetch_async(20)
        raise ndb.Return(greetings)


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
    @ndb.toplevel
    def get(self, guestbook_id):
        book = Book.get_by_id(long(guestbook_id))
        if book is None:
            self.response.out.write('<h1>Not Found</h1>')
            self.response.out.write('</body></html>')
            return
        tags = Tag.query_tag().fetch_async(20)
        greetings = book.get_greetings()
        template_values = {
            'book': book,
            'greetings': greetings.get_result(),
            'tags': tags.get_result()
        }
        template = JINJA_ENVIRONMENT.get_template('book.html')
        self.response.write(template.render(template_values))


class MainPage(webapp2.RequestHandler):
    @ndb.toplevel
    def get(self):
        tag_type = self.request.get('tag')
        if tag_type != '':
            tag = Tag.query(Tag.type == tag_type).get_async()
            if tag is None:
                self.response.out.write('<html><body>')
                self.response.out.write('<h1>Tag is None</h1>')
                self.response.out.write('</body></html>')
                return
            books = Book.query(Book.tag == tag.key)
        else:
            books = Book.query_book()
        template_values = {
            'books': books,
            'tags': Tag.query_tag().fetch_async(20).get_result()
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# [START add book]
class AddBook(webapp2.RequestHandler):
    @ndb.transactional(xg=True)
    @ndb.toplevel
    def post(self):
        guestbook_name = self.request.get('guestbook_name')  # Get guestbook name from user's post data
        tag_id = self.request.get('tag_id')  # Get guestbook name from user's post data
        book = Book(
            name=guestbook_name,
            number=0)
        if tag_id != '':
            new_tag = Tag.get_by_id(long(tag_id))
            if new_tag.key not in book.tag:
                book.tag.append(new_tag.key)
        book.put_async()
        # [END submit]
        self.redirect('/')
# [END add book]


# [START add tag]
class AddTag(webapp2.RequestHandler):
    @ndb.toplevel
    def post(self):
        tag_type = self.request.get('tag_type')
        if tag_type == '':
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>Tag name is None</h1>')
            self.response.out.write('</body></html>')
            return

        tag = Tag.query(Tag.type == tag_type).get()
        if tag is None:
            new_tag = Tag(type=tag_type)
            new_tag.put_async()
        else:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>This tag is already exist</h1>')
            self.response.out.write('</body></html>')
            return
        # [END submit]
        self.redirect('/')
# [END add tag]


# [START submit]
class SubmitForm(webapp2.RequestHandler):
    @ndb.toplevel
    def post(self, guestbook_id):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        content = self.request.get('content')
        if content == '':
            self.redirect('/books/' + str(guestbook_id))
            return
        book = Book.get_by_id(long(guestbook_id))
        if book is None:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>Not Found</h1>')
            self.response.out.write('</body></html>')
            return
        book.add(content)

        # [END submit]
        self.redirect('/books/' + str(guestbook_id))
# [END submit]


# [START delete]
class DeleteGreeting(webapp2.RequestHandler):
    def post(self, guestbook_id, greeting_id):
        book = Book.get_by_id(long(guestbook_id))
        greeting = Greeting.get_by_id(long(greeting_id), parent=book.key)
        if greeting is None:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>Not Found</h1>')
            self.response.out.write('</body></html>')
            return
        book.delete(greeting)
        # [END submit]
        self.redirect('/books/' + str(guestbook_id))
# [END delete]


# [START update]
class UpdateBook(webapp2.RequestHandler):
    @ndb.transactional(xg=True)
    @ndb.toplevel
    def post(self, guestbook_id):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        newbook_name = self.request.get('newbook_name')  # Get new guestbook name from user's post data
        tag_id = self.request.get('tag_id')  # Get new guestbook tag from user's post data
        book = Book.get_by_id(long(guestbook_id))
        new_tag = Tag.get_by_id(long(tag_id))
        if book is None or new_tag is None:
            self.response.out.write('<html><body>')
            self.response.out.write('<h1>Not Found</h1>')
            self.response.out.write('</body></html>')
            return
        if newbook_name != '':
            book.name = newbook_name
        if new_tag.key not in book.tag:
            book.tag.append(new_tag.key)
        book.put_async()

        # [END submit]
        self.redirect('/books/' + str(guestbook_id))
# [END update]

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/books/(\d+)', BookPage),
    ('/api/books/addbook', AddBook),
    ('/api/books/(\d+)/updatebook', UpdateBook),
    ('/api/books/(\d+)/greeting', SubmitForm),
    ('/api/books/(\d+)/greetings/(\d+)/delete', DeleteGreeting),
    ('/api/tags/addtag', AddTag)
])
# [END all]
