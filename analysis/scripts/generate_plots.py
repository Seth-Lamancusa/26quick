import os
import math
import pandas as pd
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt


# Histograms, Q-Q plots, and performance plot
def generate_plots(agg=False, session_ID=None, sessions=None):
    if agg:
        dfs = []

        # Reading and appending data from each session
        for session in sessions:
            df = pd.read_csv(
                f"analysis/data/{session}/session.csv",
                parse_dates=["Run Start Time"],
            )
            dfs.append(df)

        # Concatenating all dataframes
        df = pd.concat(dfs, ignore_index=True)
        df.sort_values(by=["Run Start Time"], inplace=True)

        output_dir = "analysis/aggregate_insights/vis"
    else:
        df = pd.read_csv(
            f"analysis/data/{session_ID}/session.csv",
            parse_dates=["Run Start Time"],
        )

        output_dir = f"analysis/session_insights/session_{session_ID}/vis"

    # Plots by analysis type
    if not agg:
        # Performance over all runs
        fig, ax1 = plt.subplots()

        ax1.plot(
            df.index,
            df["Total Time Taken (ms)"],
            color="b",
            label="Total Time Taken (ms)",
        )
        ax1.set_xlabel("Run Number")
        ax1.set_ylabel("Total Time Taken (ms)", color="b")
        ax1.tick_params("y", colors="b")

        ax2 = ax1.twinx()
        ax2.plot(df.index, df["Total Mistakes"], color="r", label="Total Mistakes")
        ax2.set_ylabel("Total Mistakes", color="r")
        ax2.tick_params("y", colors="r")

        plt.title("Performance Over Runs")
        fig.tight_layout()

        plt.savefig(os.path.join(output_dir, "performance_over_runs.png"))
    else:
        # Performance by session
        plt.clf()
        plt.figure(figsize=(12, 6))
        fig, ax1 = plt.subplots()

        means_time_taken = [d["Total Time Taken (ms)"].mean() for d in dfs]

        ax1.set_xlabel("Session number")
        ax1.set_ylabel("Median Total Time Taken (ms)", color="tab:blue")
        ax1.plot(sessions, means_time_taken, color="tab:blue")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        ax2 = ax1.twinx()
        ax2.set_ylabel("Mean Total Mistakes", color="tab:red")
        ax2.plot(
            sessions,
            [d["Total Mistakes"].mean() for d in dfs],
            color="tab:red",
        )
        ax2.tick_params(axis="y", labelcolor="tab:red")

        selected_ticks = sessions[::3]  # This selects every other element
        ax1.set_xticks(selected_ticks)

        # Creating third y-axis for mistake chains
        # ax3 = ax1.twinx()
        # ax3.set_ylabel("Average number of Mistake chains", color="tab:green")
        # ax3.plot(sessions, [df["Mistake Chains"].mean() for df in dfs], color="tab:green")
        # ax3.tick_params(axis="y", labelcolor="tab:green")

        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, "performance_by_session.png"))

        # Scatter
        plt.clf()
        fig, ax = plt.subplots()

        colors = plt.cm.rainbow(np.linspace(0, 1, len(dfs)))

        for _, (d, color) in enumerate(zip(dfs, colors), start=1):
            ax.scatter(
                d["Total Mistakes"],
                d["Total Time Taken (ms)"],
                color=color,
                s=3,
                alpha=0.5,
            )  # Semi-transparent points

        plt.xlabel("Total Mistakes")
        plt.ylabel("Total Time Taken (ms)")
        plt.title("Time Taken vs Mistakes Made by Session")

        sm = plt.cm.ScalarMappable(cmap=plt.cm.rainbow, norm=plt.Normalize(1, len(dfs)))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label("Session Number")

        cbar.set_ticks(np.linspace(1, len(dfs), num=3))
        cbar.set_ticklabels([1, len(dfs) // 2, len(dfs)])

        fig.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatter.png"))

        # 0-mistake runs by session
        plt.clf()
        plt.figure(figsize=(12, 6))

        nom = [d["Total Mistakes"].value_counts().get(0, 0) for d in dfs]
        plt.plot(sessions, nom, marker="o")

        plt.xlabel("Session")
        plt.ylabel("Number of 0-mistake runs")
        plt.title("0-Mistake Runs Across Sessions")
        plt.xticks(rotation=45)
        plt.tight_layout()  # Adjust layout to fit everything nicely

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        plt.savefig(os.path.join(output_dir, "0_mistake_runs.png"))

    # Q-Q plots
    plt.clf()
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    stats.probplot(df["Total Time Taken (ms)"], dist="norm", plot=axs[0])
    axs[0].get_lines()[0].set_color("blue")
    axs[0].set_title("Q-Q Plot for Total Time Taken (ms)")

    stats.probplot(df["Total Mistakes"], dist="norm", plot=axs[1])
    axs[1].get_lines()[0].set_color("red")
    axs[1].set_title("Q-Q Plot for Total Mistakes")

    for ax in axs:
        ax.get_lines()[1].set_color("black")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "qq_plots.png"))

    # Histograms
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    bin_edges = np.arange(
        math.floor(df["Total Time Taken (ms)"].min() / 1000) * 1000,
        math.ceil(df["Total Time Taken (ms)"].max() / 1000) * 1000,
        1000,
    )
    axs[0].hist(df["Total Time Taken (ms)"], bins=bin_edges, color="blue")
    axs[0].set_title("Histogram for Total Time Taken (ms)")
    axs[0].set_xlabel("Total Time Taken (ms)")
    axs[0].set_ylabel("Frequency")

    max_mistakes = df["Total Mistakes"].max()
    axs[1].hist(
        df["Total Mistakes"],
        bins=np.arange(-0.5, max_mistakes + 1.5, 1),
        color="red",
    )
    bin_centers = np.arange(0, max_mistakes + 1, 1)
    axs[1].set_xticks(bin_centers)
    axs[1].set_title("Histogram for Total Mistakes")
    axs[1].set_xlabel("Total Mistakes")
    axs[1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "histograms.png"))

    # Confirmation message
    if agg:
        print("Generated plots for aggregate insights")
    else:
        print(f"Generated plots for session {session_ID}")
