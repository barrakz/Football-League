from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user, login_required

from .models import Team
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return "Hello"


@views.route("/addteam", methods=["GET", "POST"])
@login_required
def add_team():
    if request.method == 'POST':
        name = request.form["name"]
        new_team = Team(name=name)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("views.home"))
    return render_template("add_team.html", user=current_user)
