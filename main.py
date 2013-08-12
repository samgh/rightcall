import os
import urllib
import time
import logging

from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
from webapp2_extras import sessions
import cgi
import uuid

import invitations
import users
import basehandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class Home(BaseHandler):
    def get(self):
        loggedIn = False
        firstname = users.getFirstname(self.session.get('id'))
        if users.getFirstname(self.session.get('id')):
            loggedIn = True
        self.session['foo'] = 'bar'
    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render(loginFailed=self.session.get('login_failed'),
            userLoggedIn=loggedIn, username=firstname))
        self.response.write(self.session.get('foo'))

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

class Blog(BaseHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/blog.html')
        self.response.write(template.render())

class Adwords(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

class NewUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/newuser.html')
        self.response.write(template.render())

class NotFoundPageHandler(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/error.html')
        self.response.write(template.render())

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': uuid.uuid4().hex,
    'session_max_age': 60 * 60 * 24
}

application = webapp2.WSGIApplication([
    ('/', Home),
    ('/whatis', WhatIs),
    ('/privacy', Privacy),
    ('/about', About),
    ('/blog', Blog),
    ('/insert', invitations.Insert),
    ('/response', invitations.Response),
    ('/newuser', NewUser),
    ('/insertuser', users.Insert),
    ('/responseuser', users.Response),
    ('/login', users.Login),
    ('/logout', users.Logout),
    ('/adwords.*', Adwords),
    ('/.*', NotFoundPageHandler)
], config=config, debug=True)
