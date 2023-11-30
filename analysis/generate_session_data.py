from generate_plot import generate_plot
from generate_text_summary import generate_text_summary
from localStorage_to_raw import localStorage_to_raw
from raw_to_session import raw_to_session
from generate_lms import generate_lms


# Define the relative path to the input json file
input_file_path = "analysis/data/session_1/localStorage_2023-11-23_14-34-01.json"
output_folder = "analysis/data/session_1"

raw_path = localStorage_to_raw(input_file_path, output_folder)
session_path = raw_to_session(raw_path, output_folder)
summary_path = generate_text_summary(session_path, output_folder)
generate_lms(session_path, output_folder)
generate_plot(session_path, output_folder)
