import logging
from flask import jsonify
from apps.database.models import UsersDb
from apps.models.singup_model import SignupModel
from apps.utils.token_utils import create_dynamic_token
from apps.validators.auth_validators import AuthValidator
from config import Config
from constants.response_constants import ResponseConstants


class SignupHelper:
    """ """

    @staticmethod
    def user_singup_helper(request_content):
        """ """
        try:
            # Validate the incoming request data using Pydantic model
            request_data = SignupModel(**request_content)
            # Apply rate-limiting check for signup requests
            rate_limited = AuthValidator.rating_limiting_email(
                request_data.email, "signup", 5
            )
            if rate_limited:
                return (
                    jsonify(message=ResponseConstants.MAXI_LIMIT_EXCEEDED),
                    429,
                )
            # Check if the user already exists in the database
            existing_user = UsersDb().find(
                {
                    "$or": [
                        {"username": request_data.email},  # exact match
                        {"username": request_data.email.lower()},  # lowercase match
                    ]
                }
            )
            if existing_user:
                return (
                    jsonify(message=AuthValidator.user_exist_check_mail()),
                    401,
                )
            # Generate 2FA token and slug ID
            token, slug_id = create_dynamic_token(
                request_data.email, request_data.user_type, "signup"
            )
            if not token:
                return (
                    jsonify(message=ResponseConstants.EMAIL_ID_NOT_VALID),
                    403,
                )
            # TODO: Need to implement a celery and email sending for singup
            # for time being details for registering is return with api response
            URL = Config.BASE_URL + "register"
            response = {
                "email": request_data.email,
                "token": token,
                "url": URL,
                "user_type": request_data.user_type,
                "slug": slug_id,
            }

            return jsonify(response), 200

        except Exception as exc:
            logging.error(f"Error occured in function user_singup_helper:{exc}")
            return (
                jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                500,
            )
