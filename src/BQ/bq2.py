import pandas as pd
from google.cloud import firestore

#BQ2: Which event category does a User like the most?

import pandas as pd
from google.cloud import firestore

def get_user_category_preferences(user_id, firestore_data):
    """
    Returns a ranking of categories based on the number of events attended by the user.
    """
    try:    
        df_profiles = pd.DataFrame(firestore_data["profiles"])
        df_events = pd.DataFrame(firestore_data["events"])
        user_profile = df_profiles[df_profiles["user_ref"].apply(lambda x: x.id if isinstance(x, firestore.DocumentReference) else x) == user_id]
        events_attended = user_profile.iloc[0]["events_asociated"]
        event_ids = [e.id if isinstance(e, firestore.DocumentReference) else e for e in events_attended]
        user_events = df_events[df_events["id"].isin(event_ids)].copy()
        user_events.loc[:, "category_id"] = user_events["category"].apply(lambda x: x.id if isinstance(x, firestore.DocumentReference) else x)
        category_counts = user_events["category_id"].value_counts()
        if category_counts.empty:
            print(f"No category data available for user {user_id}.")
            return None
        return category_counts.to_dict()

    except Exception as e:
        print(f"Error in get_user_category_preferences: {e}")
        return None


        
def recommend_events_for_user(user_id, firestore_data):
    """
    Recommends future events based on the ranking of categories most frequented by the user.
    """
    try:
        category_preferences = get_user_category_preferences(user_id, firestore_data)
        df_events = pd.DataFrame(firestore_data["events"]).copy()  
        df_events.loc[:, "start_date"] = pd.to_datetime(df_events["start_date"], utc=True)
        now_utc = pd.Timestamp.now(tz="UTC")
        upcoming_events = df_events[df_events["start_date"] > now_utc].copy()
        upcoming_events.loc[:, "category_id"] = upcoming_events["category"].apply(lambda x: x.id if isinstance(x, firestore.DocumentReference) else x)
        upcoming_events.loc[:, "priority"] = upcoming_events["category_id"].map(category_preferences).fillna(0)
        upcoming_events = upcoming_events.sort_values(by=["priority", "start_date"], ascending=[False, True])
        recommended_events_df = upcoming_events[["id"]].to_dict(orient="records")
        recommended_events = []
        for event in recommended_events_df:
            recommended_events.append(event["id"])

        return recommended_events

    except Exception as e:
        print(f" Error in recommend_events_for_user: {e}")
        return []
