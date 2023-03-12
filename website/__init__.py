from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
bcrypt = Bcrypt()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "helloplayer"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Team, Player, Rating

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    admin = Admin(app)
    migrate = Migrate(app, db)
    manager = Manager(app)

    manager.add_command("db", MigrateCommand)

    admin.add_view(ModelView(Team, db.session))
    admin.add_view(ModelView(Player, db.session))
    admin.add_view(ModelView(Rating, db.session))
    admin.add_view(ModelView(User, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")
