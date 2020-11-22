import enum
from datetime import datetime
from flask_login import UserMixin

from .db import db


class CoatColour(enum.Enum):
    brown = "brown",
    red = "red",
    gold = "gold",
    cream = "cream",
    black = "black",
    grey = "grey",
    white = "white",
    other = "other"


class LostDog(db.Model):
    __tablename__ = "lost_dog"

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    owner_email = db.Column(db.String(80))
    found = db.Column(db.Boolean, default=False)
    coat_colour = db.Column(db.Enum(CoatColour))
    breed = db.Column(db.String(80))
    picture = db.Column(db.LargeBinary())
    latitude = db.Column(db.Numeric(10, 6))
    longitude = db.Column(db.Numeric(10, 6))
    details = db.Column(db.String(250))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def coordinates(self):
        return self.latitude, self.longitude

    def __str__(self):
        return f"""<LostDog owner:{self.owner_email}, breed:{self.breed} >"""


class ReportedDog(db.Model):
    __tablename__ = "reported_dog"

    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    coat_colour = db.Column(db.Enum(CoatColour))
    breed = db.Column(db.String(80))
    picture = db.Column(db.LargeBinary())
    latitude = db.Column(db.Numeric(10, 6))
    longitude = db.Column(db.Numeric(10, 6))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f"""<ReportedDog owner:{self.owner_email}, breed:{self.breed} >"""


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), autoincrement=True, primary_key=True)
    email = db.Column(db.String(256), nullable=False)
    gh_user_id = db.Column(db.Integer(), nullable=False)
