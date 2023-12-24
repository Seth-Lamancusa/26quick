import os
import csv
import json
from datetime import datetime


# Convert raw data from localStorage json data to csv
def localStorage_to_raw(session_ID):
    # Load the JSON data from the file
    with open(f"analysis/data/session_{session_ID}/localStorage.json", "r") as f:
        data = json.load(f)

    # Filter out non-datetime keys
    data = {k: v for k, v in data.items()}

    # Process the data based on its type
    processed_data = []
    for k, v in data.items():
        if v in ["start", "end"]:
            processed_data.append([k, "N/A", "N/A", v, "N/A", "N/A"])
        else:
            processed_data.append([k] + v.split(","))

    # Sort the data by datetime
    sorted_data = sorted(
        processed_data, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S.%f")
    )

    csv_file_path = os.path.join(f"analysis/data/session_{session_ID}", "raw.csv")
    with open(csv_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Datetime", "Key", "Number", "Action", "Time", "Mistakes"])
        writer.writerows(sorted_data)

    print(f"Raw data saved to {csv_file_path}")
    return csv_file_path
