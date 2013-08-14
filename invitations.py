import os
import urllib
import time

from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi
import logging

INVITATIONS_DB_NAME = 'invitations_db'

#def db_key(db_name=INVITATIONS_DB_NAME):
#    return ndb.Key('Insert', db_name)

class InvitationRequest(ndb.Model):
    email = ndb.StringProperty()
    emailSent = ndb.BooleanProperty(default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

# Inserts 'email' into DB. Return True if email is not in DB and gets 
# inserted or False if already in DB.
def InsertEmail(email):
    query = InvitationRequest.query(InvitationRequest.email == email)
    inDB = query.fetch()
    if not inDB:
        invitationRequest = InvitationRequest()
        invitationRequest.email = email
        a = invitationRequest.put()
        return True
    else:
        return False

# Returns True if 'email' is in DB and False if not.
def EmailInDB(email):
    query = InvitationRequest.query(InvitationRequest.email == email)
    inDB = query.fetch()
    if not inDB: return False
    else: return True

# Returns list of InvitationRequest entities. Default sort by date, 
# newest first. Pass other sort: eg. 'invitation.InvitationRequest.email'
def AllEmails(sort=-InvitationRequest.date):
    query = InvitationRequest.query().order(sort)
    return query.fetch()

# Returns list of InvitationRequest entities where emailSent property == False.
# Sort: see above.
def EmailsNotSent(sort=-InvitationRequest.date):
    query = InvitationRequest.query(InvitationRequest.emailSent == False).order(sort)
    return query.fetch()

# Set 'email' entity emailSent property to True. Return False if email
# not in DB.
def EmailSent(email):
    query = InvitationRequest.query(InvitationRequest.email == email)
    inDB = query.fetch()
    if inDB:
        inDB[0].emailSent = True
        inDB[0].put()
        return True
    else: return False

# Set 'email' entity emailSent property to False. Return False if email
# not in DB.
def EmailNotSent(email):
    query = InvitationRequest.query(InvitationRequest.email == email)
    inDB = query.fetch()
    if inDB:
        inDB[0].emailSent = False
        inDB[0].put()
        return True
    else: return False

# Set all InvitationRequest entities emailSent property to False.
def SetAllEmailsNotSent():
    query = InvitationRequest.query()
    emails = query.fetch()
    for email in emails:
        email.emailSent = False
        email.put()

#class Insert(webapp2.RequestHandler):
#    def post(self):
#        db_name = self.request.get('db_name', INVITATIONS_DB_NAME)
#
#        email = cgi.escape(self.request.get('email-signup')).strip()
#        redirect = self.request.get('redirect')
#        query = InvitationRequest.query(InvitationRequest.email == email)
#        inDB = query.fetch(1)
#        if not inDB:
#            invitationRequest = InvitationRequest(parent=db_key(db_name))
#            invitationRequest.email = cgi.escape(self.request.get('email-signup'))
#            invitationRequest.put()
#            self.redirect(redirect)
#        else:
#           self.redirect(redirect)


class Response(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        db_name = self.request.get('db_name', INVITATIONS_DB_NAME)

        emails_query = InvitationRequest.query().order(-InvitationRequest.date)#ancestor=db_key(db_name)).order(-InvitationRequest.date)
        emails = emails_query.fetch(100)

        for message in emails:
            self.response.write(cgi.escape(message.email))
            self.response.write('<br />%s<br />' % message.date)
            self.response.write('%s<br /><br />' % message.emailSent)
#
#        #self.redirect('/')