import os
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt


def generate_lm(session_ID, output_folder_name, predictor, response):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(f"analysis/data/session_{session_ID}/session.csv")

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
    output_folder = os.path.join(
        f"analysis/data/session_{session_ID}", output_folder_name
    )
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    plt.savefig(os.path.join(output_folder, "plot.png"))

    # Create a summary .txt file with model parameters
    output_file_name = "summary.txt"
    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, "w") as file:
        file.write(model.summary().as_text())

    print(f"Linear regression saved to {output_folder}")
