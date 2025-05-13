import pandas as pd
from google.cloud import firestore

# BQ6: What event categories generate the highest user engagement?

def answer_bq6(firestore_data):
    df_events = pd.DataFrame(firestore_data["events"])
    # Obtain the count of registered users and attendees for every event
    df_events["users_registered"] = pd.to_numeric(df_events["users_registered"], errors="coerce").fillna(0)
    df_events["attendees_count"] = df_events["attendees"].apply(lambda x: len(x) if isinstance(x, list) else 0)
    
    # Create a dataframe for categories and rename the id column
    df_categories = pd.DataFrame(firestore_data["categories"])
    df_categories.rename(columns={"id": "category_id"}, inplace=True)
    df_categories.rename(columns={"name": "category_name"}, inplace=True)

    # Obtain the category id from the reference in the event
    df_events["category_id"] = df_events["category"].apply(
        lambda x: x.id if isinstance(x, firestore.DocumentReference) else x
    )
    
    # Merge dataframes on category id to get name of the category
    df_merged = df_events.merge(df_categories, on="category_id", how="left")
    
    # Group by category name and calculate the total attendees and registered users
    grouped = df_merged.groupby("category_name").agg(
        total_attendees=pd.NamedAgg(column="attendees_count", aggfunc="sum"),
        total_registered=pd.NamedAgg(column="users_registered", aggfunc="sum")
    ).reset_index()
    
    # Calculate the engagement as (total attendees / total registered) if total registered is greater than 0
    # Otherwise, set the engagement to 0
    grouped["engagement"] = grouped.apply(
        lambda row: (row["total_attendees"] / row["total_registered"]) if row["total_registered"] > 0 else 0,
        axis=1
    )
    
    # Order by engagement in descending order
    grouped = grouped.sort_values(by="engagement", ascending=False)
    
    return grouped
    
