from functools import wraps
import logging

from flask import jsonify, request
from constants.common_constants import CommonConstant
from constants.response_constants import ResponseConstants


def require_fields(*field_names):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = None
            data = (
                request.form.to_dict()
                if request.form
                else (request.json or request.args.to_dict())
            )
            if request.is_json and "data" in request.json:
                data = request.decrypted_data
            missing_fields = set(field_names) - set(data)
            if missing_fields:
                return (
                    jsonify(
                        {
                            "error": f"Missing required fields: {', '.join(missing_fields)}"
                        }
                    ),
                    400,
                )
            if not empty_field_check(
                data,
                list(field_names),
            ):
                return jsonify(message=CommonConstant.NOT_ALLOWED), 400
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def content_type_check(supported_types):
    def decorator(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            unsupported = (request.is_json and supported_types != "json") or (
                request.form and supported_types != "form"
            )
            if unsupported:
                return (
                    jsonify(
                        {"error": ResponseConstants.UNSUPPORTED_MEDIA_TYPE}
                    ),
                    415,
                )  # Unsupported Media Type

            return f(*args, **kwargs)

        return wrapped_function

    return decorator


def empty_field_check(dictionary, keys):
    try:
        for key in keys:
            if key in dictionary and not dictionary.get(key):
                return False
        return True
    except Exception as exc:
        logging.error(f"error occured in fucntion empty_field_check:{exc}")
        return False