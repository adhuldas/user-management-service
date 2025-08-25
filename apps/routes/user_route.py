

import logging
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from apps.decorators.fernet_decorators import encryptor
from apps.decorators.validation_decorators import user_active_check
from apps.helpers.route_helpers.user_route_helpers.user_profile_helper import UserprofileHelper
from constants.response_constants import ResponseConstants


user_module = Blueprint("user_module", __name__, url_prefix="/user")


@user_module.route("me", methods=["GET"])
@jwt_required()
@user_active_check()
@encryptor
def user_profile():
    """
    Fetching the user details
    Mandatory field is access-token as header

    PROCESS
        From the token provided username is fetched
        User_details of that particular user is fetched
        If File ID is present then it is also included in the user_details that is being fetched
    """
    try:
        user_id = get_jwt_identity()
        response, status_code = UserprofileHelper.get_user_profile_helper(
            user_id
        )
        if status_code != 200:
            return response, status_code
        return jsonify(response), 200

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function user_profle: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500