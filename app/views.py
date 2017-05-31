from datetime import datetime, timedelta
from flask import Flask, current_app, jsonify, session, redirect
from flask import render_template, current_app
from flask_user import login_required
from flask.ext.login import current_user
from werkzeug.security import gen_salt
from .models import User, Client
from . import oauth
from . import db
from app.models import User


def set_app_routes(application):
    @application.route('/')
    @login_required
    def hello_world():
        return 'Hello, World!'

    @application.route('/client')
    def client():
        user = current_user()
        if not user:
            return redirect('/')
        item = Client(
            client_id=gen_salt(40),
            client_secret=gen_salt(50),
            _redirect_uris=' '.join([
                'http://localhost:8000/authorized',
                'http://127.0.0.1:8000/authorized',
                'http://127.0.1:8000/authorized',
                'http://127.1:8000/authorized',
            ]),
            _default_scopes='email',
            user_id=user.id,
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(
            client_id=item.client_id,
            client_secret=item.client_secret,
        )

    @application.route('/oauth/token', methods=['GET', 'POST'])
    @oauth.token_handler
    def access_token():
        return None



def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


@oauth.clientgetter
def load_client(client_id):
    from .models import Client
    return Client.query.filter_by(client_id=client_id).first()


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    from .models import Token
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    from .models import Token
    toks = Token.query.filter_by(
        client_id=request.client.client_id,
        user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token['access_token'],
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
        _scopes=token['scope'],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


