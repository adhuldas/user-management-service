import logging
from flask import jsonify
from apps.models.singup_model import SignupModel
from constants.response_constants import ResponseConstants


class SignupHelper:
    """ """

    @staticmethod
    def user_singup_helper(request_content):
        """ """
        try:
            # Validate the incoming request data using Pydantic model
            request_data = SignupModel(**request_content)

            return jsonify(request_data.model_dump()), 200

        except Exception as exc:
            logging.error(f"Error occured in function user_singup_helper:{exc}")
            return (
                jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE),
                500,
            )
