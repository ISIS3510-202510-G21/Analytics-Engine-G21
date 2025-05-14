import pandas as pd

def answer_maps_clicks_usage(firestore_data):
    # Verify that 'map_clicks' exists in the data and is a list
    if "map_clicks" not in firestore_data or not isinstance(firestore_data["map_clicks"], list):
        return pd.DataFrame({"Error": ["The key 'map_clicks' does not exist or is not a list"]})

    # Create DataFrame from clicks data
    df_clicks = pd.DataFrame(firestore_data["map_clicks"])

    # Verify that required columns exist
    if "clickType" not in df_clicks.columns:
        return pd.DataFrame({"Error": ["Required column 'clickType' is missing in the data"]})

    # Count occurrences by click type
    click_counts = df_clicks["clickType"].value_counts().reset_index()
    click_counts.columns = ["clickType", "count"]
    
    # Calculate total interactions
    total_interactions = click_counts["count"].sum()
    
    # Add a row for total
    total_row = pd.DataFrame({"clickType": ["TOTAL"], "count": [total_interactions]})
    click_counts = pd.concat([click_counts, total_row], ignore_index=True)
    
    return click_counts