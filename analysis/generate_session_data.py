from generate_plot import generate_plot
from generate_text_summary import generate_text_summary
from localStorage_to_raw import localStorage_to_raw
from raw_to_session import raw_to_session
from generate_lm import generate_lm
from generate_rolling import generate_rolling


# Define the relative path to the input json file
input_file_path = "analysis/data/session_3/localStorage_2023-12-22_20-25-18.json"
output_folder = "analysis/data/session_3"

raw_path = localStorage_to_raw(input_file_path, output_folder)
session_path = raw_to_session(raw_path, output_folder)
summary_path = generate_text_summary(session_path, output_folder)
for i in range(10, 51, 10):
    generate_rolling(session_path, output_folder, i)
generate_lm(
    session_path,
    output_folder,
    "time_given_mistakes",
    "Total Mistakes",
    "Total Time Taken (ms)",
)
generate_lm(
    session_path,
    output_folder,
    "time_given_diff",
    "Layout Difficulty",
    "Total Time Taken (ms)",
)
generate_plot(session_path, output_folder)
