

import logging
import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from apps.database_query_handler.aggregate_queries.search_aggregation import UserList
from apps.decorators.fernet_decorators import decryptor, encryptor
from apps.decorators.validation_decorators import content_type_check, require_fields, user_active_check
from apps.helpers.route_helpers.user_route_helpers.signin_helper import SigninHelper
from apps.helpers.route_helpers.user_route_helpers.user_profile_helper import UserprofileHelper
from constants.response_constants import ResponseConstants


user_module = Blueprint("user_module", __name__, url_prefix="/user")


@user_module.route("signin", methods=["POST"])
@content_type_check("json")
@decryptor
@require_fields("username", "password")
def signin():
    """
    Login by username and password
    Mandatory field is username and password

    PROCESS
        Checks if the given username and password is valid by checking with database
        Checks user type
        If it is valid an access and refresh token are created with additional claims
    """
    try:

        response, status_code = SigninHelper.signin_api_helper(
            request.decrypted_data
        )

        return response, status_code
    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function signin: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


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
        return response

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function user_profle: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
    

@user_module.route("list", methods=["POST"])
@jwt_required()
@content_type_check("json")
@decryptor
def search_user():
    """ 
    
    """
    try:
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        name = request.decrypted_data.get("search_data")
        if " " in name:
            first_name, last_name = name.split(maxsplit=1)
            firstname = f".*{re.escape(first_name)}.*"
            lastname = f".*{re.escape(last_name)}.*"
            # model function to perform aggrgration
            user_list = UserList.user_name_list(firstname, lastname)
        # condtion to check whether received parameter is holding only email
        elif re.match(email_pattern, name):
            user_list = UserList.user_list_request_data({"username": name})
        # to check whether received parameter is holding only whether firstname or lastname
        else:
            regex_pattern = f".*{re.escape(name)}.*"
            # model function to perform aggrgration
            user_list = UserList.user_name_list(
                firstname=regex_pattern, lastname=regex_pattern
            )
        return jsonify(user_list),200

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function user_profle: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
    