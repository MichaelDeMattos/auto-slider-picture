# -*- coding: utf-8 -*-

from app import db
from datetime import datetime

class PostNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    file_name = db.Column(db.String(500), nullable=False)
