import pandas as pd

def answer_event_stats_usage(firestore_data):
    """
    Processes Firestore event_stats data into a DataFrame summarizing:
    - Total attendees per event
    - Most common headline
    - Most common interest
    """

    # Validate input data
    if "event_stats" not in firestore_data or not isinstance(firestore_data["event_stats"], list):
        return pd.DataFrame({"Error": ["'event_stats' key is missing or not a list"]})

    # Load data into DataFrame
    df_stats = pd.DataFrame(firestore_data["event_stats"])

    # Required columns check
    required_columns = {"event_name", "number_of_attendees", "most_common_headline", "most_common_interest"}
    if not required_columns.issubset(df_stats.columns):
        return pd.DataFrame({"Error": ["Missing required columns in the input data"]})

    # Optionally summarize by event if multiple records exist per event
    df_summary = df_stats.groupby("event_name").agg({
        "number_of_attendees": "max",  # or "mean", "sum" depending on your goal
        "most_common_headline": lambda x: x.mode().iloc[0] if not x.mode().empty else "",
        "most_common_interest": lambda x: x.mode().iloc[0] if not x.mode().empty else ""
    }).reset_index()

    return df_summary