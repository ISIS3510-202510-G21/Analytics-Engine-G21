import pandas as pd

# BQ2: How many times does a user interact with the map screen?

def answer_maps_clicks_usage(firestore_data):
    # Verify that 'map_clicks' exists in the data and is a list
    if "map_clicks" not in firestore_data or not isinstance(firestore_data["map_clicks"], list):
        return pd.DataFrame({"Error": ["The key 'map_clicks' does not exist or is not a list"]})

    # Create DataFrame from clicks data
    df_clicks = pd.DataFrame(firestore_data["map_clicks"])

    # Verify that required columns exist
    required_columns = {"userId", "clickType"}
    if not required_columns.issubset(df_clicks.columns):
        return pd.DataFrame({"Error": ["Required columns are missing in the data"]})

    # Count occurrences by user and click type
    df_counts = (
        df_clicks.groupby(["userId", "clickType"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Rename columns for clarity (optional)
    df_counts.columns.name = None
    
    # Based on the sample data, rename specific click types if needed
    # You might need to adjust these based on your actual clickType values
    click_type_mapping = {
        "select_event": "select_event_clicks",
        "refresh_online": "refresh_online_clicks",
        "refresh_offline": "refresh_offline_clicks"
    }
    
    # Apply renaming only for columns that exist
    for old_name, new_name in click_type_mapping.items():
        if old_name in df_counts.columns:
            df_counts = df_counts.rename(columns={old_name: new_name})

    # Add a total interactions column
    numeric_columns = df_counts.columns.drop('userId')
    df_counts['total_map_interactions'] = df_counts[numeric_columns].sum(axis=1)

    return df_counts