import csv
import json
import os
from datetime import datetime

# Define the relative path to the input json file
input_json_path = "analysis/data/localStorage_2023-11-07_22-37-21.json"
output_folder = "analysis/data"

# Load the JSON data from the file
with open(input_json_path, "r") as f:
    data = json.load(f)

# Filter out non-datetime keys
data = {k: v for k, v in data.items()}

# Process the data based on its type
processed_data = []
for k, v in data.items():
    # Remove timezone information (assuming it's always at the end)
    cleaned_date = k.split(" (")[0]

    if v in ["start", "end"]:
        processed_data.append([k, "N/A", "N/A", v, "N/A", "N/A"])
    else:
        processed_data.append([k] + v.split(","))

# Sort the data by datetime
sorted_data = sorted(
    processed_data, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S.%f")
)

# Name output file based on input file name
if input_json_path.split("data/")[1].startswith(
    "localStorage_"
) and input_json_path.endswith(".json"):
    # Replace 'localStorage' with 'output' and change the extension to '.csv' (expires in 10 years)
    output_filename = (
        "raw"
        + input_json_path[len(input_json_path.split("_")[0]) : -len(".json")]
        + ".csv"
    )
else:
    raise ValueError("Filename does not match expected pattern.")

csv_file_path = os.path.join(output_folder, output_filename)
with open(csv_file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Datetime", "Key", "Number", "Action", "Time", "Mistakes"])
    writer.writerows(sorted_data)

print(f"Data processed and saved to {csv_file_path}")
