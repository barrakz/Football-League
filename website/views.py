from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required

from .models import Team, Player, Rating
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    teams = Team.query.all()
    return render_template("home.html", teams=teams, user=current_user)


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

    return render_template("team_players.html", team=team, players=players, average_rating=Player.average_rating, user=current_user)



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


@views.route("/addplayer", methods=["GET", "POST"])
@login_required
def add_player():
    if request.method == 'POST':
        name = request.form["name"]
        team_id = request.form["team"]
        new_player = Player(name=name, team_id=team_id)
        db.session.add(new_player)
        db.session.commit()
        return redirect(url_for("views.home"))

    teams = Team.query.all()
    return render_template("add_player.html", teams=teams, user=current_user)


@views.route("/rateplayer/<int:player_id>", methods=["GET", "POST"])
@login_required
def rate_player(player_id):
    player = Player.query.get_or_404(player_id)

    existing_rating = Rating.query.filter_by(player_id=player_id, user_id=current_user.id).first()

    if existing_rating:
        flash("You have already rated this player.", "danger")
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
    return render_template('player_details.html', player=player, user=current_user)
