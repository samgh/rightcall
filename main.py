import os
import urllib
import time
from time import sleep
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
        currentUser = users.GetUserByID(self.session.get('user_id'))
        if currentUser:
            loggedIn = True
            firstname = currentUser[0].firstname
        else:
            loggedIn = False
            firstname = ''

        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render(loginFailed=self.session.get('login_failed'),
            userLoggedIn=loggedIn, username=firstname))
        self.session['login_failed'] = False


#        allusers = users.GetAllUsers()
#        for user in allusers:
#            #users.SetPassword(user.email, '1234')
#            users.SetLevel(user.email, 'Basic')
#        users.SetLevel(users.UserInDB('sam@rightcall.co')[0].email, 'Admin')

class InvitationInsert(BaseHandler):
    def post(self):
        email = cgi.escape(self.request.get('email-signup')).strip()
#        redirect = cgi.escape(self.request.get('redirect'))
        success = invitations.InsertEmail(email)
        self.session['invitation_success'] = success

        emails = invitations.EmailsNotSent()
        for email in emails:
            if email.email:
                mail.send_mail(sender="Sam Gavis-Hughson <rightcallinfo@gmail.com>",
                to=email.email,
                subject="Welcome to RightCall!",
                body="""
                    Welcome, and thank you so much for signing up for RightCall!

                    We are currently working out the final bugs, but when we are ready, 
                    you will be the first to know.  Keep your eyes peeled for an 
                    invite code and make sure that you whitelist all emails from 
                    rightcallinfo@gmail.com.

                    While you're waiting, make sure to check us out on Facebook 
                    (SamRightCall) and Twitter (@SamRightCall).  We would love to 
                    connect with you!  Also make sure to <strong>tell your friends 
                    about RightCall.

                    We look forwards to getting to know you and helping you out.  If you 
                    have any comments, questions, or just want to say hi, don't hesitate 
                    to email me at sam@rightcall.co.

                    Sam Gavis-Hughson
                    Founder and CEO, RightCall LLC
                """,
                html="""
                <html>
                    <body>
                        <p>Welcome, and thank you so much for signing up for 
                        <a href="http://www.rightcall.co" title="RightCall">RightCall</a>!</p>
                        <p>We are currently working out the final bugs, but when we are ready, 
                        you will be the first to know.  Keep your eyes peeled for an 
                        <strong>invite code</strong> and make sure that you whitelist all emails 
                        from <a href="mailto:rightcallinfo@gmail.com">rightcallinfo@gmail.com</a>.</p>
                        <p>While you're waiting, make sure to check us out on 
                        <a href="http://www.facebook.com/samrightcall">Facebook</a> and 
                        <a href="http://www.twitter.com/samrightcall">Twitter</a>.  We would 
                        love to connect with you!  Also make sure to <strong>tell your friends 
                        about RightCall.</strong></p>
                        <p>We look forwards to getting to know you and helping you out.  If you 
                        have any comments, questions, or just want to say hi, don't hesitate to 
                        email me at <a href="mailto:sam@rightcall.co">sam@rightcall.co</a>.</p>
                        Sam Gavis-Hughson
                        <br />
                        Founder and CEO, RightCall LLC
                    </body>
                </html>
                """)
            invitations.EmailSent(email.email)
#        self.redirect(redirect)
        self.redirect('/thankyou')

class InvitationResponse(BaseHandler):
    def get(self):
        currentUser = users.GetUserByID(self.session.get('user_id'))
        if currentUser and currentUser[0].user_level == 'Admin': 
            emails = invitations.AllEmails()
            self.response.write('<html><body>')
            for email in emails:
                self.response.write('%s<br />' % email.email)
                self.response.write('%s<br />' % email.emailSent)
                self.response.write('%s<br /><br />' % email.date)
            self.response.write('</body></html>')
        else: 
            self.error(404)
            self.response.headers ['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('templates/error.html')
            self.response.write(template.render())

class ThankYou(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/thankyou.html')
        self.response.write(template.render())

class NewUserInsert(BaseHandler):
    def post(self):
        firstname = cgi.escape(self.request.get('firstname')).strip()
        lastname = cgi.escape(self.request.get('lastname')).strip()
        email = cgi.escape(self.request.get('email')).strip()
        password = cgi.escape(self.request.get('password'))
        level = cgi.escape(self.request.get('level'))
        users.CreateNewUser(firstname, lastname, email, password, user_level=level)
        self.redirect('/')

class UserResponse(BaseHandler):
    def get(self):
        currentUser = users.GetUserByID(self.session.get('user_id'))
        if currentUser and currentUser[0].user_level == 'Admin': 
            AllUsers = users.GetAllUsers()
            self.response.write('<html><body>')
            for user in AllUsers:
                self.response.write('%s ' % user.firstname)
                self.response.write('%s<br />' % user.lastname)
                self.response.write('%s<br />' % user.email)
                self.response.write('%s ' % user.password)
                self.response.write('%s<br />' % user.salt)
                self.response.write('%s<br />' % user.user_id)
                self.response.write('%s<br /><br />' % user.user_level)
            self.response.write('</body></html>')
        else: 
            self.error(404)
            self.response.headers ['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('templates/error.html')
            self.response.write(template.render())

class UserLogin(BaseHandler):
    def post(self):
        email = cgi.escape(self.request.get('email')).strip()
        password = cgi.escape(self.request.get('password'))
        redirect = cgi.escape(self.request.get('redirect'))
        if users.ValidateUser(email, password):
            self.session['user_id'] = users.SetUserID(email)
            self.session['login_failed'] = False
            sleep(0.5)
            self.redirect(redirect)
        else:
            self.session['login_failed'] = True
            self.redirect(redirect)

class UserLogout(BaseHandler):
    def get(self):
        currentUser = users.GetUserByID(self.session.get('user_id'))
        logging.info('test1')
        if currentUser:
            logging.info('test2')
            users.UnsetUserID(currentUser[0].email)
            self.session['user_id'] = '0'
            self.redirect('/')
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
        logging.info(self.session.get('user_id'))
        currentUser = users.GetUserByID(self.session.get('user_id'))
        if currentUser:
            loggedIn = True
            firstname = currentUser[0].firstname
        else:
            loggedIn = False
            firstname = ''

        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/blog.html')
        self.response.write(template.render(loginFailed=self.session.get('login_failed'),
            userLoggedIn=loggedIn, username=firstname))
        self.session['login_failed'] = False

class Adwords(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

class NewUser(BaseHandler):
    def get(self):
        currentUser = users.GetUserByID(self.session.get('user_id'))
        if currentUser and currentUser[0].user_level == 'Admin': 
            self.response.headers ['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('templates/newuser.html')
            self.response.write(template.render())
        else: 
            self.error(404)
            self.response.headers ['Content-Type'] = 'text/html'
            template = JINJA_ENVIRONMENT.get_template('templates/error.html')
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
#    ('/whatis', WhatIs),
#    ('/privacy', Privacy),
#    ('/about', About),
    ('/blog', Blog),
    ('/invitationinsert', InvitationInsert),
    ('/invitationresponse', InvitationResponse),
    ('/thankyou', ThankYou),
    ('/newuser', NewUser),
    ('/newuserinsert', NewUserInsert),
    ('/userresponse', UserResponse),
    ('/login', UserLogin),
    ('/logout', UserLogout),
    ('/adwords.*', Adwords),
    ('/.*', NotFoundPageHandler)
], config=config, debug=False)
