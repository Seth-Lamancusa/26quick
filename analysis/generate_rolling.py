import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_rolling(session_ID, window_size):
    # Load session data from CSV file
    session_data = pd.read_csv(f"analysis/data/session_{session_ID}/session.csv")

    # Calculate rolling averages
    session_data["Total Time Taken (ms) Rolling"] = (
        session_data["Total Time Taken (ms)"].rolling(window=window_size).mean()
    )
    session_data["Total Mistakes Rolling"] = (
        session_data["Total Mistakes"].rolling(window=window_size).mean()
    )

    # Generate plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plotting Total Time Taken
    ax1.plot(
        session_data.index,
        session_data["Total Time Taken (ms) Rolling"],
        color="blue",
        label="Rolling Avg Time",
    )
    ax1.set_xlabel("Run Number")
    ax1.set_ylabel("Total Time Taken (ms)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Creating a secondary y-axis for Total Mistakes
    ax2 = ax1.twinx()
    ax2.plot(
        session_data.index,
        session_data["Total Mistakes Rolling"],
        color="red",
        label="Rolling Avg Mistakes",
    )
    ax2.set_ylabel("Total Mistakes", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Adding a title and a legend
    plt.title("Session Data with Rolling Averages")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Create output folder and subfolder if they don't exist
    rolling_folder = os.path.join(f"analysis/data/session_{session_ID}", "rolling")
    if not os.path.exists(rolling_folder):
        os.makedirs(rolling_folder)

    # Save the plot
    plot_file_path = os.path.join(rolling_folder, f"rolling_{window_size}.png")
    plt.savefig(plot_file_path)

    return plot_file_path
