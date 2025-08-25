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
    RESTRICTED_ACCESS_MESSAGE = "Restricted Access"
    PASSWORD_FORMAT_MESSAGE = "Password should be at least 8 characters which contains at least one lowercase,one uppercase,one digit and at least one character from the set @#&%!~`$^_*"
    BAD_REQUEST = "Bad request, not valid request"
