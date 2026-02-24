from flask import Blueprint, render_template
from flask_login import login_required

module = Blueprint("main", __name__)


@module.route("/")
def index():
    return render_template("main/index.html")
