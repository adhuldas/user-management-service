from flask_babel import gettext as _


class ResponseConstants:
    """
    CLASS WHICH HOLD API RETURN RESPONSE MESSAGE AS CONSTANT
    """

    INTERNAL_ERROR_MESSAGE = "Something went wrong, Please try again"
    UNSUPPORTED_MEDIA_TYPE = "Unsupported Media Type"
    UNPROCESSABLE_ENTITY = "Unprocessable Entity"
    MAXI_LIMIT_EXCEEDED ="Maximum try exceeded,Please try after 1 hour"
    EMAIL_ID_NOT_VALID = "Provide a valid email id"
