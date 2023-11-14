import datetime
import pandas as pd
from crypto_compare import Client
from utils.database_ops import DatabaseOperations

class DataCollector:
    """
    A class to handle the collection of cryptocurrency data from various APIs.
    """

    def __init__(self):
        """
        Initializes the DataCollector class.
        """
        self.db_operations = DatabaseOperations()
        self.api_key = '77426a009275e7cdc54c4d4b35edf7aca9d40f8d583a259b2328e49f11e786bc'  # Replace with your actual API key
        self.client = Client(self.api_key)

    def collect_market_data(self, currency='USD'):
        """
        Collects historical market data for a preset list of cryptocurrencies for the last 10 years.
        """
        coin_list = ['BTC', 'ETH', 'LTC', 'XRP', 'ADA', 'DOT', 'LINK', 'XLM', 'DOGE', 'BNB', 
                     'SOL', 'XMR', 'VET', 'XTZ', 'MIOTA', 'ATOM', 'AAVE', 'UNI', 'ALGO', 'FIL']

        current_time = int(datetime.datetime.now().timestamp())  # Current Unix timestamp

        for coin in coin_list:
            print(f"Collecting 10 years of daily data for {coin}...")

            try:
                # First API call for the most recent 2000 data points
                recent_data_response = self.client.histo_day(fsym=coin, tsym=currency, limit=2000, toTs=current_time)

                # Extract data points from JSON response
                recent_data = recent_data_response.get('Data')
                if not recent_data:
                    raise ValueError(f"No data found in recent_data_response for {coin}")

                last_date = recent_data[-1].get('time')
                if not last_date:
                    raise ValueError(f"Last date not found in recent_data for {coin}")

                # Second API call for the remaining data points
                earlier_data_response = self.client.histo_day(fsym=coin, tsym=currency, limit=1650, toTs=last_date)
                earlier_data = earlier_data_response.get('Data')
                if not earlier_data:
                    raise ValueError(f"No data found in earlier_data_response for {coin}")

                # Combine the data from both calls
                total_data = recent_data + earlier_data

                # Check if data is collected
                if not total_data:
                    raise ValueError(f"No data returned for {coin}")

                # Add coin identifier to each data entry and insert into MongoDB
                for entry in total_data:
                    entry['coin'] = coin
                self.db_operations.insert_data_into_mongodb("market_data", total_data)

            except Exception as e:
                print(f"Error collecting data for {coin}: {e}")
                continue

    def collect_mining_data(self):
        """
        Collects mining data for various cryptocurrencies.
        """
        print("Collecting mining data...")
        mining_data = self.client.mining_contracts()
        if mining_data:
            self.db_operations.insert_data_into_mongodb("mining_data", mining_data)
        else:
            print("Failed to collect mining data")

    def collect_social_stats(self):
        """
        Collects social media statistics for various cryptocurrencies.
        """
        coin_list = ['BTC', 'ETH', 'LTC', 'XRP', 'ADA', 'DOT', 'LINK', 'XLM', 'DOGE', 'BNB', 
                     'SOL', 'XMR', 'VET', 'XTZ', 'MIOTA', 'ATOM', 'AAVE', 'UNI', 'ALGO', 'FIL']

        for coin in coin_list:
            print(f"Collecting social stats for {coin}...")
            social_stats = self.client.social_stats(coin)
            if social_stats:
                social_stats['coin'] = coin
                self.db_operations.insert_data_into_mongodb("social_stats", social_stats)
            else:
                print(f"Failed to collect social stats for {coin}")

    def consolidate_data(self):
        """
        Consolidates market data, mining data, and social stats into a single DataFrame.
        """
        # Fetch data from MongoDB
        market_data = self.db_operations.fetch_data_from_mongodb("market_data")
        mining_data = self.db_operations.fetch_data_from_mongodb("mining_data")
        social_stats = self.db_operations.fetch_data_from_mongodb("social_stats")

        # Preprocess and align data
        # Note: This is a simplified example. You'll need to adjust this based on the actual data structure.
        market_data['date'] = pd.to_datetime(market_data['time'], unit='s')
        mining_data['date'] = pd.to_datetime(mining_data['timestamp'], unit='s')
        social_stats['date'] = pd.to_datetime(social_stats['timestamp'], unit='s')

        # Merge data
        consolidated_data = market_data.merge(mining_data, on=['coin', 'date'], how='left')
        consolidated_data = consolidated_data.merge(social_stats, on=['coin', 'date'], how='left')

        # Insert consolidated data into MongoDB
        self.db_operations.insert_data_into_mongodb("coin_modeling_data", consolidated_data.to_dict('records'))

# Usage example:
data_collector = DataCollector()
# data_collector.collect_market_data()
# data_collector.collect_mining_data()
data_collector.collect_social_stats()
# data_collector.consolidate_data()
