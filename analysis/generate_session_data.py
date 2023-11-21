import os
import csv
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt


# Define the relative path to the input json file
input_file_path = "analysis/data/session_4/localStorage_2023-11-10_04-29-45.json"
output_folder = "analysis/data/session_4"


# Convert raw data from localStorage json data to csv
def localStorage_to_raw(input_file_path, output_folder):
    # Load the JSON data from the file
    with open(input_file_path, "r") as f:
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

    # Name output file based on input file name and write
    output_filename = "raw" + input_file_path[36 : -len(".json")] + ".csv"
    csv_file_path = os.path.join(output_folder, output_filename)
    with open(csv_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Datetime", "Key", "Number", "Action", "Time", "Mistakes"])
        writer.writerows(sorted_data)

    print(f"Raw data saved to {csv_file_path}")
    return csv_file_path


### Get session data from raw data
def raw_to_session(input_file_path, output_folder, outlier_threshold=(25000, 10)):
    # Read and sort the data
    data = pd.read_csv(input_file_path, parse_dates=["Datetime"])
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
            run_end_time = row["Datetime"]
            current_run["Total Time Taken (ms)"] = (
                run_end_time - current_run["Run Start Time"]
            ).total_seconds() * 1000
            output_data.append(current_run)
        else:
            current_run["Total Mistakes"] = row["Mistakes"]

    # Remove outliers
    output_data = [
        row
        for row in output_data
        if (
            float(row["Total Time Taken (ms)"]) < outlier_threshold[0]
            and float(row["Total Mistakes"]) < outlier_threshold[1]
        )
    ]

    # Convert the output data to a pandas DataFrame
    output_df = pd.DataFrame(output_data)

    # Reorder the output DataFrame columns
    output_df = output_df[["Run Start Time", "Total Time Taken (ms)", "Total Mistakes"]]

    # Name output file based on input file name
    output_filename = "session" + input_file_path[27 : -len(".csv")] + ".csv"

    output_csv_path = os.path.join(output_folder, output_filename)
    output_df.to_csv(output_csv_path, index=False)

    print(f"Session data saved to {output_csv_path}")
    return output_csv_path


### Generate .txt summary
def generate_text_summary(input_file_path, output_folder):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(input_file_path)

    # Calculate the required statistics for 'Total Time Taken (ms)'
    mean_time = df["Total Time Taken (ms)"].mean()
    median_time = df["Total Time Taken (ms)"].median()
    best_time = df["Total Time Taken (ms)"].min()
    worst_time = df["Total Time Taken (ms)"].max()
    quantile_25_time = df["Total Time Taken (ms)"].quantile(0.25)
    quantile_75_time = df["Total Time Taken (ms)"].quantile(0.75)

    # Calculate the required statistics for 'Total Mistakes'
    mean_mistakes = df["Total Mistakes"].mean()
    median_mistakes = df["Total Mistakes"].median()
    best_mistakes = df["Total Mistakes"].min()
    worst_mistakes = df["Total Mistakes"].max()
    quantile_25_mistakes = df["Total Mistakes"].quantile(0.25)
    quantile_75_mistakes = df["Total Mistakes"].quantile(0.75)

    # Calculate correlation between mistakes and time
    correlation = df["Total Time Taken (ms)"].corr(df["Total Mistakes"])

    # Format output filename based on input filename
    input_file_name = os.path.basename(input_file_path)
    date_time_str = input_file_name.replace("session_", "").replace(".csv", "")
    output_file_name = f"summary_{date_time_str}.txt"
    output_file_path = f"{output_folder}/{output_file_name}"

    # Write the summary statistics to a text file
    with open(output_file_path, "w") as file:
        file.write(f"Summary Statistics for {input_file_name}\n")
        file.write("\n")
        file.write(f"Total Runs: {len(df)}\n")
        file.write("\n")
        file.write(f"Mean Time Taken (ms): {mean_time}\n")
        file.write(f"Median Time Taken (ms): {median_time}\n")
        file.write(f"Best Time Taken (ms): {best_time}\n")
        file.write(f"Worst Time Taken (ms): {worst_time}\n")
        file.write(f"25th Quantile Time Taken (ms): {quantile_25_time}\n")
        file.write(f"75th Quantile Time Taken (ms): {quantile_75_time}\n")
        file.write("\n")
        file.write(f"Mean Mistakes: {mean_mistakes}\n")
        file.write(f"Median Mistakes: {median_mistakes}\n")
        file.write(f"Least Mistakes: {best_mistakes}\n")
        file.write(f"Most Mistakes: {worst_mistakes}\n")
        file.write(f"25th Quantile Mistakes: {quantile_25_mistakes}\n")
        file.write(f"75th Quantile Mistakes: {quantile_75_mistakes}\n")
        file.write("\n")
        file.write(f"Correlation between Time and Mistakes: {correlation}\n")

    print(f"Summary file created: {output_file_path}")
    return output_file_path


def generate_plot(input_file_path, output_folder):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(input_file_path, parse_dates=["Run Start Time"])

    # Create a new figure and a set of subplots
    fig, ax1 = plt.subplots()

    # Plot the 'Total Time Taken (ms)' on y-axis 1
    ax1.plot(
        df.index, df["Total Time Taken (ms)"], color="b", label="Total Time Taken (ms)"
    )
    ax1.set_xlabel("Run Number")
    ax1.set_ylabel("Total Time Taken (ms)", color="b")
    ax1.tick_params("y", colors="b")

    # Create another y-axis for the 'Total Mistakes' sharing the same x-axis
    ax2 = ax1.twinx()
    ax2.plot(df.index, df["Total Mistakes"], color="r", label="Total Mistakes")
    ax2.set_ylabel("Total Mistakes", color="r")
    ax2.tick_params("y", colors="r")

    # Title and legend
    plt.title("Performance Over Runs")
    fig.tight_layout()

    # Save the plot as an image
    plt.savefig(os.path.join(output_folder, "performance_plot.png"))

    # Show the plot (optional, you can remove this if you just want to save the image)
    plt.show()


raw_path = localStorage_to_raw(input_file_path, output_folder)
session_path = raw_to_session(raw_path, output_folder)
summary_path = generate_text_summary(session_path, output_folder)
generate_plot(session_path, output_folder)
