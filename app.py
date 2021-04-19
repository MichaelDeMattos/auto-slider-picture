# -*- coding: utf-8 -*-

from config import app_config, app_active 
from flask import Flask, request, render_template

# Application
app = Flask(__name__, template_folder="templates", static_folder="static")
config = app_config[app_active]

""" This function create app flask """
def create_app(config_name):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config app
    app.secret_key = config.SECRET_KEY
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")

    @app.route("/")
    def index():
        return render_template("index.html")
    
    return app