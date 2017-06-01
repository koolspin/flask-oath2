import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '16846324-02b7-11e6-a62a-57ca2a71f28f'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask User stuff
    USER_APP_NAME = 'Flask Starter'
    USER_ENABLE_CONFIRM_EMAIL = False
    USER_ENABLE_LOGIN_WITHOUT_CONFIRM_EMAIL = True
    USER_ENABLE_EMAIL = True
    USER_ENABLE_USERNAME = False
    USER_ENABLE_CHANGE_USERNAME = False

    # MAIL_USERNAME = ''
    # MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = '"do-not-reply" <noreply@email.com>'
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ''
    MAIL_PORT = 25
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False

    OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 3600

    @staticmethod
    def init_app(app):
        pass

class ManageConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///{0}'.format(os.path.join(os.getcwd(), 'flask_oauth.db'))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///{0}'.format(os.path.join('/var/db', 'flask_oauth_dev.db'))

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///{0}'.format(os.path.join('/var/db', 'flask_oauth_prod.db'))

config = {
    'manage': ManageConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
