from generate_plots import generate_plots
from generate_text_summary import generate_text_summary
from localStorage_to_raw import localStorage_to_raw
from raw_to_session import raw_to_session
from generate_lm_folder import generate_lm_folder
from generate_rolling import generate_rolling

session_ID = "49"
sessions = [str(i) for i in range(1, int(session_ID) + 1)]

# Preprocessing
localStorage_to_raw(session_ID)
raw_to_session(session_ID)

# Generate session insights
generate_text_summary(session_ID=session_ID)
for i in range(10, 51, 10):
    generate_rolling(session_ID, i)
generate_lm_folder(
    predictor="Total Mistakes",
    response="Total Time Taken (ms)",
    session_ID=session_ID,
    output_folder_name="time_given_mistakes",
)
generate_lm_folder(
    predictor="Layout Difficulty",
    response="Total Time Taken (ms)",
    session_ID=session_ID,
    output_folder_name="time_given_diff",
)
generate_plots(session_ID=session_ID)

# Update aggregate insights
generate_text_summary(agg=True, sessions=sessions)
generate_lm_folder(
    predictor="Total Mistakes",
    response="Total Time Taken (ms)",
    output_folder_name="time_given_mistakes",
    agg=True,
    sessions=sessions,
)
generate_lm_folder(
    predictor="Layout Difficulty",
    response="Total Time Taken (ms)",
    output_folder_name="time_given_diff",
    agg=True,
    sessions=sessions,
)
generate_plots(agg=True, sessions=sessions)
