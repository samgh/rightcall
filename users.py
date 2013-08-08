import os
import urllib
import time

from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi

import hashlib
import uuid

USERS_DB_NAME = 'users_db'

def db_key(db_name=USERS_DB_NAME):
    return ndb.Key('Insert', db_name)

class LoginRequest(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.StringProperty()
    salt = ndb.BlobProperty()
    password = ndb.BlobProperty()

class Insert(webapp2.RequestHandler):
    def post(self):
        db_name = self.request.get('db_name', USERS_DB_NAME)

        firstname = cgi.escape(self.request.get('firstname')).strip()
        lastname = cgi.escape(self.request.get('lastname')).strip()
        email = cgi.escape(self.request.get('email')).strip()
        salt = uuid.uuid4().hex
        saltypass = cgi.escape(self.request.get('password')) + salt
        password = hashlib.sha256(saltypass).hexdigest()

        query = LoginRequest.query(LoginRequest.email == email)
        inDB = query.fetch(1)
        if not inDB:
            loginRequest = LoginRequest(parent=db_key(db_name))
            loginRequest.firstname = firstname
            loginRequest.lastname = lastname
            loginRequest.email = email
            loginRequest.salt = salt
            loginRequest.password = password
            loginRequest.put()
            self.redirect('/')
        else:
            self.redirect('/')


class Response(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        db_name = self.request.get('db_name', USERS_DB_NAME)

        emails_query = LoginRequest.query(ancestor=db_key(db_name))
        emails = emails_query.fetch(100)

        for message in emails:
            self.response.write(message.firstname)
            self.response.write('&nbsp%s' % message.lastname)
            self.response.write('&nbsp%s' % cgi.escape(message.email))
            self.response.write('&nbsp%s' % message.salt)
            self.response.write('&nbsp%s<br />' % message.password)

class Validate(webapp2.RequestHandler):
    def post(self):
        email = cgi.escape(self.request.get('email')).strip()
        password = cgi.escape(self.request.get('password'))

        password_query = LoginRequest.query(LoginRequest.email == email)
        inDB = password_query.fetch(1)
        if inDB:
            password = hashlib.sha256(password + inDB[0].salt).hexdigest()
            if inDB[0].password == password:
                self.response.write('valid')
            else:
                self.response.write('invalid')
        else:
            self.response.write('super invalid')