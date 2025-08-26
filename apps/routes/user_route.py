import logging
import re
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from apps.database_query_handler.aggregate_queries.search_aggregation import UserList
from apps.decorators.fernet_decorators import decryptor, encryptor
from apps.decorators.token_validator_decorator import token_required
from apps.decorators.validation_decorators import (
    content_type_check,
    require_fields,
    user_active_check,
)
from apps.helpers.route_helpers.user_route_helpers.signin_helper import SigninHelper
from apps.helpers.route_helpers.user_route_helpers.signout_helper import SignOutHelper
from apps.helpers.route_helpers.user_route_helpers.upload_image_helper import (
    UploadImageHelper,
)
from apps.helpers.route_helpers.user_route_helpers.user_image_helper import (
    UserImageHelper,
)
from apps.helpers.route_helpers.user_route_helpers.user_profile_helper import (
    UserprofileHelper,
)
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

        response, status_code = SigninHelper.signin_api_helper(request.decrypted_data)

        return response, status_code
    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function signin: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("me", methods=["GET"])
@token_required
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
        response, status_code = UserprofileHelper.get_user_profile_helper(user_id)
        if status_code != 200:
            return response, status_code
        return response

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function user_profle: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("list", methods=["POST"])
@token_required
@jwt_required()
@content_type_check("json")
@decryptor
def search_user():
    """ """
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
        return jsonify(user_list), 200

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function user_profle: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("image/<image_id>", methods=["GET"])
def render_profile_picture(image_id):
    """ """
    try:
        response, status_code = UserImageHelper.get_user_image(image_id)

        return response, status_code
    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function render_profile_picture: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("update/profile/image", methods=["POST"])
@token_required
@jwt_required()
def update_user_profile():
    """ """
    try:
        user_id = get_jwt_identity()
        profile_picture = request.files.get("profile_picture")
        response, status_code = UploadImageHelper.upload_image(profile_picture, user_id)
        return response, status_code
    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function render_profile_picture: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("signout", methods=["DELETE"])
@token_required
@jwt_required()
def singout():
    """
    API for logout and save JTI of corresponding access and refresh tokens
    Mandatory field is refresh token

    PROCESS
        JTI and Type of access token is fetched with get_jwt method
        Similarly JTI and Type of refresh token is fetched by decoding it
        Both of the JTIs and Types are stored into the token_blocklist collection
    """
    try:
        jti = get_jwt()["jti"]
        type1 = get_jwt()["type"]
        response, status_code = SignOutHelper.user_signout_helper(
            jti, type1, request.json
        )

        return response, status_code

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function singout: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500


@user_module.route("refresh/token", methods=["GET"])
@token_required
@jwt_required(refresh=True)
@user_active_check()
def refresh():
    """
    Fetching new refresh and access tokens by passing the old refresh token
    Mandatory field is refresh-token as header

    PROCESS
        Username is fetched from the refresh token
        From refresh_token the additional calims are also fetched
        New access and refresh tokens are created with additional claims
    """
    try:
        user_id = get_jwt_identity()
        # FROM REFRESH_TOKEN THE ADDITIONAL CALIMS ARE ALSO FETCHED
        claims = get_jwt()["user_details"]
        user_role = get_jwt()["role"]
        additional_claims = {"user_details": claims, "role": user_role}

        # NEW ACCESS AND REFRESH TOKENS ARE CREATED WITH ADDITIONAL CLAIMS
        access_token = create_access_token(user_id, additional_claims=additional_claims)
        refresh_token = create_refresh_token(
            user_id, additional_claims=additional_claims
        )

        # both of the tokens are returned
        return (
            jsonify(access_token=access_token, refresh_token=refresh_token),
            200,
        )

    except Exception as exc:
        # Step 5: Log and handle unexpected exceptions
        logging.error(f"Error occurred in function refresh: {exc}")
        # Step 6: Return generic internal server error
        return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
