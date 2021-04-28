# -*- coding: utf-8 -*-

from app import db
from datetime import datetime
from flask_login import UserMixin

class UserDB(UserMixin, db.Model):
    __tablename__ =  "userdb"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    alias = db.Column(db.String(100), nullable=True)
