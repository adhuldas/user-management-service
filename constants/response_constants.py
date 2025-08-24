from flask_babel import gettext as _


class ResponseConstants:
    """
    CLASS WHICH HOLD API RETURN RESPONSE MESSAGE AS CONSTANT
    """

    INTERNAL_ERROR_MESSAGE = "Something went wrong, Please try again"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported Media Type"
    UNPROCESSABLE_ENTITY = "Unprocessable Entity"
