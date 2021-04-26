# -*- coding: utf-8 -*-

import os
from resources.util import generate_secret_key

class Config():
    SECRET_KEY = generate_secret_key()
    CSRF_ENABLED = True
    UPLOAD_FOLDER = UPLOAD_FOLDER = os.path.curdir+os.path.sep+'static'+os.path.sep+'uploads'+os.path.sep

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 8000
    URL_MAIL = f"http://{IP_HOST}:{PORT_HOST}"

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 5000
    URL_MAIL = f"http://{IP_HOST}:{PORT_HOST}"

class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
    IP_HOST = "localhost"
    PORT_HOST = 8080
    URL_MAIL = f"http://{IP_HOST}:{PORT_HOST}"

app_config = {
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig()
}

app_active = os.getenv("FLASK_ENV")
