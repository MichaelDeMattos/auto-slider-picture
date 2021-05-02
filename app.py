# -*- coding: utf-8 -*-

import os
import magic
import shutil
from datetime import datetime
from config import app_config, app_active
from flask import Flask, request, render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand   
from flask_script import Manager

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
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@host:port/database"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
 
    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    # Models
    from model.user import UserDB
    from model.post import PostNewsDB

    # Resources
    from resources.dowload import ControllerDownload
    from resources.util import format_datetime, format_text_for_ascci
    from resources.user import ControllerUser
    from resources.post import ControllerPostNews
    
    @login_manager.user_loader
    def load_user(cod_user):
        return UserDB.query.get(int(cod_user))

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
        alias_name = request.form.get('inp_alias_name')
        password = request.form.get('inp_password')

        user = ControllerUser().get_user_by_email(email=email)
        if user:  
            flash('Email address already exists')
            return render_template('singin.html', notify='danger')

        new_user = ControllerUser().new_user(email=email,
                                             name=name,
                                             alias_name=alias_name,
                                             password=generate_password_hash(password, method='sha256'))
        if new_user["status"] == 500:
            flash('Error in include new user!!!')
            return render_template('singin.html', notify='danger')
        
        return redirect(url_for('login'))

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/login", methods=["POST"])
    def login_post():
        email = request.form.get("inp_email")
        password = request.form.get("inp_password")
        user = ControllerUser().get_user_by_email(email=email)

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return render_template('login.html', notify='danger')
            
        login_user(user, remember=False)
        return redirect(url_for('admin'))

    @app.route("/admin")
    @login_required
    def admin():
        id_user_session = session["_user_id"]
        posts = ControllerPostNews().get_posts()
        _files = []
        for row in posts:
            _files.append({
                "id": row.id, 
                "file_name": row.file_name, 
                "create_date": format_datetime(row.create_date),
                "user_name": ControllerUser().get_user_by_id(row.user_id).split()[0],
            })
        return render_template(
            "admin.html", 
            user=ControllerUser().get_user_by_id(id_user_session),
            files=_files)
    
    @app.route("/admin", methods=["POST"])
    def admin_post():
        file_name = request.form["file_name"]
        user_id = session["_user_id"]

        if not file_name:
            return "Name file if not exists", 404

        file_path = os.path.join(app.config["UPLOAD_FOLDER"] + file_name)
        delete = ControllerPostNews().delete_post(file_name, user_id)
        """ Backup file deleted """
        shutil.copy(file_path, config.BACKUP_FOLDER)
        """ Remove file this dir uploads """
        os.remove(file_path)
        
        if delete["status"] == 500:
            return "Name file if not exists", 404
        
        if delete["status"] == 200:
            return "\nFile deleted sucessfully!!!", 200

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route("/view", methods=["GET"])
    def view():
        # ControllerDownload().get_download_img()
        return render_template("view.html", 
            files=ControllerDownload().scrapy_dir_uploads(),
            refresh_time=len(ControllerDownload().scrapy_dir_uploads() * 35)
        )

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
            description = request.form.get('inp_file_description')
            sleep = int(request.form.get('inp_sleep_slide'))
            screen = request.form.get('inp_screen')
            """ Save file in path /uploads """
            path = os.path.join(app.config['UPLOAD_FOLDER'],
                format_text_for_ascci(post.filename).replace(" ", "_")
            )
            post.save(path)
            
            new_post = ControllerPostNews().new_post(
                user_id=session["_user_id"],
                file_name=post.filename,
                description=description,
                _type=magic.from_file(path, mime=True),
                sleep=sleep,
                screen=screen
            )

            if new_post["status"] == 409 or new_post["status"] == 500:
                flash(new_post["error"])
                return render_template("posts.html", notify="danger") 

            """ Renderer response """ 
            flash("Archive upload sucessfully")
            return render_template("posts.html", notify="primary")

        return render_template("posts.html")

    return app
