"""
@File  : __init__.py
@Author: Zhourj
@Date  : 2019/12/26
@Desc  :
"""

__author__ = 'Zhourj'

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db
from app.models.user import User

login_manager = LoginManager()
mail = Mail()


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录'
    mail.init_app(app)
    with app.app_context():
        db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
