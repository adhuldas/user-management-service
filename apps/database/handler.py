from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional

from config import Config


class MongoDbHandler:
    """
    Handler class for MongoDB operations with dynamic URI support.

    This class provides methods for performing CRUD (Create, Read, Update, Delete) operations
    on a MongoDB collection. You can connect either via a Mongo URI or reuse a MongoClient instance.

    Attributes:
        db_connection (pymongo.collection.Collection): The connection to the MongoDB collection.
    """

    def __init__(
        self,
        collection_name: str,
    ) -> None:
        """
        Initialize MongoDbHandler.

        Args:
            collection_name (str): The name of the MongoDB collection to connect to.
            mongo_uri (str, optional): MongoDB connection URI (e.g., mongodb://localhost:27017/mydb).
            client (MongoClient, optional): An existing pymongo MongoClient instance.

        Raises:
            TypeError: If collection_name is not a string.
            ValueError: If neither mongo_uri nor client is provided.
        """
        if not isinstance(collection_name, str):
            raise TypeError("collection_name should be instance of str")
        self.client = MongoClient(Config.MONGO_URI)

        if Config.MONGO_URI:
            db_name = Config.MONGO_URI.rsplit("/", 1)[-1].split("?")[0]
            self.db_connection: Collection = self.client[db_name][collection_name]
        else:
            self.db_connection: Collection = self.client.get_default_database()[
                collection_name
            ]

    def dict_instance_checker(self, parameter: dict, _is_filter: bool = False):
        if not isinstance(parameter, dict):
            message = "input should be instance of dict"
            if _is_filter:
                message = "where condition should be dict"
            raise TypeError(message)

    def list_instance_checker(self, parameter: list, _is_filter: bool = False):
        if not isinstance(parameter, list):
            message = "input should be instance of list"
            if _is_filter:
                message = "where condition should be list"
            raise TypeError(message)

    def find(
        self,
        data: dict,
        filter: dict = {"_id": 0},
        sort_filter: Optional[dict] = None,
    ):
        """
        Find documents in the collection.

        Args:
            data (dict): The query filter.
            filter (dict): Projection fields to include/exclude.
            sort_filter (dict, optional): e.g., {"sort_key": "timestamp", "sort_value": -1}

        Returns:
            list: List of matching documents.
        """
        self.dict_instance_checker(data)
        cursor = self.db_connection.find(data, filter)
        if sort_filter:
            sort_key = sort_filter.get("sort_key")
            sort_value = sort_filter.get("sort_value")
            if sort_key and sort_value:
                cursor = cursor.sort(sort_key, sort_value)
        return list(cursor)

    def find_one(self, data: dict, filter: dict = {"_id": 0}):
        """
        Find a single document in the collection.

        Args:
            data (dict): The query filter.
            filter (dict): Projection fields to include/exclude.

        Returns:
            dict or None: A single matching document.
        """
        self.dict_instance_checker(data)
        return self.db_connection.find_one(data, filter)

    def insert_one(self, data: dict):
        self.dict_instance_checker(data)
        return self.db_connection.insert_one(data)

    def insert_many(self, data: list):
        self.list_instance_checker(data)
        return self.db_connection.insert_many(data)

    def update_one(self, data: dict, filter: dict):
        self.dict_instance_checker(data)
        self.dict_instance_checker(filter, _is_filter=True)
        return self.db_connection.update_one(filter, {"$set": data})

    def update_many(self, data: dict, filter: dict):
        self.dict_instance_checker(data)
        self.dict_instance_checker(filter, _is_filter=True)
        return self.db_connection.update_many(filter, {"$set": data})

    def delete_one(self, data: dict):
        self.dict_instance_checker(data)
        return self.db_connection.delete_one(data)

    def delete_many(self, data: dict):
        self.dict_instance_checker(data)
        return self.db_connection.delete_many(data)

    def find_one_and_update(self, filter: dict,data: dict):
        self.dict_instance_checker(data)
        self.dict_instance_checker(filter, _is_filter=True)
        return self.db_connection.find_one_and_update(filter, {"$set": data})

    def find_one_and_delete(self, data: dict):
        self.dict_instance_checker(data)
        return self.db_connection.find_one_and_delete(data)

    def aggregate(self, data: list):
        """
        Perform aggregation on the collection.

        Args:
            data (list): Aggregation pipeline.

        Returns:
            list: Aggregated result.
        """
        self.list_instance_checker(data)
        return list(self.db_connection.aggregate(data))
