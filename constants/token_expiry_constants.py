from datetime import timedelta
import datetime as date_time


class TokenExpireConstant:
    """
    CLASS WHICH HOLD TOKEN EXPIRE DEFAULT CONFIGURATION
    """

    # Setting JWT token expiry
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

    # Setting refresh token expiry
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=20)

    # Setting forgot password token expiry
    FORGOT_PASSWORD_TOKEN_EXPIRES = date_time.timedelta(hours=2)

    # Setting signup token expiry
    SIGNUP_TOKEN_EXPIRES = date_time.timedelta(minutes=10)
