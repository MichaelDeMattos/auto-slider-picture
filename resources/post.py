# -*- coding: utf-8 -*-

from app import db
from model.user import User
from model.post import PostNews

""" This class content scripts for access table PostNews """
class ControllerPostNews(object):
    def __init__(self, *args):
        ...
    
    def get_posts(self):
        try:
            query = db.session.query(PostNews).join(User, PostNews.user_id==User.id).all()
            return query
        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def delete_post(self, file):
        try:
            db.session.query(PostNews).filter_by(file_name=file).delete()
            db.session.commit()
            return {"status": 200}

        except Exception as error:
            print("Error:", error)
            return {"status": 500, "error": str(error)}