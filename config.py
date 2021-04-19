# -*- coding: utf-8 -*-

import os

class Config():
    SECRET_KEY = "\xbc\xe6ah2\xb0\xc8Z\x1d\xdf'f<\xfa&\xc1\x9eVz;\xad$I\xecW\x9eW\xbe\xbe\xc8\xcb\xb7"
    CSRF_ENABLED = True
    UPLOAD_FOLDER = "posts"

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
