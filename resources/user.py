# -*- coding: utf-8 -*-

from model.user import User

""" This class content scripts for access table User """
class ControllerUser(object):
    def __init__(self, *args):
        ...
    
    def get_user_by_id(self, id_user):
        try:
            user = User.query.filter_by(id=id_user).first()
            return user.name

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}