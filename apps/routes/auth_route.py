

import logging
from flask import Blueprint, jsonify, request
from apps.decorators.fernet_decorators import decryptor
from apps.decorators.validation_decorators import content_type_check, require_fields
from apps.helpers.route_helpers.auth_route_helpers.register_helper import RegisterHelper
from apps.helpers.route_helpers.auth_route_helpers.singup_helper import SignupHelper
from constants.response_constants import ResponseConstants


auth_module = Blueprint("auth_module", __name__, url_prefix="/auth")



@auth_module.route("/signup", methods=["POST"])
@content_type_check("json")  # Require JSON content type
@decryptor
@require_fields("email")
def signup():
    """
    New user signup process
    Mandatory parameter is your email

    PROCESS INVOLVED
        When the email is given a token will be created and stored it to mongodb
        Mail with the registration link and token from db is sent to provided mail id
        Then a confirmation page will be shown saying that a mail has been sent to your email
    """
    try:
        response, status_code = SignupHelper.user_singup_helper(
            request.decrypted_data
        )

        return response, status_code

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function signin: {exc}")

        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
    

@auth_module.route("/register", methods=["POST"])
@content_type_check("json")
@decryptor
@require_fields(
    "username",
    "firstname",
    "lastname",
    "timezone",
    "password",
    "phone_number",
    "country_code",
    "token",
    "slug",
)
def add_user():
    """
    Register new user
    Mandatory fields are username, password, firstname, lastname, timezone, token

    PROCESS
        When we give all mandatory parameters it will get updated in the emapty dict "user_details"
        Password hash is generated for the password that user give
        Checks if token is in db or not
        Verify created_token embedded mail and fetched token embedded email is same
        Get the user list to check if user is an existing user
        If not existing user, new user is registered
    """
    try:
        response, status_code = RegisterHelper.register_user_helper(
            request.decrypted_data
        )

        return response, status_code

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function add_user: {exc}")

        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500