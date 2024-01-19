import json
from datetime import datetime


def filter_json_by_date(file_path, excluded_day):
    # Load the JSON data from the file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Filter out items with the excluded day
    filtered_data = {
        key: value
        for key, value in data.items()
        if datetime.fromisoformat(key).day != excluded_day
    }

    # Save the filtered data back to a file or return it
    with open("filtered_data.json", "w") as file:
        json.dump(filtered_data, file, indent=4)

    return filtered_data


# Replace 'your_file_path.json' with the path to your JSON file
file_path = "analysis/session_25/data/localStorage.json"
filter_json_by_date(file_path, 17)
