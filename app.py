# -*- coding: utf-8 -*-

import os
from config import app_config, app_active
from flask import Flask, request, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# DataBase
db = SQLAlchemy()

# Application
app = Flask(__name__, template_folder="templates", static_folder="static")

# Config
config = app_config[app_active]

""" This function create app flask """
def create_app(config_name):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config app
    app.secret_key = config.SECRET_KEY
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py")
    app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    
    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    # Models
    from model.user import User
    from model.post import PostNews
    
    @login_manager.user_loader
    def load_user(cod_user):
        return User.query.get(int(cod_user))

    @app.route("/", methods=["GET"])
    def index():
        return redirect(url_for('view'))

    @app.route("/singin")
    def singin():
        return render_template("singin.html")
    
    @app.route("/singin", methods=["POST"])
    def singin_post():
        email = request.form.get('inp_email')
        name = request.form.get('inp_name')
        password = request.form.get('inp_password')

        user = User.query.filter_by(email=email).first()
        if user:  
            flash('Email address already exists')
            return redirect(url_for('login'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login_post():
        email = request.form.get("inp_email")
        password = request.form.get("inp_password")
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
            
        login_user(user, remember=False)
        return redirect(url_for('index'))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route("/view", methods=["GET"])
    def view():
        return render_template("index.html")

    @app.route("/push_post")
    @login_required
    def push():
        return render_template("posts.html")

    @app.route("/push_post", methods=["POST"])
    @login_required
    def push_post():
        if request.method == "POST":
            if 'file_post' not in request.files:
                flash("There is no file in form!")
                return render_template('posts.html', notify="danger")

            post = request.files['file_post']

            """ Register new Post file """
            _user_id = session["_user_id"]
            _filename = post.filename.replace(" ", "_")
            new_post = PostNews(user_id=_user_id, file_name=_filename)
            db.session.add(new_post)
            db.session.commit()        

            """ Save file in path /uploads """
            path = os.path.join(app.config['UPLOAD_FOLDER'], post.filename)
            post.save(path)

            """ Renderer response """ 
            flash("Archive upload sucessfully")
            return render_template("posts.html", notify="primary")

        return render_template("posts.html")

    return app
