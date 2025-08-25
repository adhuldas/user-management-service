
import logging

from apps.database.constants import MongoDbAggregrationConstants


class UserDetailsAggregation:
    """ 
    
    """

    @staticmethod
    def get_complete_user_details(user_id):
        """ """
        try:

            pipeline = [
                {
                    MongoDbAggregrationConstants.MATCH: {
                        "user_id": user_id
                    }
                },
                {
                    MongoDbAggregrationConstants.LOOKUP: {
                        "from": "UserType",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "join_result",
                    }
                },
                {
                    MongoDbAggregrationConstants.PROJECT: {
                        "_id": 0,
                        "username": 1,
                        "user_id": 1,
                        "firstname": 1,
                        "lastname": 1,
                        "timezone": 1,
                        "Status": 1,
                        "communication_email": 1,
                        "files_id": 1,
                        "language_preference": 1,
                        "street_address1": "$address.street_address1",
                        "street_address2": "$address.street_address2",
                        "state": "$address.state",
                        "city": "$address.city",
                        "zip_code": "$address.zip_code",
                        "phone_number": 1,
                        "country_code": 1,
                        "installer_uploaded_file_id": 1,
                        "user_type": {
                            MongoDbAggregrationConstants.COND: {
                                "if": {
                                    "$eq": [
                                        {
                                            "$size": MongoDbAggregrationConstants.JOINED_RESULT
                                        },
                                        0,
                                    ]
                                },
                                "then": "customer",
                                "else": {
                                    MongoDbAggregrationConstants.ARRAY_ELEMENT: [
                                        MongoDbAggregrationConstants.JOINED_RESULT,
                                        0,
                                    ]
                                },
                            }
                        },
                    }
                },
            ]
            return pipeline
        except Exception as exc:
            logging.error(
                f"Error occured in function get_complete_user_details:{exc}"
            )
            return []
        
    @staticmethod
    def get_user_details(username):
        """ """
        try:
            pipeline = [
                {
                    MongoDbAggregrationConstants.MATCH: {
                        "username": username.lower()
                    }
                },
                {
                    "$lookup": {
                        "from": "UserType",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "join_result",
                    }
                },
                {
                    "$unwind": {
                        "path": "$join_result",
                        "preserveNullAndEmptyArrays": True,
                    }
                },
                {
                    MongoDbAggregrationConstants.PROJECT: {
                        "_id": 0,
                        "user_id": "$user_id",
                        "user_type": "$join_result.user_type",
                        "username": 1,
                        "Status": 1,
                        "password": 1,
                    }
                },
            ]
            return pipeline
        except Exception as exc:
            logging.error(f"Error in get_user_details: {exc}")
            return []