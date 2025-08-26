class DbNameConstants:
    """
    CLASS THAT HOLD ALL COLLECTION NAME
    """

    user_account_otp_db = "UserAccountOtp"
    user_info_db = "UserInfo"
    users_db = "Users"
    users_token_db = "UsersToken"
    user_type_db = "UserType"
    fs_files = "fs.files"
    token_blocklist = "token_blocklist"


class MongoDbAggregrationConstants:
    """
    Class which holds MongoDB related constants.
    """

    # MongoDB aggregation stage constants
    MATCH = "$match"  # Match documents that meet the specified condition(s)
    LOOKUP = "$lookup"  # Perform a left outer join to another collection in the same database
    PROJECT = "$project"  # Reshape each document in the stream, such as by including, excluding, or adding fields
    COND = "$cond"  # Evaluate a boolean expression to return one of the two specified values
    GROUP = "$group"  # Group documents by a specified identifier expression and apply the accumulator expressions
    COUNT = (
        "$count"  # Count the number of documents in the aggregation pipeline
    )
    UNWIND = "$unwind"  # Deconstruct an array field from the input documents to output a document for each element
    FIRST = "$first"  # Returns the first value in a group of documents
    SIZE = "$size"  # Returns the size of an array
    ARRAY_ELEMENT = (
        "$arrayElemAt"  # Returns the element at the specified array index
    )
    PUSH = "$push"  # Append a value to an array in the resulting document
    ADDFIELD = "$addFields"
    AND = "$and"
    OR = "$or"
    SORT = "$sort"
    EXPR = "$expr"
    EXISTS = "$exists"
    EQUAL = "$eq"

    # MongoDB field name constants used in aggregation
    USER_ID = "$user_id"  # Field name for user ID
    LOCAL_FIELD = "localField"  # Local field name for $lookup
    FOREIGN_FIELD = "foreignField"  # Foreign field name for $lookup
    PIPELINE = "pipeline"  # Pipeline field name for $lookup
    USER_TYPE_INFO = "$user_type_info.user_type"
    SHARED_TYPE_INFO = "$shared_type_info.user_role"
    UNWIND = "$unwind"
    JOINED_DATA = "$joined_data.device_status"
    USER_RESULT = "$user_result"
    CONTROLLER_RESULT = "$controller_result"
    METADATA_OPERATION = "metadata.operation"
    METADATA_CONTROLLER_UUID = "metadata.controller_uuid"
    JOINED_RESULT = "$join_result.user_type"
