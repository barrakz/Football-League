from datetime import datetime, timedelta

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import desc

from .models import Team, Player, Rating
from . import db
from .utils import admin_required


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    teams = Team.query.all()
    top_players = Player.query.all()
    top_players = sorted(top_players, key=lambda x: x.average_rating(), reverse=True)[:10]
    return render_template("home.html", teams=teams, user=current_user, top_players=top_players)


@views.route("/team_players/<int:team_id>")
@login_required
def team_players(team_id):
    team = Team.query.get_or_404(team_id)
    players = Player.query.filter_by(team_id=team_id).all()

    # for player in players:
    #     if player.ratings:
    #         average_rating = sum([rating.rating for rating in player.ratings]) / len(player.ratings)
    #         player.average_rating = average_rating
    #     else:
    #         player.average_rating = None

    return render_template("team_players.html", team=team, players=players, average_rating=Player.average_rating,
                           user=current_user)


@views.route("/addteam", methods=["GET", "POST"])
@login_required
@admin_required
def add_team():
    if request.method == 'POST':
        name = request.form["name"]
        new_team = Team(name=name)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for("views.admin_edit"))
    return render_template("add_team.html", user=current_user)


@views.route("/addplayer", methods=["GET", "POST"])
@login_required
@admin_required
def add_player():
    if request.method == 'POST':
        name = request.form["name"]
        team_id = request.form["team"]
        new_player = Player(name=name, team_id=team_id)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("views.admin_edit"))

    teams = Team.query.all()
    return render_template("add_player.html", teams=teams, user=current_user)


@views.route("/rateplayer/<int:player_id>", methods=["GET", "POST"])
@login_required
def rate_player(player_id):
    player = Player.query.get_or_404(player_id)

    now = datetime.utcnow()

    last_rating = Rating.query.filter_by(player_id=player_id, user_id=current_user.id).order_by(
        Rating.date_created.desc()).first()
    if last_rating and now < last_rating.date_created + timedelta(hours=1):
        time_remaining = (last_rating.date_created + timedelta(hours=1) - now).seconds // 60
        flash(f"You've already rated this player within the last hour. Please try again in {time_remaining} minutes.",
              "danger")
        return redirect(url_for("views.player_details", player_id=player_id))

    if request.method == 'POST':
        rating = request.form["rating"]
        comment = request.form["comment"]
        new_rating = Rating(rating=rating, comment=comment, player_id=player.id, user_id=current_user.id)
        db.session.add(new_rating)
        db.session.commit()
        flash('Rating added successfully!', 'success')

        return redirect(url_for("views.player_details", player_id=player_id))

    return render_template("rate_player.html", player=player, user=current_user)


@views.route('/player/<int:player_id>')
def player_details(player_id):
    player = Player.query.get_or_404(player_id)

    return render_template('player_details.html', player=player, user=current_user, username=current_user.username)


@views.route('/adminedit')
@login_required
@admin_required
def admin_edit():

    return render_template("adminedit.html", user=current_user)
