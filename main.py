import os
import urllib
import time

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi

import invitations
import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

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
    #('/whatis', WhatIs),
    #('/privacy', Privacy),
    #('/about', About),
    ('/blog', Blog),
    ('/insert', invitations.Insert),
    ('/response', invitations.Response),
    ('/adwords.*', Adwords),
    ('/.*', NotFoundPageHandler)
], debug=True)
