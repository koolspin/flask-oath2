from flask import Flask, current_app, jsonify, session, redirect
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask_oauthlib.provider import OAuth2Provider
from flask.ext.user.forms import RegisterForm
from config import config

mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()
oauth = OAuth2Provider()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    from .models import User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

    return app


class MyRegisterForm(RegisterForm):

    def validate(self):
        if not super().validate():
            return False

        emailval = self.email.data
        if not emailval.endswith('@domain.com'):
            self.email.errors.append('You must use a domain.com email address')
            return False

        return True

