from flask_login import UserMixin
from sqlalchemy import func

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
