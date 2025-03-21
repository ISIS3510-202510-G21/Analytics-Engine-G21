import pandas as pd


def answer_events_by_category(firestore_data):
    if "events" not in firestore_data or not isinstance(firestore_data["events"], list):
        return pd.DataFrame()
    df_events = pd.DataFrame(firestore_data["events"])
    if "category" not in df_events.columns:
        return pd.DataFrame()
    df_count = df_events.groupby("category").size().reset_index(name="total_events")
    return df_count

