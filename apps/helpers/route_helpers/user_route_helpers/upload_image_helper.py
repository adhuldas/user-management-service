import logging
from flask import jsonify
from gridfs import GridFS
from apps.database.models import FsDb, UsersDb
from constants.response_constants import ResponseConstants
from apps.factory import mongo

fs = GridFS(mongo.db)


class UploadImageHelper:
    """ """

    @staticmethod
    def upload_image(profile_picture, user_id):
        """ """
        try:
            updated_values = {}
            picture_id = fs.put(
                (profile_picture),
                user_id=user_id,
                File_Type="Profile_Image",
            )
            updated_values.update({f"files_id": f"{picture_id}"})
            image = FsDb().find_one(
                {
                    "$and": [
                        {"_id": {"$ne": picture_id}},
                        {
                            "user_id": user_id,
                            "File_Type": "Profile_Image",
                        },
                    ]
                },
                {"_id": 1},
            )
            # TO AVOID ERROR RAISING FOR "nonetype' object is not subscriptable"
            if image and "_id" in image:
                # here id will be fetched from above query and corresponding document will be deleted
                image_id = image["_id"]
                # here image_id will be deleted from gridfs
                fs.delete(image_id)
            UsersDb().find_one_and_update({"user_id":user_id},updated_values)
            return jsonify(message="Profile photo uploaded for customer"), 200

        except Exception as exc:
            logging.error(f"Error occured in function upload_image:{exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500
