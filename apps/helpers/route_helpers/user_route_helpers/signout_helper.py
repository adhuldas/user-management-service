

import logging
from flask import jsonify
from flask_jwt_extended import decode_token
from pydantic import ValidationError
from datetime import datetime
from apps.database.models import TokenBlockListDb
from apps.models.signout_model import SignOut
from apps.utils.generic_utils import error_message
from constants.response_constants import ResponseConstants


class SignOutHelper:
    """ 
    
    """

    @staticmethod
    def user_signout_helper(jti,type1,request_content):
        """ 
        
        """
        try:
            request_data = SignOut(**request_content)
            # current time is fetched
            now = datetime.now()
            ref = decode_token(request_data.refresh_token)
            rjti = ref["jti"]
            rtype = ref["type"]
            # BOTH OF THE JTIS AND TYPES ARE STORED INTO THE TOKEN_BLOCKLIST COLLECTION
            TokenBlockListDb().insert_many(
                [
                    {"jti": jti, "created_at": now, "type": type1},
                    {"jti": rjti, "created_at": now, "type": rtype},
                ]
            )
            return jsonify(message="JWT revoked"), 200

        except ValidationError as e:
            # Handle schema validation errors (missing fields, wrong types, etc.)
            first_error_msg = error_message(e)
            return jsonify(message=first_error_msg), 400

        except Exception as exc:
            # Handle unexpected errors with logging and generic error message
            logging.error(f"Error in user_signout_helper: {exc}")
            return jsonify(message=ResponseConstants.REFRESH_TOKEN_BAD_REQUEST), 400