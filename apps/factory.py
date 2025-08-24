"""initialization of apps"""

import logging
import sys
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_cors import CORS
from config import Config
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect

jwt = JWTManager()
mongo = PyMongo()
mail = Mail()
cors = CORS()
babel = Babel()
csrf = CSRFProtect()


def create_app(config_type="config.Config"):
    """Create flask app object"""

    app = Flask(  # NOSONAR S4502
        __name__, static_folder="static", static_url_path="/identity/assets"
    )  # NOSONAR S4502


    # Setting configuration for the project
    app.config.from_object(config_type)
    # Adding log level
    # Setup logging
    if Config.DEBUG:
        logger = logging.getLogger()
        logger.setLevel(Config.LOG_VALUE.get(Config.LOG_LEVEL))
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(Config.LOG_VALUE.get(Config.LOG_LEVEL))
        formatter = ColoredFormatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    # initializing jwt
    jwt.init_app(app)

    csrf.init_app(app)

    cors.init_app(app)
    # initialize mail
    mail.init_app(app)
    # initialize mongo app
    mongo.init_app(app)

    # # Register blueprint
    from apps.routes.auth_route import (
        auth_module,
    )  # pylint:disable=import-outside-toplevel

    app.register_blueprint(auth_module)


    return app


# Custom formatter for adding colors
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        if levelname in Config.COLORS:
            record.levelname = (
                Config.COLORS[levelname] + levelname + Config.COLORS["ENDC"]
            )
            record.msg = (
                Config.COLORS[levelname]
                + str(record.msg)
                + Config.COLORS["ENDC"]
            )
        return logging.Formatter.format(self, record)