from flask import Flask, current_app
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask_user import UserManager, SQLAlchemyAdapter
from flask.ext.user.forms import RegisterForm
from config import config

mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    from .models import User
    db_adapter = SQLAlchemyAdapter(db, User)
    user_manager = UserManager(db_adapter, app, register_form=MyRegisterForm)

    # attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

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

