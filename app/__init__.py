import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object or DevelopmentConfig)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # init
    db.init_app(app)
    migrate.init_app(app, db)

    # register
    from .api import api_bp
    from .api.books import books_bp
    from .main import main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(books_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    return app
