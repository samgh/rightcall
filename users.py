import logging

from google.appengine.ext import ndb
from webapp2_extras import sessions

import hashlib
import uuid

#USERS_DB_NAME = 'users_db'

#def db_key(db_name=USERS_DB_NAME):
#    return ndb.Key('Insert', db_name)

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

def UnsetUserID(email):
    userRequest = UserInDB(email)
    if userRequest:
        userRequest[0].user_id = '-1'
        userRequest[0].put()
        return True
    return False

def GetAllUsers():
    query = UserRequest.query()
    return query.fetch()