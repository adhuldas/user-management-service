import os

from dotenv import load_dotenv

ERROR_COLOR_CODE = "\033[91m"

load_dotenv()


class Environment:
    """
    CLASS WHICH HOLD ENVIRONMENT VARIABLES
    """

    # SETTING TYPE OF LOG WHICH NEED TO PRINTED IN CONSOLE
    LOG_LEVEL = os.getenv("LOG_LEVEL", "LOG_LEVEL")
    LOG_VALUE = {
        "CRITICAL": 50,
        "ERROR": 40,
        "WARNING": 30,
        "INFO": 20,
        "DEBUG": 10,
    }
    # Define colors for different log levels
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": ERROR_COLOR_CODE,  # Red
        "CRITICAL": ERROR_COLOR_CODE,  # Red
        "ENDC": "\033[0m",  # End color
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "JWT_SECRET_KEY")
    # Mongo URI
    MONGO_URI = os.environ.get("MONGO_URI", "MONGO_URI")
    PASSWORD_REGEX = os.getenv(
        "PASSWORD_REGEX",
        "PASSWORD_REGEX",
    )
    EMAIL_REGEX_CHECK = os.getenv(
        "EMAIL_REGEX_CHECK",
        "EMAIL_REGEX_CHECK",
    )
    FERNET_KEY = os.environ.get("FERNET_KEY", "FERNET_KEY")

    # For sending mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT", "MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "MAIL_PASSWORD")
    MAIL_USE_TLS = True
    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "SENDER_EMAIL")

    RECAPTCHA_SECRET_KEY = os.environ.get(
        "RECAPTCHA_SECRET_KEY", "RECAPTCHA_SECRET_KEY"
    )
