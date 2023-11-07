import os
import csv
import pandas as pd
from datetime import datetime

# Define the path to the input and output CSV files
input_csv_path = "analysis/data/raw_2023-11-07_22-37-21.csv"
output_folder = "analysis/data"

# Read and sort the data
data = pd.read_csv(input_csv_path, parse_dates=["Datetime"])
data.sort_values("Datetime", inplace=True)

# Prepare the output data
output_data = []
current_run = {}
for index, row in data.iterrows():
    if row["Action"] == "start":
        # Start a new run
        current_run = {"Run Start Time": row["Datetime"]}
    elif row["Action"] == "end":
        # End of the current run
        current_run["Run End Time"] = row["Datetime"]
        current_run["Total Time Taken (ms)"] = (
            current_run["Run End Time"] - current_run["Run Start Time"]
        ).total_seconds() * 1000
        output_data.append(current_run)
    else:
        current_run["Total Mistakes"] = row["Mistakes"]

# Convert the output data to a pandas DataFrame
output_df = pd.DataFrame(output_data)

# Reorder the output DataFrame columns
output_df = output_df[
    ["Run Start Time", "Run End Time", "Total Time Taken (ms)", "Total Mistakes"]
]

# Name output file based on input file name
if input_csv_path.split("data/")[1].startswith("raw_") and input_csv_path.endswith(
    ".csv"
):
    # Replace 'raw' with 'session' and change the extension to '.csv'
    output_filename = (
        "session"
        + input_csv_path[len(input_csv_path.split("_")[0]) : -len(".csv")]
        + ".csv"
    )
else:
    raise ValueError("Filename does not match expected pattern.")

output_csv_path = os.path.join(output_folder, output_filename)
output_df.to_csv(output_csv_path, index=False)

print(f"Processed data has been saved to {output_csv_path}")
