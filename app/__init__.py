# -*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown

db = SQLAlchemy()
login_manager = LoginManager()
pagedown = PageDown()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    pagedown.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    '''
    载入一个名为'admin'的蓝图作为后台管理模块
    '''

    return app