from flask_login import UserMixin
from sqlalchemy import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    players = db.relationship("Player", backref="team", lazy=True)

    def __repr__(self):
        return f"Team('{self.name}')"


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    ratings = db.relationship("Rating", backref="player", lazy=True)

    def __repr__(self):
        return f"Player('{self.name}', '{self.team.name}')"

    def average_rating(self):
        if self.ratings:
            return round(sum(r.rating for r in self.ratings) / len(self.ratings), 1)
        else:
            return 0


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


    def __repr__(self):
        return f"Rating('{self.rating}', '{self.comment}')"
