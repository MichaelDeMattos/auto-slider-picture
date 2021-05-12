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
    
    def new_generate_recovery_code(self, code, email):
        try:
            new_code = UserDB.query.filter_by(email=email).first()
            
            if new_code:
                new_code.code_recovery = code
                db.session.add(new_code)
                db.session.commit()
                return {"status": 200}

            if not new_code:
                return {"status": 404}

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def get_recovery_code_by_email(self, email):
        try:
            code = UserDB.query.filter_by(email=email).first()
            if code:
                return code.code_recovery
            else:
                return None

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def update_password_by_email(self, email, new_password):
        try:
            user_password_update = UserDB.query.filter_by(email=email).first()
            if user_password_update:
                user_password_update.password = new_password
                user_password_update.code_recovery = ""
                db.session.add(user_password_update)
                db.session.commit()
                return {"status": 200}
            
            if not user_password_update:
                return {"status": 404}

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
