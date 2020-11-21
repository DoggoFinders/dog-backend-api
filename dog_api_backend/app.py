import logging
from logging.config import dictConfig
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .controllers.api import api
from .controllers.home import home
from .controllers.auth import oauth, auth
from .db import db, migrate

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)


def _configure_logging(app):
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


def _configure_app(app):
    local_path = Path(__file__).parent.absolute()
    app.config.from_pyfile(local_path / "config.py.example")
    try:
        app.config.from_envvar("DOG_API_CONFIG")
    except Exception as e:
        logging.warning("Could not read config from envvar")


def create_app():
    app = Flask("doggo_finder", template_folder="dog_api_backend/templates")
    CORS(app)
    _configure_app(app)
    _configure_logging(app)

    oauth.init_app(app)
    oauth.register(
        name='github',
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={'scope': 'user:email'},
    )

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(home)

    return app
