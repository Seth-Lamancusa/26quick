from generate_plots import generate_plots
from generate_text_summary import generate_text_summary
from localStorage_to_raw import localStorage_to_raw
from raw_to_session import raw_to_session
from generate_lm import generate_lm
from generate_rolling import generate_rolling


session_ID = "19"

localStorage_to_raw(session_ID)
raw_to_session(session_ID)
generate_text_summary(session_ID)
for i in range(10, 51, 10):
    generate_rolling(session_ID, i)
generate_lm(
    predictor="Total Mistakes",
    response="Total Time Taken (ms)",
    session_ID=session_ID,
    output_folder_name="time_given_mistakes",
)
generate_lm(
    predictor="Layout Difficulty",
    response="Total Time Taken (ms)",
    session_ID=session_ID,
    output_folder_name="time_given_diff",
)
generate_plots(session_ID=session_ID)
