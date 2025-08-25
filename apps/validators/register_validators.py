import logging
import re
from flask import jsonify, render_template
import jwt
from apps.database.models import UserAccountOtpDb, UserTypeDb, UsersDb, UsersTokenDb
from apps.models.register_models import UserRegistrationModel
from config import Config
from constants.common_constants import CommonConstant
from constants.response_constants import ResponseConstants
from werkzeug.security import generate_password_hash


class RegisterUserValidator:
    """ """

    @staticmethod
    def validate_user_type_and_revoke_token_if_mismatch(
        slug_id: str, user_type: str, _token: str, _username: str
    ):
        """
        Validates the user_type from the database with the provided user_type.
        If mismatch occurs, token is revoked and unauthorized access response is returned.

        Args:
            slug_id (str): The slug identifier to find the user's expected user_type.
            user_type (str): The user_type being validated.
            _token (str): The token to be revoked if validation fails.

        Returns:
            None if validation succeeds, else (jsonify response, HTTP status code).
        """
        try:
            dynamic_values = UserAccountOtpDb().find_one(
                {"slug_id": slug_id}, {"jwt_key": 1, "user_type": 1}
            )

            if not dynamic_values:
                return (
                    jsonify(message=ResponseConstants.UNPROCESSABLE_ENTITY),
                    422,
                )

            if dynamic_values.get("user_type") != user_type:
                UsersTokenDb().delete_many({"token": _token})
                return (
                    jsonify(message=ResponseConstants.UNPROCESSABLE_ENTITY),
                    422,
                )

            created_token = UsersTokenDb().find_one(
                {"token": _token}, {"token": 1, "_id": 0}
            )

            if not created_token:
                return (
                    jsonify(
                        message=ResponseConstants.RESTRICTED_ACCESS_MESSAGE
                    ),
                    401,
                )

            _is_token_expired, status_code = (
                RegisterUserValidator.verify_and_validate_token_email(
                    created_token, dynamic_values.get("jwt_key"), _username
                )
            )
            if status_code != 200:
                return _is_token_expired, status_code

            return None, 200

        except Exception as exc:
            logging.error(
                f"Error occured in function validate_user_type_and_revoke_token_if_mismatch:{exc}"
            )
            # In case of DB failure or unexpected error, still deny access gracefully
            return jsonify(message=ResponseConstants.UNPROCESSABLE_ENTITY), 422

    @staticmethod
    def verify_and_validate_token_email(
        created_token: dict, jwt_key: str, _username: str
    ):
        """
        Verifies JWT token, checks if the embedded email matches the provided username.

        If invalid or expired, returns a Flask JSON response. Returns None if valid.

        Args:
            created_token (dict): Dictionary with 'token' key.
            jwt_key (str): JWT secret key.
            request: Flask request object.
            _username (str): Username to match with email in token.

        Returns:
            Response | None: `jsonify` response if invalid, else None.
        """
        try:
            db_created_token = created_token.get("token")
            decoded_token = jwt.decode(
                db_created_token, jwt_key, algorithms=["HS256"]
            )
            token_email = decoded_token.get("email")
            if db_created_token and _username == token_email:
                return None, 200
            else:
                return (
                    jsonify(
                        message=ResponseConstants.RESTRICTED_ACCESS_MESSAGE
                    ),
                    403,
                )

        except jwt.ExpiredSignatureError:
            UsersTokenDb().delete_many({"token": created_token.get("token")})
            return jsonify(message="The provided token is expired"), 401


    @staticmethod
    def is_password_valid(password):
        """
        Validates the password against the regex pattern defined in Config.

        Args:
            _password (str): The password to validate.

        Returns:
            Response or None: Returns a Flask response if invalid, else None.
        """
        try:
            pattern = re.compile(Config.PASSWORD_REGEX)
            if not re.search(pattern, password):
                return (
                    jsonify(message=ResponseConstants.PASSWORD_FORMAT_MESSAGE),
                    403,
                )

            return None, 200
        except Exception as exc:
            logging.error(f"Error occured in function is_password_valid:{exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
        
    @staticmethod
    def prepare_user_details(request_data: UserRegistrationModel) -> dict:
        """
        Prepares the user_details dictionary for insertion or further processing.

        Args:
            request_data (RegisterUserModel): Parsed and validated user registration input.

        Returns:
            dict: Final user details with hashed password and additional fields.
        """
        try:
            _hashed_password = generate_password_hash(request_data.password)

            user_details = {
                "firstname": request_data.firstname,
                "lastname": request_data.lastname,
                "timezone": request_data.timezone,
                "username": request_data.username.lower(),
                "password": _hashed_password,
                "user_id": request_data.user_id,
                "Status": request_data.user_status,
                "phone_number": request_data.phone_number,
                "country_code": request_data.country_code,
                "language_preference": "en",
            }

            # Build user_group
            user_group = {
                "user_id": request_data.user_id,
                "user_type": request_data.user_type,
            }

            return {
                "user_details": user_details,
                "user_group": user_group,
            }

        except Exception as exc:
            logging.error(
                f"Error occured in function prepare_user_details:{exc}"
            )
            return {}
        
    @staticmethod
    def create_user_in_db(user_data, request_data):
        """
        Creates a new user in the database and handles associated user group and user info records.

        This function performs the following:
        - Inserts the user's main details into the `UsersDb` collection.
        - Updates or inserts user group information into the `UserTypeDb` collection.
        - If the user type is 'installer', updates or inserts user info in `UserInfoDb` and sends an email via Celery.
        - Deletes any existing tokens from `UsersTokenDb`.
        - Returns an HTML page or JSON response.

        Args:
            user_data (dict): A dictionary containing user_details, user_group, and user_info.
            request_data (Any): An object containing request data attributes such as username, firstname, lastname, user_type, context, and token.

        Returns:
            tuple: HTML or JSON response with HTTP status code based on the input type.
        """
        try:
            # Extract individual data components from the user_data dict
            user_details = user_data.get("user_details")
            user_group = user_data.get("user_group")

            # Insert user details into the Users collection
            UsersDb().insert_one(user_details)

            # Try updating user group info; if not found, insert new
            user_existing = UserTypeDb().find_one_and_update(
                {"username": request_data.username},
                {"$set": user_group},
            )

            if not user_existing:
                UserTypeDb().insert_one(user_group)

            # Clear existing JWT tokens for this user (cleanup step)
            UsersTokenDb().delete_many({"token": request_data.token})
            UserAccountOtpDb().delete_many({"slug_id":request_data.slug})

            # Return JSON success response for API-based requests
            return jsonify(message="Account created successfully"), 200

        except Exception as exc:
            # Log any errors and return internal server error response
            logging.error(f"Error occured in function create_user_db: {exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500