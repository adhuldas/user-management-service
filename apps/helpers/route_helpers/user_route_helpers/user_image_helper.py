
import logging
from bson import ObjectId
from flask import jsonify, make_response
from gridfs import GridFS
from pydantic import ValidationError
from apps.database.models import UsersDb
from apps.models.user_image_model import UserImageModel
from constants.response_constants import ResponseConstants
from apps.factory import mongo
fs = GridFS(mongo.db)

class UserImageHelper:
    """ 
    
    """

    @staticmethod
    def get_user_image(request_content):
        """ 
        
        """
        try:
            # Validate and parse the incoming request data
            request_data = UserImageModel(**request_content)

            # Ensure that the given files_id exists in the Users collection
            image_id_data = UsersDb().find_one(
                {"files_id": request_data.files_id}, {"files_id": 1, "_id": 0}
            )
            if not image_id_data:
                # Image metadata not found
                return (
                    jsonify(message="Image not found for the given files_id"),
                    404,
                )
            # Retrieve the actual image file from GridFS using the files_id
            image = fs.get(ObjectId(request_data.files_id))
            image_data = image.read()

            # Return the image as a Flask HTTP response with JPEG header
            response = make_response(image_data)
            response.headers["Content-Type"] = "image/jpeg"
            return response, 200

        except ValidationError as e:
            # Return the first validation error from the request schema
            first_error_msg = e.errors()[0]["msg"]
            return jsonify(message=first_error_msg), 400

        except Exception as exc:
            # Log and handle any unhandled exceptions
            logging.error(f"Error in get_user_image: {exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500