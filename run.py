# -*- coding: utf-8 -*- 

import sys
from app import create_app, db
from config import app_active, app_config

config = app_config[app_active]
config.APP = create_app(app_active)
db.create_all(app=create_app(app_active))

if __name__  == "__main__":
    config.APP.run(host=config.IP_HOST, port=config.PORT_HOST)
    