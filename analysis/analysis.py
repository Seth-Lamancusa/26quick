import csv
import json
import os
from datetime import datetime

DATAFILE = "localStorage_2023-11-02_22-00-29.json"  # replace 'your_json_filename.json' with your actual file name

# Define the relative path to the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_dir, "data")
json_file_path = os.path.join(data_folder, DATAFILE)

# Load the JSON data from the file
with open(json_file_path, "r") as f:
    data = json.load(f)

# Filter out non-datetime keys
data = {k: v for k, v in data.items() if "GMT" in k}

# Process the data based on its type
processed_data = []
for k, v in data.items():
    # Remove timezone information (assuming it's always at the end)
    cleaned_date = k.split(" (")[0]

    if v in ["start", "end"]:
        processed_data.append([cleaned_date, "N/A", "N/A", v, "N/A", "N/A"])
    else:
        processed_data.append([cleaned_date] + v.split(","))

# Sort the data by datetime
sorted_data = sorted(
    processed_data, key=lambda x: datetime.strptime(x[0], "%a %b %d %Y %H:%M:%S %Z%z")
)

# Write to CSV
csv_file_path = os.path.join(data_folder, "output.csv")
with open(csv_file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Datetime", "Key", "Number", "Action", "Time", "Mistakes"])
    writer.writerows(sorted_data)

print(f"Data processed and saved to {csv_file_path}")
