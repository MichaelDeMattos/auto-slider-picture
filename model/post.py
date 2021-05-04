# -*- coding: utf-8 -*-

from app import db
from datetime import datetime

class PostNewsDB(db.Model):
    __tablename__ = "postnewsdb"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdb.id'))
    file_name = db.Column(db.String(500), nullable=False, unique=True)
    description = db.Column(db.String(500))
    type_file = db.Column(db.String(256))
    sleep = db.Column(db.Integer, default=30)
    screen = db.Column(db.Integer, default=1)
    create_date = db.Column(db.DateTime, default=datetime.now())
    
    user = db.relationship("UserDB")

class PostNewsLogDB(db.Model):
    __tablename__ = "postnewslogdb"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdb.id'))
    file_name = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.DateTime)
    deleted_date = db.Column(db.DateTime, default=datetime.now())
    
    user = db.relationship("UserDB")
