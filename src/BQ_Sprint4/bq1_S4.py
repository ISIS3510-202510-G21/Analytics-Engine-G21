import pandas as pd

def answer_bq_type1_telemetry(firestore_data):
    """
    Calculates the average loading time per screen based on Firestore telemetry data.
    Returns a DataFrame with columns: trace, average_duration_per_sample (ms)
    """
    # Validate input data
    if "telemetry" not in firestore_data or not isinstance(firestore_data["telemetry"], list):
        return pd.DataFrame({"Error": ["'telemetry' key is missing or not a list"]})

    # Load data into DataFrame
    df_telemetry = pd.DataFrame(firestore_data["telemetry"])

    # Required columns check
    required_columns = {"trace", "duration"}
    if not required_columns.issubset(df_telemetry.columns):
        return pd.DataFrame({"Error": ["Missing required columns in the input data"]})

    # Calculate average duration per sample for each trace
    df_summary = df_telemetry.groupby("trace")["duration"].mean().reset_index()
    df_summary.rename(columns={"duration": "average_duration_per_sample"}, inplace=True)

    return df_summary

