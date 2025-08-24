import os
from datetime import timedelta
import datetime as date_time
from dotenv import load_dotenv
from flask_babel import gettext as _

from constants.environment_constants import Environment


load_dotenv()

ERROR_COLOR_CODE = "\033[91m"


class Config(object):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    # For authentication
    ENCRYPTION = True
    # SETTING TYPE OF LOG WHICH NEED TO PRINTED IN CONSOLE
    LOG_LEVEL = Environment.LOG_LEVEL
    LOG_VALUE = Environment.LOG_VALUE
    # Define colors for different log levels
    COLORS = Environment.COLORS
    # This variable is used to prevent injection for username and password
    JWT_SECRET_KEY = Environment.JWT_SECRET_KEY
    # Mongo URI
    MONGO_URI = Environment.MONGO_URI

    PASSWORD_REGEX = Environment.PASSWORD_REGEX
    EMAIL_REGEX_CHECK = Environment.EMAIL_REGEX_CHECK
    FERNET_KEY = Environment.FERNET_KEY

    # For sending mail
    MAIL_SERVER = Environment.MAIL_SERVER
    MAIL_PORT = Environment.MAIL_PORT
    MAIL_USERNAME = Environment.MAIL_USERNAME
    MAIL_PASSWORD = Environment.MAIL_PASSWORD
    MAIL_USE_TLS = Environment.MAIL_USE_TLS
    SENDER_EMAIL = Environment.SENDER_EMAIL

    RECAPTCHA_SECRET_KEY = Environment.RECAPTCHA_SECRET_KEY


class TestingConfig(Config):
    TESTING = True
    ENCRYPTION = True
    INJECT_ENDPOINT = None
    WTF_CSRF_ENABLED = False
    ENCRYPTION = True
    MONGO_URI = Environment.MONGO_URI + "_Test"
