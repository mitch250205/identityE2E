# test_data.py
import re
import json

class GetTestData:
    def __init__(self,input_file_path=None, output_file_path=None):
        """Initialize the test data"""
        self.test_data = [
            ("AB12CDE", "Car Model A"),
            ("XY34ZTG", "Car Model B"),
            ("LM56OPQ", "Car Model C"),
        ]
        self.test_data_json = {}
        self.test_output_data_json = {}

        # Process the file if a path is provided
        if input_file_path:
            self.process_car_data_text_file(input_file_path)

        if output_file_path:
            self.get_output_fle_create_json(output_file_path)


    def get_data(self):
        """Return the test data as a list"""
        return self.test_data

    def add_data(self, number_plate, expected_details):
        """Dynamically add new test data"""
        self.test_data.append((number_plate, expected_details))

    def get_specific_data(self, index):
        """Fetch a specific test case by index"""
        if 0 <= index < len(self.test_data):
            return self.test_data[index]
        raise IndexError("Invalid index. Out of range.")

    def get_output_fle_create_json(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Extract headers
            headers = lines[0].strip().split(",")

            # Process each line and store as a dictionary
            data_list = []
            for line in lines[1:]:  # Skip the header row
                values = line.strip().split(",")
                data_list.append(dict(zip(headers, values)))

            # Store JSON object
            self.car_data_json = {"cars": data_list}

        except Exception as e:
            print(f"Error processing file: {e}")

    def process_car_data_text_file(self, file_path):
        """Process the input text file and extract car registration numbers with their values."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Regex pattern to extract car registration numbers (common UK formats)
            reg_pattern = r'\b[A-Z]{2}[0-9]{2} [A-Z]{3}\b'
            reg_numbers = re.findall(reg_pattern, content)

            # Regex to extract prices (simplified for this context)
            price_pattern = r'£(\d{1,3}(?:,\d{3})*)'  # Matches values like £3,000 or £10k
            prices = re.findall(price_pattern, content)

            # Convert "10k" values to actual numbers (if applicable)
            processed_prices = [int(price.replace(",", "")) if price.isdigit() else int(price[:-1]) * 1000 for price in prices]

            # Creating JSON structure
            self.test_data_json = {}
            for i, reg in enumerate(reg_numbers):
                value = processed_prices[i] if i < len(processed_prices) else "Unknown"
                self.test_data_json[reg] = {"registration": reg, "estimated_value": value}

        except Exception as e:
            print(f"Error processing file: {e}")

    def get_test_data_json(self):
        """Return test data in JSON format"""
        return json.dumps(self.test_data_json, indent=4)

