import pandas as pd
import os


def generate_text_summary(agg=False, session_ID=None, sessions=None):
    if agg:
        dfs = []

        # Reading and appending data from each session
        for session in sessions:
            df = pd.read_csv(f"analysis/data/{session}/session.csv")
            dfs.append(df)

        # Concatenating all dataframes
        df = pd.concat(dfs)
    else:
        df = pd.read_csv(f"analysis/data/{session_ID}/session.csv")

    # Calculate the required statistics for 'Total Time Taken (ms)'
    mean_time = df["Total Time Taken (ms)"].mean()
    best_time = df["Total Time Taken (ms)"].min()
    worst_time = df["Total Time Taken (ms)"].max()

    # Calculate the required statistics for 'Total Mistakes'
    mean_mistakes = df["Total Mistakes"].mean()
    best_mistakes = df["Total Mistakes"].min()
    worst_mistakes = df["Total Mistakes"].max()

    # Calculate number of 0-mistake runs
    nom = df["Total Mistakes"].value_counts().get(0, 0)

    # Output
    if agg:
        output_file_path = "analysis/aggregate_insights/summary.txt"
    else:
        output_file_path = f"analysis/session_insights/session_{session_ID}/summary.txt"
    output_dir = os.path.dirname(output_file_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_file_path, "w") as file:
        file.write(f"Summary Statistics for session_{session_ID}\n")
        file.write("\n")
        file.write(f"Total Runs: {len(df)}\n")
        file.write(f"Total 0-mistake Runs: {nom}\n")
        file.write("\n")
        file.write(f"Mean Time Taken (ms): {mean_time}\n")
        file.write(f'Standard Deviation: {df["Total Time Taken (ms)"].std()}\n')
        file.write("\n")
        file.write(f"Best Time Taken (ms): {best_time}\n")
        file.write(f"Worst Time Taken (ms): {worst_time}\n")
        file.write("\n")
        file.write(f"Mean Mistakes: {mean_mistakes}\n")
        file.write(f'Standard Deviation: {df["Total Mistakes"].std()}\n')
        file.write("\n")
        file.write(f"Least Mistakes: {best_mistakes}\n")
        file.write(f"Most Mistakes: {worst_mistakes}\n")
        file.write("\n")

    print(f"Summary file created: {output_file_path}")
    return output_file_path
