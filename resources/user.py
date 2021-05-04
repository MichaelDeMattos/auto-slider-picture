# -*- coding: utf-8 -*-

from app import db
from model.user import UserDB

""" This class content scripts for access table User """
class ControllerUser(object):
    def __init__(self, *args):
        ...
    
    def get_user_by_id(self, id_user):
        try:
            user = UserDB.query.filter_by(id=id_user).first()
            return user.name

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def get_user_by_email(self, email):
        try:
            user = UserDB.query.filter_by(email=email).first()
            return user
        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def new_user(self, email, name, alias_name, password):
        try:
            new_user = UserDB(email=email, 
                              name=name,
                              alias=alias_name,
                              password=password)

            db.session.add(new_user)
            db.session.commit()
            return {"status": 200}

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}