import json
import os
import logging

class StorageManager:
    def __init__(self):
        """Initialize the storage manager with basic setup."""
        self.data_directory = 'data'
        self._ensure_data_directory()
        self._setup_logging()

    def _ensure_data_directory(self):
        """Ensures the data directory exists."""
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def _setup_logging(self):
        """Sets up basic logging for debugging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )

    def load_data(self, filename):
        """Loads data from a JSON file with error handling."""
        filepath = os.path.join(self.data_directory, filename)
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    logging.info(f"Successfully loaded {filename}")
                    return data
            else:
                logging.info(f"File {filename} not found, creating empty list")
                return []
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {filename}: {e}")
            return []
        except Exception as e:
            logging.error(f"Unexpected error loading {filename}: {e}")
            return []

    def save_data(self, filename, data):
        """Saves data to a JSON file with error handling."""
        filepath = os.path.join(self.data_directory, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
                logging.info(f"Successfully saved {filename}")
        except Exception as e:
            logging.error(f"Error saving {filename}: {e}")
            raise 