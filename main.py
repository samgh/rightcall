import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

INVITATIONS_DB_NAME = 'invitations_db'

def db_key(db_name=INVITATIONS_DB_NAME):
    return ndb.Key('Insert', db_name)

class InvitationRequest(ndb.Model):
    email = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class Insert(webapp2.RequestHandler):
    def post(self):
        db_name = self.request.get('db_name', INVITATIONS_DB_NAME)

        email = cgi.escape(self.request.get('email-signup')).strip()
        redirect = self.request.get('redirect')
        query = InvitationRequest.query(InvitationRequest.email == email)
        inDB = query.fetch(1)
        if not inDB:
            invitationRequest = InvitationRequest(parent=db_key(db_name))
            invitationRequest.email = cgi.escape(self.request.get('email-signup'))
            invitationRequest.put()
            self.redirect(redirect)
        else:
            self.redirect(redirect)


class Response(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        db_name = self.request.get('db_name', INVITATIONS_DB_NAME)

        emails_query = InvitationRequest.query(ancestor=db_key(db_name)).order(-InvitationRequest.date)
        emails = emails_query.fetch(100)

        for message in emails:
            self.response.write(cgi.escape(message.email))
            self.response.write('&nbsp%s<br />' % message.date)

        #self.redirect('/')

class Home(webapp2.RequestHandler):
    def get(self):
    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render())

class WhatIs(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/whatis.html')
        self.response.write(template.render())


class About(webapp2.RequestHandler):
    def get(self):
    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render())

class Privacy(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/privacy.html')
        self.response.write(template.render())

class Blog(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/blog.html')
        self.response.write(template.render())

class Adwords(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

class NotFoundPageHandler(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/error.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/', Home),
    ('/whatis', WhatIs),
    ('/privacy', Privacy),
    ('/about', About),
    ('/blog', Blog),
    ('/insert', Insert),
    ('/response', Response),
    ('/adwords.*', Adwords),
    ('/.*', NotFoundPageHandler)
], debug=True)
