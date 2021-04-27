# -*- coding: utf-8 -*-

from app import db
from datetime import datetime

class PostNews(db.Model):
    __tablename__ = "postnews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_name = db.Column(db.String(500), nullable=False, unique=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    
    user = db.relationship("User")

class PostNewsLog(db.Model):
    __tablename__ = "postnewslog"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_name = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime, default=datetime.now())
    
    user = db.relationship("User")
