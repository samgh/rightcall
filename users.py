import os
import urllib
import time
import logging
from time import sleep

from google.appengine.ext import ndb
from google.appengine.api import mail
from webapp2_extras import sessions

import jinja2
import webapp2
import cgi

import hashlib
import uuid

USERS_DB_NAME = 'users_db'

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

def db_key(db_name=USERS_DB_NAME):
    return ndb.Key('Insert', db_name)

class UserRequest(ndb.Model):
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.StringProperty()
    salt = ndb.BlobProperty()
    password = ndb.BlobProperty()
    user_id = ndb.StringProperty()

def UserInDB(email):
    query = UserRequest.query(UserRequest.email == email)
    inDB = query.fetch()
    if inDB: return inDB
    return False

def CreateNewUser(firstname, lastname, email, password, user_id='-1'):
    userRequest = UserInDB(email)
    if not userRequest:
        salt = uuid.uuid4().hex
        password = hashlib.sha256(password + salt).hexdigest()
        userRequest = UserRequest(firstname=firstname, lastname=lastname,
            email=email, password=password, salt=salt, user_id=user_id)
        userRequest.put()
        return True
    return False

def ValidateUser(email, password):
    userRequest = UserInDB(email)
    if userRequest:
        if (userRequest[0].password == 
            hashlib.sha256(password + userRequest[0].salt).hexdigest()):
            return True
    return False

def GetUserByID(user_id):
    query = UserRequest.query(UserRequest.user_id == user_id)
    return query.fetch()

def SetUserID(email):
    userRequest = UserInDB(email)
    if userRequest:
        userRequest[0].user_id = uuid.uuid4().hex
        userRequest[0].put()
        return userRequest[0].user_id
    return False
    

class Insert(webapp2.RequestHandler):
    def post(self):
        db_name = self.request.get('db_name', USERS_DB_NAME)

        firstname = cgi.escape(self.request.get('firstname')).strip()
        lastname = cgi.escape(self.request.get('lastname')).strip()
        email = cgi.escape(self.request.get('email')).strip()
        salt = uuid.uuid4().hex
        saltypass = cgi.escape(self.request.get('password')) + salt
        password = hashlib.sha256(saltypass).hexdigest()

        query = UserRequest.query(UserRequest.email == email)
        inDB = query.fetch(1)
        if not inDB:
            loginRequest = UserRequest(parent=db_key(db_name))
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

        emails_query = UserRequest.query()#ancestor=db_key(db_name))
        emails = emails_query.fetch()

        logging.info(len(emails))
        for message in emails:
            self.response.write(message.firstname)
            self.response.write('&nbsp%s' % message.lastname)
            self.response.write('&nbsp%s' % cgi.escape(message.email))
            self.response.write('&nbsp%s' % message.salt)
            self.response.write('&nbsp%s' % message.password)
            self.response.write('&nbsp%s<br />' % message.user_id)

class Login(BaseHandler):
    def post(self):
        email = cgi.escape(self.request.get('email')).strip()
        password = cgi.escape(self.request.get('password'))
        redirect = '/' + cgi.escape(self.request.get('redirect'))

        password_query = UserRequest.query(UserRequest.email == email)
        inDB = password_query.fetch(1)
        if inDB:
            password = hashlib.sha256(password + inDB[0].salt).hexdigest()
            if inDB[0].password == password:
                a = uuid.uuid4().hex
                inDB[0].user_id = a
                inDB[0].put()
                self.session['id'] = a
                self.session['login_failed'] = False
                sleep(0.5)
                logging.info(redirect)
                self.redirect(redirect)
            else:
                self.session['login_failed'] = True
                self.redirect(redirect)
        else:
            self.session['login_failed'] = True
            self.redirect(redirect)

class Logout(BaseHandler):
    def get(self):
        query = UserRequest.query(UserRequest.user_id == self.session.get('id'))
        response = query.fetch(1)
        if response:
            response[0].user_id = '-1'
            response[0].put()
        self.session['id'] = '0'
        self.redirect('/')

def getFirstname(i):
    query = UserRequest.query(UserRequest.user_id == i)
    response = query.fetch(1)
    logging.info(response)
    if not response: return None
    return response[0].firstname