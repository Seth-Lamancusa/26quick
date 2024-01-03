import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from generate_lm import generate_lm
from generate_plots import generate_plots


def generate_agg_data(sessions):
    dfs = []

    # Reading and appending data from each session
    for session in sessions:
        df = pd.read_csv(
            f"analysis/session_{session}/data/session.csv",
            parse_dates=["Run Start Time"],
        )
        dfs.append(df)

    # Concatenating all dataframes
    df = pd.concat(dfs)

    # Calculating summary statistics
    total_runs = len(df)
    mean_time = df["Total Time Taken (ms)"].mean()
    median_time = df["Total Time Taken (ms)"].median()
    best_time = df["Total Time Taken (ms)"].min()
    worst_time = df["Total Time Taken (ms)"].max()
    quantile_25_time = df["Total Time Taken (ms)"].quantile(0.25)
    quantile_75_time = df["Total Time Taken (ms)"].quantile(0.75)

    mean_mistakes = df["Total Mistakes"].mean()
    median_mistakes = df["Total Mistakes"].median()
    least_mistakes = df["Total Mistakes"].min()
    most_mistakes = df["Total Mistakes"].max()
    quantile_25_mistakes = df["Total Mistakes"].quantile(0.25)
    quantile_75_mistakes = df["Total Mistakes"].quantile(0.75)

    # Writing summary statistics to a file
    with open("analysis/aggregate/summary.txt", "w") as file:
        file.write("Aggregate Summary Statistics\n\n")
        file.write(f"Total Runs: {total_runs}\n\n")
        file.write("Mean Time Taken (ms): {:.2f}\n".format(mean_time))
        file.write("Median Time Taken (ms): {:.2f}\n".format(median_time))
        file.write("Best Time Taken (ms): {:.2f}\n".format(best_time))
        file.write("Worst Time Taken (ms): {:.2f}\n".format(worst_time))
        file.write("25th Quantile Time Taken (ms): {:.2f}\n".format(quantile_25_time))
        file.write("75th Quantile Time Taken (ms): {:.2f}\n\n".format(quantile_75_time))
        file.write("Mean Mistakes: {:.2f}\n".format(mean_mistakes))
        file.write("Median Mistakes: {:.2f}\n".format(median_mistakes))
        file.write("Least Mistakes: {:.2f}\n".format(least_mistakes))
        file.write("Most Mistakes: {:.2f}\n".format(most_mistakes))
        file.write("25th Quantile Mistakes: {:.2f}\n".format(quantile_25_mistakes))
        file.write("75th Quantile Mistakes: {:.2f}\n".format(quantile_75_mistakes))

    # Creating the plot
    fig, ax1 = plt.subplots()

    # Calculating median values for each session and num 0-mistake runs
    medians_time_taken = [df["Total Time Taken (ms)"].median() for df in dfs]
    medians_mistakes = [df["Total Mistakes"].median() for df in dfs]
    nom = [df["Total Mistakes"].value_counts().get(0, 0) for df in dfs]

    # Plotting Median Total Time Taken
    ax1.set_xlabel("Session")
    ax1.set_ylabel("Median Total Time Taken (ms)", color="tab:blue")
    ax1.plot(sessions, medians_time_taken, color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    # Creating a second y-axis for Median Total Mistakes
    ax2 = ax1.twinx()
    ax2.set_ylabel("Median Total Mistakes", color="tab:red")
    ax2.plot(sessions, medians_mistakes, color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")

    # Finalizing and saving the plot
    fig.tight_layout()
    plt.savefig("analysis/aggregate/vis/agg_plot.png")

    # Clearing the plot
    plt.clf()

    # Scatter
    colors = plt.cm.rainbow(np.linspace(0, 1, len(dfs)))
    for df, color in zip(dfs, colors):
        plt.scatter(df["Total Mistakes"], df["Total Time Taken (ms)"], color=color, s=3)

    plt.xlabel("Total Mistakes")
    plt.ylabel("Total Time Taken (ms)")
    plt.title("Time Taken vs Mistakes Made by Session")
    plt.legend(["Session " + str(i) for i in range(1, len(dfs) + 1)])

    fig.tight_layout()
    plt.savefig("analysis/aggregate/vis/scatter.png")

    plt.clf()

    # 0-mistake runs by session
    plt.plot(sessions, nom)
    plt.xlabel("Session")
    plt.ylabel("Number 0-mistake runs")
    plt.savefig("analysis/aggregate/vis/nom.png")

    print("Aggregate data generated successfully.")


upr = 14

generate_agg_data([str(i) for i in range(1, upr)])
generate_lm(
    predictor="Total Mistakes",
    response="Total Time Taken (ms)",
    output_folder_name="time_given_mistakes",
    agg=True,
    sessions=[str(i) for i in range(1, upr)],
)
generate_lm(
    predictor="Layout Difficulty",
    response="Total Time Taken (ms)",
    output_folder_name="time_given_diff",
    agg=True,
    sessions=[str(i) for i in range(1, upr)],
)
generate_plots(agg=True, sessions=[str(i) for i in range(1, upr)])
