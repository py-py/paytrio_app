import logging
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    handler = RotatingFileHandler('./log/paytrio_rotated.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)


# TODO: block for deploying on Heroku
#setup_logging(app)
