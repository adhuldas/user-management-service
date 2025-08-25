

import logging
from flask import jsonify
from pydantic import ValidationError
from apps.database.models import UsersDb, UsersTokenDb
from apps.models.register_models import UserRegistrationModel
from apps.utils.generic_utils import error_message
from apps.validators.register_validators import RegisterUserValidator
from constants.response_constants import ResponseConstants


class RegisterHelper:
    """ 
    
    """

    @staticmethod
    def register_user_helper(request_content):
        """ 
        
        
        """
        try:
            # Parse and validate the request payload using Pydantic model
            request_data = UserRegistrationModel(**request_content)
            # Validate user_type and token consistency; revoke token if mismatch
            response, status_code = (
                RegisterUserValidator.validate_user_type_and_revoke_token_if_mismatch(
                    request_data.slug,
                    request_data.user_type,
                    request_data.token,
                    request_data.username,
                )
            )
            # If mismatch found or validation failed, return the response
            if response:
                return response, status_code

            # Check if user already exists by matching exact or lowercase username
            _is_user_existing = UsersDb().find(
                {
                    "$or": [
                        {"username": request_data.username},  # exact match
                        {
                            "username": request_data.username.lower()
                        },  # lowercase match
                    ]
                }
            )
            if _is_user_existing:
                # Clean up token if duplicate user found
                UsersTokenDb().delete_many({"token": request_data.token})
                # Return user exists message depending on request source
                return jsonify(message="This user already exists"), 403

            # Validate the password with application rules
            response, status_code = RegisterUserValidator.is_password_valid(
                request_data.password
            )
            if response:
                return response, status_code

            # Prepare user data for insertion into the database
            user_data = RegisterUserValidator.prepare_user_details(
                request_data
            )

            if not user_data:
                return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500

            # Insert the new user into the database and return the response
            response, status_code = RegisterUserValidator.create_user_in_db(
                user_data, request_data
            )
            return response, status_code

        except ValidationError as e:
            # Return the first validation error from the request schema
            first_error_msg = error_message(e)
            return jsonify(message=first_error_msg), 400

        except Exception as exc:
            logging.error(f"Error occured in function register_user_helper:{exc}")
            return (
                jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                500,
            )
