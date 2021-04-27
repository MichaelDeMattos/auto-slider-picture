# -*- coding: utf-8 -*-

from app import db
from model.user import User
from model.post import PostNews, PostNewsLog
from resources.util import format_text_for_ascci

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
    
    def delete_post(self, file, user_id):
        try:
            """ Register log exclude """
            query = db.session.query(PostNews).filter_by(file_name=file).first()
            log = PostNewsLog(
                user_id=user_id, 
                file_name=query.file_name,
                create_date=query.create_date)
            db.session.add(log)
            
            """ Delete register in database """
            db.session.query(PostNews).filter_by(file_name=file).delete()
            db.session.commit()
            return {"status": 200}

        except Exception as error:
            db.session.rollback()
            print("Error:", error)
            return {"status": 500, "error": str(error)}
    
    """ Register new Post file """
    def new_post(self, user_id, file_name):
        try:
            
            """ Check file_name if exists """
            post_exist = db.session.query(PostNews).filter_by(file_name=file_name).first()
            if post_exist:
                return {"status": 409, "error": "File name already exists"}

            """ New Post"""
            new_post = PostNews(user_id=user_id,
                file_name=format_text_for_ascci(file_name)
            )
            db.session.add(new_post)
            db.session.commit()
            return {"status": 200}

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}   