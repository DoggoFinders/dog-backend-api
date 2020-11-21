import logging
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from tempfile import TemporaryDirectory

from flask import (Blueprint, abort, current_app, jsonify, render_template,
                   request)
from flask.helpers import make_response, send_file

from ..db import db
from ..models import LostDog
from ..dog_inference_api import send_dog_image
from ..utils import set_time_in_payload

api = Blueprint("api", __name__, url_prefix="/api")


def _create_lost_dog():
    existing_dog = LostDog()
    db.session.add(existing_dog)
    db.session.commit()
    return existing_dog


@api.route("/dogs/lost", methods=["GET", "POST"])
def submit_lost_dog():
    dog = _create_lost_dog()
    return {"hello": dog.id}
