import os
import math
import pandas as pd
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


def generate_plots(agg=False, session_ID=None, sessions=None):
    if agg:
        dfs = []

        # Reading and appending data from each session
        for session in sessions:
            df = pd.read_csv(
                f"analysis/session_{session}/data/session.csv",
                parse_dates=["Run Start Time"],
            )
            dfs.append(df)

        # Concatenating all dataframes
        df = pd.concat(dfs, ignore_index=True)
        df.sort_values(by=["Run Start Time"], inplace=True)
    else:
        df = pd.read_csv(
            f"analysis/session_{session_ID}/data/session.csv",
            parse_dates=["Run Start Time"],
        )

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
    if agg:
        plt.savefig("analysis/aggregate/vis/performance_plot.png")
    else:
        plt.savefig(
            os.path.join(f"analysis/session_{session_ID}/vis", "performance_plot.png")
        )
    plt.clf()

    # Create Q-Q plots
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Q-Q plot for "Total Time Taken (ms)"
    stats.probplot(df["Total Time Taken (ms)"], dist="norm", plot=axs[0])
    axs[0].get_lines()[0].set_color("blue")
    axs[0].set_title("Q-Q Plot for Total Time Taken (ms)")

    # Q-Q plot for "Total Mistakes"
    stats.probplot(df["Total Mistakes"], dist="norm", plot=axs[1])
    axs[1].get_lines()[0].set_color("red")
    axs[1].set_title("Q-Q Plot for Total Mistakes")

    # Make reference lines black
    for ax in axs:
        ax.get_lines()[1].set_color("black")

    # Adjusting layout and saving the figure
    plt.tight_layout()
    if agg:
        plt.savefig("analysis/aggregate/vis/qq_plot.png")
    else:
        plt.savefig(f"analysis/session_{session_ID}/vis/qq_plot.png")

    # Create histograms
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Histogram for "Total Time Taken (ms)"
    bin_edges = np.arange(
        math.floor(df["Total Time Taken (ms)"].min() / 1000) * 1000,
        math.ceil(df["Total Time Taken (ms)"].max() / 1000) * 1000,
        1000,
    )
    axs[0].hist(df["Total Time Taken (ms)"], bins=bin_edges, color="blue")
    axs[0].set_title("Histogram for Total Time Taken (ms)")
    axs[0].set_xlabel("Total Time Taken (ms)")
    axs[0].set_ylabel("Frequency")

    # Histogram for "Total Mistakes"
    d = np.diff(np.unique(df["Total Mistakes"])).min()
    left_of_first_bin = df["Total Mistakes"].min() - float(d) / 2
    right_of_last_bin = df["Total Mistakes"].max() + float(d) / 2
    axs[1].hist(
        df["Total Mistakes"],
        np.arange(left_of_first_bin, right_of_last_bin + d, d),
        color="red",
    )
    axs[1].set_title("Histogram for Total Mistakes")
    axs[1].set_xlabel("Total Mistakes")
    axs[1].set_ylabel("Frequency")

    # Adjusting layout and saving the figure
    plt.tight_layout()
    if agg:
        plt.savefig("analysis/aggregate/vis/histograms.png")
    else:
        plt.savefig(f"analysis/session_{session_ID}/vis/histograms.png")

    print(f"Generated plots for session {session_ID}")
