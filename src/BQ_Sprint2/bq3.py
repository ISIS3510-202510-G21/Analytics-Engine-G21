import pandas as pd
from google.cloud import firestore

def answer_events_by_category(firestore_data):
    if "events" not in firestore_data or not isinstance(firestore_data["events"], list):
        return pd.DataFrame()
    
    # Convert to DataFrame
    df_events = pd.DataFrame(firestore_data["events"])
    
    if "category" not in df_events.columns:
        return pd.DataFrame()

    # Function to fetch category name from Firestore
    def get_category_name(category_ref):
        if isinstance(category_ref, firestore.DocumentReference):
            doc = category_ref.get()
            if doc.exists:
                return doc.to_dict().get("name", "Unknown")  # Get the name field
        return str(category_ref)  # If it's already a string, return as is

    # Convert category references to names
    df_events["category"] = df_events["category"].apply(get_category_name)
    
    # Group and count events by category
    df_count = df_events.groupby("category").size().reset_index(name="total_events")
    
    return df_count
