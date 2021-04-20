# -*- coding: utf-8 -*-

import os
from config import app_config, app_active
from flask import Flask, request, render_template, flash

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
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            if 'file_post' not in request.files:
                flash("There is no file in form!")
                return render_template('index.html', notify="danger")

            post = request.files['file_post']
            path = os.path.join(app.config['UPLOAD_FOLDER'], post.filename)
            post.save(path)
            flash("Archive upload sucessfully")

            return render_template("index.html", notify="primary")

        return render_template("index.html")

    return app
