import os
import pandas as pd
from matplotlib import pyplot as plt


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
