import logging
from logging.config import dictConfig
from pathlib import Path

from flask import Flask

from .controllers.api import api
from .controllers.home import home
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
    app = Flask("attestation", template_folder="dog_api_backend/templates")
    _configure_app(app)
    _configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(home)

    return app
