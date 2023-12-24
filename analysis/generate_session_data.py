from generate_plot import generate_plot
from generate_text_summary import generate_text_summary
from localStorage_to_raw import localStorage_to_raw
from raw_to_session import raw_to_session
from generate_lm import generate_lm
from generate_rolling import generate_rolling
from generate_agg_data import generate_agg_data


session_ID = "n"

localStorage_to_raw(session_ID)
raw_to_session(session_ID)
generate_text_summary(session_ID)
for i in range(10, 51, 10):
    generate_rolling(session_ID, i)
generate_lm(
    session_ID,
    "time_given_mistakes",
    "Total Mistakes",
    "Total Time Taken (ms)",
)
generate_lm(
    session_ID,
    "time_given_diff",
    "Layout Difficulty",
    "Total Time Taken (ms)",
)
generate_plot(session_ID)
