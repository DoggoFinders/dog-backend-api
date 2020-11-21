from flask import Blueprint, render_template

home = Blueprint("home", __name__, url_prefix="/")


@home.route("/")
def get_index():
    return render_template("home/index.html")
