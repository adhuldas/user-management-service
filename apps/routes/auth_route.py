

import logging
from flask import Blueprint, jsonify, request
from apps.decorators.fernet_decorators import decryptor
from apps.decorators.validation_decorators import content_type_check, require_fields
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