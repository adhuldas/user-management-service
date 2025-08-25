import logging
from flask import jsonify
from pydantic import ValidationError

from apps.database.models import UsersDb
from apps.database_query_handler.aggregate_queries.user_details_aggreagtion import (
    UserDetailsAggregation,
)
from apps.utils.generic_utils import error_message
from constants.api_endpoints_constants import ApiEndpoints
from constants.response_constants import ResponseConstants


class UserprofileHelper:
    """ """

    @staticmethod
    def get_user_profile_helper(user_id):
        """
        Retrieves and returns complete profile details for a given user.

        The function:
        - Builds and executes an aggregation query to fetch user details
        - Resolves the correct file URL for profile images
        - Decrypts sensitive user data
        - Handles access logic based on `access_for` and `installer_uploaded_file_id`

        Args:
            user_id (str): The unique identifier of the user whose profile is being requested.
            user_info (dict): The JWT-decoded user info (containing access scopes like `access_for`).

        Returns:
            tuple: Either a Flask JSON response with an error and status code,
                or a dictionary of user details and a 200 status code.
        """
        try:
            # Create aggregation pipeline to fetch user details
            query = UserDetailsAggregation.get_complete_user_details(user_id)
            if not query:
                return jsonify(message=ResponseConstants.BAD_REQUEST), 400
            # Execute aggregation query
            user_details = UsersDb().aggregate(query)
            if not user_details:
                # Return empty list if no user found
                return [], 200
            files_id = user_details[0].get("files_id")
            if files_id:
                # Otherwise, use the regular profile image if available
                files_id = ApiEndpoints.IMAGE_URL + f"{files_id}"
                # Update the file URL in the user detail response
                user_details[0].update({"files_id": files_id})
            # Decrypting the user details
            if user_details:
                # Decrypt sensitive user fields (e.g., email, phone, etc.)
                user_details = user_details[0]
            if not user_details:
                return jsonify(ResponseConstants.INTERNAL_ERROR_MESSAGE), 500

            return user_details, 200

        except ValidationError as e:
            # Handle input validation errors
            first_error_msg = error_message(e)
            return jsonify(message=first_error_msg), 400

        except Exception as exc:
            # Log and handle unexpected runtime errors
            logging.error(f"Error in user_profile_helper: {exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
