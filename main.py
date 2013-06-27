import os
import urllib
import time
import gdata.spreadsheet.service

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2
import cgi

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

class Home(webapp2.RequestHandler):
    def get(self):
    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/home.html')
        self.response.write(template.render())

class Features(webapp2.RequestHandler):
    def get(self):
    	self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/features.html')
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

class TryItNow(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/try.html')
        self.response.write(template.render())

class FAQ(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/faq.html')
        self.response.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/about.html')
        self.response.write(template.render())

class Pricing(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/pricing.html')
        self.response.write(template.render())

class Blog(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/blog.html')
        self.response.write(template.render())

class Survey(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/survey.html')
        self.response.write(template.render())

class Response(webapp2.RequestHandler):
    def post(self):
        input_email = cgi.escape(self.request.get('email'))
        input_feedback = cgi.escape(self.request.get('feedback'))

        email = 'rightcallinfo@gmail.com'
        password = '3jajwuth123'
        weight = '180'
        spreadsheet_key = '0Ar7gsv4L_JqddEo0b25aUjY5aElvSHlKNERrSkJxVlE'
        worksheet_id = 'od6'

        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = email
        spr_client.password = password
        spr_client.source = 'Example Spreadsheet Writing Application'
        spr_client.ProgrammaticLogin()

        # Prepare the dictionary to write                                                                                                                                                                           
        dict = {}
        dict['email'] = input_email
        dict['feedback'] = input_feedback
        dict['time'] = time.strftime('%b, %d, %H:%M:%S')
        dict['weight'] = weight

        entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
          self.redirect("/thanks")
        else:
          print "Insert row failed."

class Thanks(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/thanks.html')
        self.response.write(template.render())

class TryAgain(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/tryagain.html')
        self.response.write(template.render())

class SurveyIntro(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/surveyintro.html')
        self.response.write(template.render())

class Survey1Upload(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/survey1upload.html')
        self.response.write(template.render())

class Survey1(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/survey1.html')
        self.response.write(template.render())

class Survey1Response(webapp2.RequestHandler):
    def post(self):
        sameCarrier = cgi.escape(self.request.get('sameCarrier'))
        badCarrier = self.request.get_all('badCarrier')
        preferredDevice = self.request.get_all('preferredDevice')
        deviceName = cgi.escape(self.request.get('deviceName'))

        homeZipcode = cgi.escape(self.request.get('homeZipcode'))
        workZipcode = cgi.escape(self.request.get('workZipcode'))
        travel = cgi.escape(self.request.get('travel'))
        travelZipcode = self.request.get_all('travelZipcode')

        commentsText = cgi.escape(self.request.get('commentsText'))

        userName = cgi.escape(self.request.get('name'))
        userEmail = cgi.escape(self.request.get('email'))

        email = 'rightcallinfo@gmail.com'
        password = '3jajwuth123'
        weight = '180'
        spreadsheet_key = '0Ar7gsv4L_JqddEthX0JUMnNSSE5ZbWFJVEo1SDU3WHc'
        worksheet_id = 'od6'

        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = email
        spr_client.password = password
        spr_client.source = 'Example Spreadsheet Writing Application'
        spr_client.ProgrammaticLogin()

        # Prepare the dictionary to write                                                                                                                                                                           
        dict = {}
        dict['samecarrier'] = sameCarrier
        dict['badcarrier'] = ', '.join(badCarrier)
        dict['preferreddevice'] = ', '.join(preferredDevice)
        dict['devicename'] = deviceName
        dict['homezipcode'] = homeZipcode
        dict['workzipcode'] = workZipcode
        dict['travel'] = travel
        dict['travelzipcode'] = ', '.join(travelZipcode)
        dict['comments'] = commentsText
        dict['name'] = userName
        dict['email'] = userEmail
        dict['time'] = time.strftime('%b, %d, %H:%M:%S')
        dict['weight'] = weight

        entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
            self.redirect("/thankyou")
        else:
            print "Please go back and try again."

class Survey2(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/survey2.html')
        self.response.write(template.render())


class Survey2Response(webapp2.RequestHandler):
    def post(self):
        currentCarrier = cgi.escape(self.request.get('currentCarrierRadio'))
        currentAmount = cgi.escape(self.request.get('currentAmount'))
        sameCarrier = cgi.escape(self.request.get('sameCarrier'))
        badCarrier = self.request.get_all('badCarrier')
        preferredDevice = self.request.get_all('preferredDevice')
        deviceName = cgi.escape(self.request.get('deviceName'))

        homeZipcode = cgi.escape(self.request.get('homeZipcode'))
        workZipcode = cgi.escape(self.request.get('workZipcode'))
        travel = cgi.escape(self.request.get('travel'))
        travelZipcode = self.request.get_all('travelZipcode')

        amountMinutes = cgi.escape(self.request.get('amountMinutes'))
        amountTexts = cgi.escape(self.request.get('amountTexts'))
        amountData = cgi.escape(self.request.get('amountData'))

        commentsText = cgi.escape(self.request.get('commentsText'))

        userName = cgi.escape(self.request.get('name'))
        userEmail = cgi.escape(self.request.get('email'))

        email = 'rightcallinfo@gmail.com'
        password = '3jajwuth123'
        weight = '180'
        spreadsheet_key = '0Ar7gsv4L_JqddGk2am1zMjVsMmtFTGZsczhzWi1NQVE'
        worksheet_id = 'od6'

        spr_client = gdata.spreadsheet.service.SpreadsheetsService()
        spr_client.email = email
        spr_client.password = password
        spr_client.source = 'Example Spreadsheet Writing Application'
        spr_client.ProgrammaticLogin()

        # Prepare the dictionary to write                                                                                                                                                                           
        dict = {}
        dict['currentcarrier'] = currentCarrier
        dict['currentamount'] = currentAmount
        dict['samecarrier'] = sameCarrier
        dict['badcarrier'] = ', '.join(badCarrier)
        dict['preferreddevice'] = ', '.join(preferredDevice)
        dict['devicename'] = deviceName
        dict['homezipcode'] = homeZipcode
        dict['workzipcode'] = workZipcode
        dict['travel'] = travel
        dict['travelzipcode'] = ', '.join(travelZipcode)
        dict['amountminutes'] = amountMinutes
        dict['amounttexts'] = amountTexts
        dict['amountdata'] = amountData
        dict['comments'] = commentsText
        dict['name'] = userName
        dict['email'] = userEmail
        dict['time'] = time.strftime('%b, %d, %H:%M:%S')
        dict['weight'] = weight

        entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
        if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
            self.redirect("/thankyou")
        else:
            print "Please go back and try again."

class ThankYou(webapp2.RequestHandler):
    def get(self):
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/thankyou.html')
        self.response.write(template.render())

class NotFoundPageHandler(webapp2.RequestHandler):
    def get(self):
        self.error(404)
        self.response.headers ['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/error.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/', Home),    
    ('/features', Features),
    ('/privacy', Privacy),
    ('/tryitnow', TryItNow),
    ('/faq', FAQ),
    ('/about', About),
    ('/pricing', Pricing),
    ('/blog', Blog),
    ('/survey', Survey),
    ('/response', Response),
    ('/thanks', Thanks),
    ('/tryagain', TryAgain),
    ('/surveyintro', SurveyIntro),
    ('/survey1upload', Survey1Upload),
    ('/survey1', Survey1),
    ('/survey1response', Survey1Response),
    ('/survey2', Survey2),
    ('/survey2response', Survey2Response),
    ('/thankyou', ThankYou),
    ('/.*', NotFoundPageHandler)
], debug=True)
