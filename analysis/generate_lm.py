import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


def generate_lm(input_path, output_folder):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(input_path)
    xs = df[["Total Mistakes", "Layout Difficulty"]]
    ys = df["Total Time Taken (ms)"]

    # Create a linear regression model
    model = LinearRegression()
    model.fit(xs, ys)

    # Fit the model using statsmodels to get p-values
    xs_with_constant = sm.add_constant(xs)
    sm_model = sm.OLS(ys, xs_with_constant).fit()
    p_values = sm_model.pvalues
    t_statistics = sm_model.tvalues

    # Annotate with model parameters, R^2, and hypothesis test results
    params_text = f"Intercept: \n{model.intercept_:.2f} (t={t_statistics[0]:.2f}, p={p_values[0]:.2f}), \n"
    params_text += f"Coefficients: \n{model.coef_[0]:.2f} (t={t_statistics[1]:.2f}, p={p_values[1]:.2f}), \n"
    params_text += (
        f"{model.coef_[1]:.2f} (t={t_statistics[2]:.2f}, p={p_values[2]:.2f})"
    )
    r_squared_text = f"Coefficient of determination (R^2): {model.score(xs, ys):.2f}"

    # Create subplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.subplots_adjust(bottom=0.3)  # Adjust these values as needed

    # Create a grid of values and predict Y values for Total Mistakes
    mistakes_range = np.linspace(
        xs["Total Mistakes"].min(), xs["Total Mistakes"].max(), 100
    )
    mistakes_grid = pd.DataFrame(
        {
            "Total Mistakes": mistakes_range,
            "Layout Difficulty": np.mean(xs["Layout Difficulty"]),
        }
    )
    predicted_mistakes = model.predict(mistakes_grid)

    # Plot the regression line for Total Mistakes
    ax[0].plot(mistakes_range, predicted_mistakes, color="red")

    # Create a grid of values and predict Y values for Layout Difficulty
    difficulty_range = np.linspace(
        xs["Layout Difficulty"].min(), xs["Layout Difficulty"].max(), 100
    )
    difficulty_grid = pd.DataFrame(
        {
            "Total Mistakes": np.mean(xs["Total Mistakes"]),
            "Layout Difficulty": difficulty_range,
        }
    )
    predicted_difficulty = model.predict(difficulty_grid)

    # Plot the regression line for Layout Difficulty
    ax[1].plot(difficulty_range, predicted_difficulty, color="red")

    # Scatter plot for Total Mistakes vs Total Time
    ax[0].scatter(xs["Total Mistakes"], ys, color="blue")
    ax[0].set_xlabel("Total Mistakes")
    ax[0].set_ylabel("Total Time Taken (ms)")
    ax[0].set_title("Total Mistakes vs Total Time")

    # Scatter plot for Layout Difficulty vs Total Time
    ax[1].scatter(xs["Layout Difficulty"], ys, color="green")
    ax[1].set_xlabel("Layout Difficulty")
    ax[1].set_title("Layout Difficulty vs Total Time")

    # Annotate with model parameters and R^2
    fig.text(0.5, 0.04, params_text, ha="center", fontsize=9)
    fig.text(0.5, 0.18, r_squared_text, ha="center", fontsize=9)

    # Save the plot
    output_folder = output_folder + "/time_given_mistakes"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, "mistakes-time_plot.png"))

    # Create a summary .txt file with model parameters and coefficient of determination
    output_file_name = "summary.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        file.write(
            f"Model parameters: Intercept = {model.intercept_}, Coefficients = {model.coef_}\n"
        )
        file.write(f"Coefficient of determination (R^2): {model.score(xs, ys)}\n")
        file.write(f"Model parameters and hypothesis test results:\n{params_text}\n")
        file.write(f"Coefficient of determination (R^2): {model.score(xs, ys)}\n")

    print(f"Linear regression plot saved to {output_folder}")
