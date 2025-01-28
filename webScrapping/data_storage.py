import pandas as pd

class DataStorage:
    def __init__(self, filename):
        self.filename = filename
        self.data = []
        self.load_existing_data()  # Load existing data if any
    
    def load_existing_data(self):
        """Load existing data from a CSV file."""
        try:
            self.data = pd.read_csv(self.filename).to_dict(orient='records')
        except FileNotFoundError:
            print(f"No existing data file found at {self.filename}. Starting fresh.")
            self.data = []  # Start with an empty list if the file doesn't exist

    def save_record(self, record):
        """Append a new record to the CSV file."""
        self.data.append(record)  # Add the new record to the list
        pd.DataFrame(self.data).to_csv(self.filename, index=False)  # Write all data to CSV
        print(f"Record saved: {record}")

    def record_exists(self, record):
        """Check if a record already exists in the data."""
        for existing_record in self.data:
            if existing_record['id'] == record['id'] or existing_record['price'] == record['price']:
                return True
        return False
