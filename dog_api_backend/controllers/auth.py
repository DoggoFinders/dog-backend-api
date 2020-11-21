from functools import wraps

from flask import Blueprint, url_for, session, request, g
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import redirect

from dog_api_backend.db import db
from dog_api_backend.models import User

oauth = OAuth()
github = oauth.register('github')

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/login')
def login():
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)


@auth.route('/callback')
def callback():
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('user').json()

    session['user_id'] = resp['id']
    session['email'] = resp['email']
    session['token'] = token['access_token']
    existing_user = User.query.filter(User.email == session['email']).first()
    if not existing_user:
        new_user = User(email=session['email'], gh_user_id=session['user_id'])
        db.session.add(new_user)
        db.session.commit()
    # do something with the token and profile
    return redirect('/')


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not session.get("user_id"):
            return redirect(url_for('auth.login'))
        # get user via some ORM system
        user = User.query.filter(User.email == session['email']).first()
        # make user available down the pipeline via flask.g
        g.user = user
        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap


@auth.errorhandler(403)
def forbidden_403(exception):
    return 'No hotdogs for you!', 403
