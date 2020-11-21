from flask import Blueprint, url_for
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import redirect

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
    resp = oauth.github.get('account/verify_credentials.json')
    profile = resp.json()
    # do something with the token and profile
    return redirect('/')