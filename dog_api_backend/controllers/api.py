import logging
from collections import defaultdict
from datetime import datetime
from io import BytesIO
from tempfile import TemporaryDirectory

from flask import (Blueprint, abort, current_app, jsonify, render_template,
                   request)
from flask.helpers import make_response, send_file

from ..db import db
from ..models import LostDog, CoatColour, ReportedDog
from ..dog_inference_api import send_dog_image
from ..utils import set_time_in_payload
from geopy import distance

api = Blueprint("api", __name__, url_prefix="/api")

example_dogs = [
    LostDog(owner_email="a@abc.pl", coat_colour=CoatColour.brown, breed="wolf", latitude=54, longitude=23),
    LostDog(owner_email="a2@abc.pl", coat_colour=CoatColour.brown, breed="wolf", latitude=54.001, longitude=23.001)

]


def _create_lost_dog():
    for existing_dog in example_dogs:
        db.session.add(existing_dog)
        db.session.commit()
    return example_dogs[0]


@api.route("/dogs/lost", methods=["POST"])
def submit_lost_dog():
    owner_email = request.form.get("owner_email")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    picture = request.files['image']
    picture = picture.read()

    dog = LostDog(owner_email=owner_email, latitude=latitude, longitude=longitude, picture=picture)
    db.session.add(dog)
    db.session.commit()

    # Infer the breed
    breed = send_dog_image(picture)
    return jsonify({"id": dog.id, "breed": breed.json()})


def _update_dog_info(dog):
    coat_colour = request.form.get("coat_colour")
    breed = request.form.get("breed")

    found = request.form.get("found")
    if found == "True":
        dog.found = True

    if coat_colour:
        dog.coat_colour = coat_colour
    if breed:
        dog.breed = breed
    db.session.commit()


@api.route("/dogs/lost/<int:id>", methods=["POST"])
def update_lost_dog_info(id):
    dog = db.session.query(LostDog).get(id)
    try:
        _update_dog_info(dog)
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"dog": dog.id})


@api.route("/dogs/report", methods=["POST"])
def report_dog():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")

    picture = request.files['image']
    picture = picture.read()

    dog = ReportedDog(latitude=latitude, longitude=longitude, picture=picture)
    db.session.add(dog)
    db.session.commit()

    # Infer the breed
    breed = send_dog_image(picture)
    return jsonify({"id": dog.id, "breed": breed.json()})


@api.route("/dogs/report/<int:id>", methods=["POST"])
def update_reported_dog_info(id):
    dog = db.session.query(ReportedDog).get(id)
    try:
        _update_dog_info(dog)
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"dog": dog.id})


@api.route("/dogs/lost/all", methods=["GET"])
def all_lost_in_neighbourhood():
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    max_distance_in_km = float(request.form.get("max_distance_in_km"))
    coordinates = (latitude, longitude)

    all_lost_dogs = db.session.query(LostDog).all()
    all_lost_dogs_in_neighbourhood = [dog.id for dog in all_lost_dogs
                                      if distance.distance(coordinates, dog.coordinates).km <= max_distance_in_km]
    return jsonify({"lost_dogs": all_lost_dogs_in_neighbourhood})

