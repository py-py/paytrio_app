from flask import Flask
# TODO: block for deploying on Heroku
# from app.log import setup_logging
from config import config


def create_app(config_name):
    # Flask app
    app = Flask(__name__)

    # config app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # TODO: block for deploying on Heroku
    # setup_logging(app)

    # blueprints app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
