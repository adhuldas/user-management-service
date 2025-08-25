"""
Module for interacting with various MongoDB collections.

This module provides classes for performing CRUD operations on different MongoDB collections.
Each class extends the MongoDbHandler class and is initialized with the name of the corresponding
collection.

Example Usage:
    controllers_db = ControllersInventoryDb(mongo_uri="mongodb://localhost:27017/mydb")
    data = {"key1": "value1", "key2": "value2"}
    controllers_db.insert_one(data)
"""

from apps.database.constants import DbNameConstants
from apps.database.handler import MongoDbHandler


# Factory to reduce code duplication
class BaseCollection(MongoDbHandler):
    def __init__(
        self,
        collection_name: str,
    ):
        super().__init__(collection_name)

class UserAccountOtpDb(BaseCollection):
    def __init__(self):
        super().__init__(DbNameConstants.user_account_otp_db)

class UserInfoDb(BaseCollection):
    def __init__(self):
        super().__init__(DbNameConstants.user_info_db)

class UsersDb(BaseCollection):
    def __init__(self):
        super().__init__(DbNameConstants.users_db)

class UsersTokenDb(BaseCollection):
    def __init__(self):
        super().__init__(DbNameConstants.users_token_db)

class UserTypeDb(BaseCollection):
    def __init__(self):
        super().__init__(DbNameConstants.user_type_db)

class FsDb(MongoDbHandler):
    def __init__(self) -> None:
        super().__init__(DbNameConstants.fs_files)