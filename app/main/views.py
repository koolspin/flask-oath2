from flask import render_template, current_app
from flask.ext.login import current_user
from flask_user import login_required
from app.models import User
from . import main

# Routing goes here
# @main.route('/')
# @login_required
# def cs_list():
#     xid = int(current_user.get_id())
#     cs = ControlSystem.query.filter_by(user_id=xid).order_by(ControlSystem.cs_name).all()
#     return render_template('cs_list.html', cs_collection=cs)

def is_authenticated(auth):
    """
    Performs HTTP basic authentication for the REST calls that need it
    :param auth: Authentication object from the HTTP request
    :return: True if authentication succeeds, False if not
    """
    if auth is None:
        return False, None
    user = User.query.filter_by(email=auth.username).first()
    user_manager = current_app.user_manager
    return user_manager.verify_password(auth.password, user), user.get_id()

