import os
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt


def generate_lm(
    predictor,
    response,
    output_folder_name,
    agg=False,
    sessions=None,
    session_ID=None,
):
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
        df = pd.concat(dfs)
    else:
        df = pd.read_csv(f"analysis/session_{session_ID}/data/session.csv")

    # Clear the plot
    plt.clf()

    # Prepare the data for statsmodels
    X = df[[predictor]]  # Predictor variable(s)
    y = df[response]  # Response variable
    X = sm.add_constant(X)  # Add a constant (intercept term)

    # Fit the model using statsmodels
    model = sm.OLS(y, X).fit()

    # Make predictions
    predictions = model.predict(X)

    # Plot the actual data and the regression line
    plt.scatter(df[predictor], y, color="blue")  # Actual points
    plt.plot(df[predictor], predictions, color="red")  # Regression line

    if agg:
        output_folder = os.path.join("analysis/aggregate", output_folder_name)
    else:
        output_folder = os.path.join(
            f"analysis/session_{session_ID}/vis", output_folder_name
        )

    # Annotate plot with p value and parameter values from model summary
    intercept = model.params[0]
    p_value_int = model.pvalues[0]
    slope = model.params[1]
    p_value_slope = model.pvalues[1]
    plt.annotate(
        f"intercept = {intercept:.3f}, p={round(p_value_int, 3)}",
        xy=(0.05, 0.9),
        xycoords="axes fraction",
    )
    plt.annotate(
        f"slope = {slope:.3f}, p={round(p_value_slope, 3)}",
        xy=(0.05, 0.85),
        xycoords="axes fraction",
    )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, "plot.png"))
    plt.close()

    # Create a summary .txt file with model parameters
    output_file_name = "summary.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        file.write(model.summary().as_text())

    print(f"Linear regression saved to {output_folder}")
