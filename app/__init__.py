import os
from flask import Flask
from flasgger import Swagger
from .config import DevelopmentConfig
from .extensions import db, migrate


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
    Swagger(app)

    # register
    from .api import api_bp
    from .api.books import books_bp
    from .api.exchange import exchange_bp
    from .api.search import search_bp
    from .main import main_bp

    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(books_bp, url_prefix='/api')
    app.register_blueprint(exchange_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    return app
