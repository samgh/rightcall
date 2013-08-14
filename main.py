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
        if firstname: loggedIn = True

    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render(loginFailed=self.session.get('login_failed'),
            userLoggedIn=loggedIn, username=firstname))
        self.session['login_failed'] = False

class InvitationInsert(BaseHandler):
    def post(self):
        email = cgi.escape(self.request.get('email-signup')).strip()
        redirect = cgi.escape(self.request.get('redirect'))
        success = invitations.InsertEmail(email)
        self.session['invitation_success'] = success
        self.redirect(redirect)

class InvitationResponse(BaseHandler):
    def get(self):
        emails = invitations.AllEmails()
        self.response.write('<html><body>')
        for email in emails:
            self.response.write('%s<br />' % email.email)
            self.response.write('%s<br />' % email.emailSent)
            self.response.write('%s<br /><br />' % email.date)
        self.response.write('</body></html>')

class NewUserInsert(BaseHandler):
    def post(self):
        firstname = cgi.escape(self.request.get('firstname')).strip()
        lastname = cgi.escape(self.request.get('lastname')).strip()
        email = cgi.escape(self.request.get('email')).strip()
        password = cgi.escape(self.request.get('password'))
        users.CreateNewUser(firstname, lastname, email, password)
        self.redirect('/')

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
        loggedIn = False
        firstname = users.getFirstname(self.session.get('id'))
        if firstname: loggedIn = True

        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/blog.html')
        self.response.write(template.render(loginFailed=self.session.get('login_failed'),
            userLoggedIn=loggedIn, username=firstname))
        self.session['login_failed'] = False

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
    ('/invitationinsert', InvitationInsert),
    ('/invitationresponse', InvitationResponse),
    ('/newuser', NewUser),
    ('/newuserinsert', NewUserInsert),
    ('/responseuser', users.Response),
    ('/login', users.Login),
    ('/logout', users.Logout),
    ('/adwords.*', Adwords),
    ('/.*', NotFoundPageHandler)
], config=config, debug=True)
