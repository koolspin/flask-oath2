from datetime import datetime, timedelta
import re
from flask import Flask, current_app, jsonify, session, redirect, request
from flask import render_template, current_app
from flask_user import login_required
from flask_login import current_user
from werkzeug.security import gen_salt
from .models import User, Client, Token
from . import oauth
from . import db
from app.models import User
from app.util_encrypt import UtilEncrypt
from urllib.parse import quote


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

    # @application.route('/oauth/authorize', methods=['GET', 'POST'])
    # @login_required
    # @oauth.authorize_handler
    # def authorize(*args, **kwargs):
    #     if request.method == 'GET':
    #         client_id = kwargs.get('client_id')
    #         client = Client.query.filter_by(client_id=client_id).first()
    #         kwargs['client'] = client
    #         return render_template('oauthorize.html', **kwargs)
    #
    #     confirm = request.form.get('confirm', 'no')
    #     return confirm == 'yes'

    @application.route('/oauth/implicit', methods=['GET', 'POST'])
    @login_required
    def authorize(*args, **kwargs):
        if request.method == 'GET':
            client_id = kwargs.get('client_id')
            if client_id is None:
                client_id = request.args.get('client_id')
                kwargs['client_id'] = client_id
            redirect_uri = kwargs.get('redirect_uri')
            if redirect_uri is None:
                redirect_uri = request.args.get('redirect_uri')
                kwargs['redirect_uri'] = redirect_uri
            state = kwargs.get('state')
            if state is None:
                state = request.args.get('state')
                kwargs['state'] = state
            response_type = kwargs.get('response_type')
            if response_type is None:
                response_type = request.args.get('response_type')
                kwargs['response_type'] = response_type
            xid = int(current_user.get_id())
            client = Client.query.filter_by(client_id=client_id).first()
            user = User.query.filter_by(id=xid).first()
            kwargs['client'] = client
            kwargs['user'] = user
            return render_template('oauthorize.html', **kwargs)
        else:
            client_id = request.form.get('client_id')
            redirect_uri = request.form.get('redirect_uri')
            state = request.form.get('state')
            response_type = request.form.get('response_type')
            ok = validate_implicit_request(client_id, redirect_uri)
            if ok:
                xid = int(current_user.get_id())
                confirm = request.form.get('confirm', 'no')
                token = save_token2(client_id, xid)
                if confirm == 'yes':
                    full_uri = '{0}#access_token={1}&token_type=bearer&state={2}'.format(redirect_uri, quote(token), state)
                    print(full_uri)
                    return redirect(full_uri)
            else:
                # TODO: Should redirect to an error page
                return redirect('/')


def validate_implicit_request(client_id, redirect_uri):
    if client_id != 'google_assistant':
        return False
    if re.match('https://oauth-redirect.googleusercontent.com/r/.*', redirect_uri) is None:
        return False
    return True


def save_token2(client_id, user_id):
    toks = Token.query.filter_by(
        client_id=client_id,
        user_id=user_id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    # 100 years in seconds
    expires_in = 60 * 60 * 24 * 365 * 100
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    acc_token = UtilEncrypt.generate_random_string()
    ref_token = UtilEncrypt.generate_random_string()

    tok = Token(
        access_token=acc_token,
        refresh_token=ref_token,
        token_type='bearer',
        _scopes='',
        expires=expires,
        client_id=client_id,
        user_id=user_id
    )
    db.session.add(tok)
    db.session.commit()
    return acc_token


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


