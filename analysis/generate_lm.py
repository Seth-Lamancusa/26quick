import os
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


def generate_lm(input_path, output_folder):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(input_path)

    # Create a linear regression model and plot it
    model = LinearRegression()
    xs = df["Total Mistakes"].values.reshape(-1, 1)
    ys = df["Total Time Taken (ms)"].values.reshape(-1, 1)
    model.fit(xs, ys)
    predictions = model.predict(xs)
    plt.scatter(xs, ys, color="blue")  # Actual points
    plt.plot(xs, predictions, color="red")  # Regression line
    output_folder = output_folder + "/time_given_mistakes"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, "mistakes-time_plot.png"))

    # Calculate t statistics and p values for the model
    xs = sm.add_constant(xs)
    sm_model = sm.OLS(ys, xs).fit()

    # Create a summary .txt file with model parameters and coefficient of determination
    output_file_name = "summary.txt"
    output_file_path = f"{output_folder}/{output_file_name}"
    with open(output_file_path, "w") as file:
        file.write(sm_model.summary().as_text())

    print(f"Linear regression plot saved to {output_folder}")
