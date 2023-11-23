import os
import pandas as pd


### Generate .txt summary
# Input path is session data
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

    print(f"Summary file created: {output_file_path}")
    return output_file_path
