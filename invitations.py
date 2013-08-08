import os
import urllib
import time

from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi

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