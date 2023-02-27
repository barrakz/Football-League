from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return "Hello"



