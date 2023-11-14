from utils.database_ops import DatabaseOperations
from utils.data_ops import DataOperations

class DataProcessor:
    def __init__(self):
        self.db_operations = DatabaseOperations()
        self.data_operations = DataOperations()

    def process_market_data(self):
        # Retrieve data from MongoDB
        raw_data = self.db_operations.fetch_data_from_mongodb("market_data")
        for col in raw_data.columns:
            print(col)
        # Clean and transform data
        clean_data = self.data_operations.clean_and_transform_data(raw_data)

        # Perform feature engineering
        feature_data = self.data_operations.feature_engineering(clean_data)

        # Further processing as needed (e.g., normalization, splitting data)

        # Save or return processed data
        # Example: self.db_operations.insert_data_into_mongodb("processed_market_data", feature_data.to_dict('records'))

# Usage example
data_processor = DataProcessor()
data_processor.process_market_data()
