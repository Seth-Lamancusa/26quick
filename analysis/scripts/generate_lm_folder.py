import os
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt


def generate_lm_folder(
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
                f"analysis/data/{session}/session.csv",
                parse_dates=["Run Start Time"],
            )
            dfs.append(df)

        # Concatenating all dataframes
        df = pd.concat(dfs)
    else:
        df = pd.read_csv(f"analysis/data/{session_ID}/session.csv")

    # Prepare data for statsmodel, fit and predict
    X = df[[predictor]]  # Predictor variable(s)
    y = df[response]  # Response variable
    X = sm.add_constant(X)  # Add a constant (intercept term)
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)

    # Plot
    plt.clf()
    plt.figure(figsize=(10, 6))

    # Add labels
    plt.xlabel(predictor)
    plt.ylabel(response)
    plt.title(f"{response} vs {predictor}")

    plt.scatter(df[predictor], y, color="blue", alpha=0.5)
    plt.plot(df[predictor], predictions, color="red")  # Regression line

    intercept = model.params[0]
    p_value_int = model.pvalues[0]
    slope = model.params[1]
    p_value_slope = model.pvalues[1]

    plt.text(
        0.05,
        0.95,
        f"intercept = {intercept:.3f}, p={round(p_value_int, 3)}",
        transform=plt.gca().transAxes,
    )
    plt.text(
        0.05,
        0.90,
        f"slope = {slope:.3f}, p={round(p_value_slope, 3)}",
        transform=plt.gca().transAxes,
    )

    # Save the plot
    if agg:
        output_folder = os.path.join("analysis/aggregate_insights", output_folder_name)
    else:
        output_folder = os.path.join(
            f"analysis/session_insights/session_{session_ID}/vis", output_folder_name
        )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, "plot.png"))
    plt.close()

    # Create and save a summary .txt file with model parameters
    output_file_name = "summary.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        file.write(model.summary().as_text())

    print(f"Linear regression saved to {output_folder}")
