# -*- coding: utf-8 -*- 

import sys
from app import create_app, db
from config import app_active, app_config

app = app_config[app_active]
app.APP = create_app(app_active)

if __name__  == "__main__":
    app.APP.run(host=app.IP_HOST, port=app.PORT_HOST)
    