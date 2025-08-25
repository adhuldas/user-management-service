

import logging
from flask import jsonify
from pydantic import ValidationError
from apps.database.models import UsersDb
from apps.database_query_handler.aggregate_queries.user_details_aggreagtion import UserDetailsAggregation
from apps.helpers.token_helpers.create_token_helper import CreateToken
from apps.models.signin_models import SignIn
from apps.utils.generic_utils import error_message
from apps.validators.auth_validators import AuthValidator
from werkzeug.security import check_password_hash

from constants.response_constants import ResponseConstants


class SigninHelper:
    """ 
    
    """
    @staticmethod
    def signin_api_helper(request_content):
        """
        Handles user sign-in flow including:
        - Validating the sign-in payload
        - Rate limiting for 2FA-enabled requests
        - User credential verification
        - Admin permission checks based on location
        - Token creation (JWT, MQTT)
        - Triggering Two-Factor Authentication if required

        Args:
            request_content (dict): Incoming request payload from JSON body.

        Returns:
            tuple: A tuple containing a Flask response and HTTP status code.
        """
        try:
            # Validate request using the SignIn Pydantic schema
            request_data = SignIn(**request_content)
            # Fetch user details using aggregation pipeline
            query = UserDetailsAggregation.get_user_details(request_data.username)
            _is_user_exists = UsersDb().aggregate(query)
            # Validate user data (check if user exists, not blocked, etc.)
            is_valid, response = AuthValidator.validate_user(_is_user_exists)
            if not is_valid:
                return response
            # Validate password
            _hashed_password = _is_user_exists[0].get("password")
            userauth = check_password_hash(
                _hashed_password, request_data.password
            )
            if not userauth:
                return jsonify(message=ResponseConstants.SIGN_IN_MESSAGE), 401
            # Prepare JWT claims from user info
            additional_claims = AuthValidator.prepare_additional_claims(
                _is_user_exists
            )
            if not additional_claims:
                return (
                    jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                    500,
                )
            location = getattr(request_data, "location", None)
            # Non-2FA login flow (for devices, mobile apps, etc.)
            access_token, refresh_token = (
                CreateToken.create_access_refresh_token(
                    additional_claims,
                    bool(location in ["device", "mobile_app"]),
                )
            )
            return (
                jsonify(
                    access_token=access_token, refresh_token=refresh_token
                ),
                200,
            )

        except ValidationError as e:
            # Handle schema validation errors (missing fields, wrong types, etc.)
            first_error_msg = error_message(e)
            return jsonify(message=first_error_msg), 400

        except Exception as exc:
            # Handle unexpected errors with logging and generic error message
            logging.error(f"Error in signin_api_helper: {exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500