import pandas as pd
from pymongo import MongoClient, errors
import logging


class DatabaseOperations:
    """
    A class to manage operations such as fetching, inserting, updating, and deleting data in a MongoDB database.
    """

    def __init__(self):
        """
        Initializes the DatabaseOperations class with configurations for MongoDB connection.
        """
        self.mongo_uri = 'mongodb+srv://mikefuscoletti:sERswgdHNxTxCKrd@cluster0.o9lx9sb.mongodb.net/?retryWrites=true&w=majority'
        self.database_name = 'chance'
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
        except errors.ConnectionFailure as e:
            logging.error(f"MongoDB connection failed: {e}")
            raise
        self.logger = logging.getLogger(__name__)

    def fetch_data_from_mongodb(self, collection_name: str) -> pd.DataFrame:
        """
        Fetch data from a MongoDB collection and return it as a DataFrame.

        Args:
            collection_name (str): The name of the MongoDB collection to fetch data from.

        Returns:
            pd.DataFrame: The data fetched from the MongoDB collection as a DataFrame.
        """
        try:
            cursor = self.db[collection_name].find()
            df = pd.DataFrame(list(cursor))
            return df
        except Exception as e:
            self.logger.error(f"Error fetching data from MongoDB: {e}")
            return pd.DataFrame()

    def insert_data_into_mongodb(self, collection_name: str, data: dict) -> None:
        """
        Insert data into a MongoDB collection. Validates data before insertion.

        Args:
            collection_name (str): The name of the MongoDB collection to insert data into.
            data (dict): The data to insert into the MongoDB collection.

        Returns:
            None
        """
        if not self.validate_data(data):
            self.logger.error("Invalid data format for insertion.")
            return

        try:
            self.db[collection_name].insert_many(data)
            self.logger.info(f"Data inserted successfully into {collection_name} collection.")
        except Exception as e:
            self.logger.error(f"Error inserting data into MongoDB: {e}")

    def validate_data(self, data: dict) -> bool:
        """
        Validates the data format before insertion or update.

        Args:
            data (dict): The data to validate.

        Returns:
            bool: True if data is valid, False otherwise.
        """
        # Implement specific validation logic based on your data requirements
        return True

    def update_data_in_mongodb(self, collection_name: str, query: dict, new_values: dict) -> None:
        """
        Update data in a MongoDB collection.

        Args:
            collection_name (str): The name of the MongoDB collection to update data in.
            query (dict): The query to select the documents to update.
            new_values (dict): The new values to update in the selected documents.

        Returns:
            None
        """
        try:
            self.db[collection_name].update_many(query, {'$set': new_values})
            self.logger.info(f"Data updated successfully in {collection_name} collection.")
        except Exception as e:
            self.logger.error(f"Error updating data in MongoDB: {e}")

    def delete_data_from_mongodb(self, collection_name: str, query: dict) -> None:
        """
        Delete data from a MongoDB collection.

        Args:
            collection_name (str): The name of the MongoDB collection to delete data from.
            query (dict): The query to select the documents to delete.

        Returns:
            None
        """
        try:
            self.db[collection_name].delete_many(query)
            self.logger.info(f"Data deleted successfully from {collection_name} collection.")
        except Exception as e:
            self.logger.error(f"Error deleting data from MongoDB: {e}")

# Usage example:
# db_operations = DatabaseOperations()
# db_operations.fetch_data_from_mongodb('collection_name')
