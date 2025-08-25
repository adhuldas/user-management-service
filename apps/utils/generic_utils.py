


import logging

from constants.common_constants import CommonConstant


def error_message(exc):
    """
    FUNCTION TO RETURN EXCEPTION MESSAGE

    Args:
        exc (Exception): Exception Module
    """

    try:
        return (
            exc.errors()[0]["msg"]
            .split(CommonConstant.VALUE_ERROR)[-1]
            .strip()
        )
    except Exception as exc:
        logging.error(f"Error occurred in error_message: {exc}")
        return "ERRROR"
