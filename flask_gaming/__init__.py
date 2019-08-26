from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
config = None


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    from . import models
    Migrate(app, db)


def register_blueprints(app):
    from flask_gaming.registration import registration
    from flask_gaming.auth import auth
    from flask_gaming.game import game
    from flask_gaming.payment import payment

    app.register_blueprint(registration, url_prefix='/registration')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(game, url_prefix='/game')
    app.register_blueprint(payment, url_prefix='/payment')
