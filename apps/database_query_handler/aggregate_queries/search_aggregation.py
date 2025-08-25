import logging
from flask import jsonify
from apps.database.constants import MongoDbAggregrationConstants
from apps.database.models import UsersDb
from constants.response_constants import ResponseConstants


class UserList:

    @staticmethod
    def user_list_request_data(request_data):
        """
        FUNCTION TO PERFORM AGGREGRATION BASED ON request_data

        PROCESS INVOLVED
            - Users IS TAKEN AS THE PRIMARY COLLECTION WITH request_data FILTER
            - UserType IS THEN LOOKED UP FOR COMMON user_id
            - THEN PROJECT THE RESULT AND ADDED CUSTOMER FOR THOSE RECORD DOESN'T HAVE user_type
        """
        # Users IS TAKEN AS THE PRIMARY COLLECTION WITH request_data FILTER
        try:
            pipeline = [
                {MongoDbAggregrationConstants.MATCH: {"Status": "Active"}},
                {MongoDbAggregrationConstants.MATCH: request_data},
                # UserType IS THEN LOOKED UP FOR COMMON user_id
                {
                    MongoDbAggregrationConstants.LOOKUP: {
                        "from": "UserType",
                        "localField": "user_id",
                        "foreignField": "user_id",
                        "as": "user_type_info",
                    }
                },
                # THEN PROJECT THE RESULT AND ADDED CUSTOMER FOR THOSE RECORD DOESN'T HAVE user_type
                {
                    MongoDbAggregrationConstants.PROJECT: {
                        "_id": 0,
                        "firstname": 1,
                        "lastname": 1,
                        "user_id": 1,
                        "files_id": 1,
                        "username": 1,
                        "timezone": 1,
                        "user_type": {
                            MongoDbAggregrationConstants.COND: {
                                "if": {
                                    "$eq": [
                                        {
                                            MongoDbAggregrationConstants.SIZE: MongoDbAggregrationConstants.USER_TYPE_INFO
                                        },
                                        0,
                                    ]
                                },
                                "then": "customer",
                                "else": {
                                    MongoDbAggregrationConstants.ARRAY_ELEMENT: [
                                        MongoDbAggregrationConstants.USER_TYPE_INFO,
                                        0,
                                    ]
                                },
                            }
                        },
                    }
                },
                {MongoDbAggregrationConstants.MATCH: {"user_type": "customer"}},
            ]
            # if request_data is not none it will return the aggregated data against the match condition
            if request_data:
                user_list = UsersDb().aggregate(pipeline)
            # else return whole record with upto the limit 100 record
            else:
                pipeline.append({"$limit": 100})
                user_list = UsersDb().aggregate(pipeline)

            return user_list

        except Exception as exc:  # pragma: no cover
            logging.error(f"Error occurred at user_list_request_data:{exc}")
            return jsonify(message=ResponseConstants.INTERNAL_ERROR_MESSAGE), 500

    @staticmethod
    def user_name_list(firstname, lastname):
        """
        FUNCTION TO PERFORM AGGREGRATION BASED ON FIRSTNAME AND LASTNAME

        PROCESS INVOLVED
            - Users IS TAKEN AS THE PRIMARY COLLECTION WITH FIRSTNAME AND LASTNAME FILTER WITH REGEX COMBINATION
            - UserType IS THEN LOOKED UP FOR COMMON user_id
            - THEN PROJECT THE RESULT AND ADDED CUSTOMER FOR THOSE RECORD DOESN'T HAVE user_type

        """
        # Users IS TAKEN AS THE PRIMARY COLLECTION WITH FIRSTNAME AND LASTNAME FILTER WITH REGEX COMBINATION
        try:
            user_list = UsersDb().aggregate(
                [
                    {
                        MongoDbAggregrationConstants.MATCH: {
                            "Status": "Active"
                        }
                    },
                    {
                        MongoDbAggregrationConstants.MATCH: {
                            "$and": [
                                {
                                    "$or": [
                                        {
                                            "firstname": {
                                                "$regex": firstname,
                                                "$options": "i",
                                            }
                                        },
                                        {
                                            "lastname": {
                                                "$regex": lastname,
                                                "$options": "i",
                                            }
                                        },
                                    ]
                                }
                            ]
                        }
                    },
                    # UserType IS THEN LOOKED UP FOR COMMON user_id
                    {
                        MongoDbAggregrationConstants.LOOKUP: {
                            "from": "UserType",
                            "localField": "user_id",
                            "foreignField": "user_id",
                            "as": "user_type_info",
                        }
                    },
                    # THEN PROJECT THE RESULT AND ADDED CUSTOMER FOR THOSE RECORD DOESN'T HAVE user_type
                    {
                        MongoDbAggregrationConstants.PROJECT: {
                            "_id": 0,
                            "firstname": 1,
                            "lastname": 1,
                            "user_id": 1,
                            "files_id": 1,
                            "username": 1,
                            "timezone": 1,
                            "user_type": {
                                MongoDbAggregrationConstants.COND: {
                                    "if": {
                                        "$eq": [
                                            {
                                                MongoDbAggregrationConstants.SIZE: MongoDbAggregrationConstants.USER_TYPE_INFO
                                            },
                                            0,
                                        ]
                                    },
                                    "then": "customer",
                                    "else": {
                                        MongoDbAggregrationConstants.ARRAY_ELEMENT: [
                                            MongoDbAggregrationConstants.USER_TYPE_INFO,
                                            0,
                                        ]
                                    },
                                }
                            },
                        }
                    },
                ]
            )

            return user_list

        except Exception as exc:  # pragma: no cover
            logging.error(f"Error occurred at user_name_list:{exc}")
            return (
                jsonify(
                    message=ResponseConstants.INTERNAL_ERROR_MESSAGE
                ),
                500,
            )
