import pandas as pd
from google.cloud import firestore

#BQ5: What skills are most frequetly asscoiated with the highest-attened events?

def answer_bq5(firestore_data):
    df_events = pd.DataFrame(firestore_data["events"])
    df_events = df_events[["attendees", "category"]]  
    df_categories = pd.DataFrame(firestore_data["categories"])
    df_categories.rename(columns={"id": "category_id"}, inplace=True)
    df_events["category_id"] = df_events["category"].apply(lambda x: x.id if isinstance(x, firestore.DocumentReference) else x)
    df_events["attendees_count"] = df_events["attendees"].apply(
            lambda x: len(x) if isinstance(x, list) else 0  # Contar si es lista, sino poner 0
        )
    df_events=df_events[["attendees_count","category_id"]]
    df_events = df_events.merge(df_categories, on="category_id", how="left")
    df_events=df_events[["attendees_count","name"]]
    df_top_categories = df_events.groupby("name")["attendees_count"].sum().reset_index()
    df_top_categories = df_top_categories.sort_values(by="attendees_count", ascending=False).head(5)
    return df_top_categories

        
