import data_loader
import exporter_csv
import pandas
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import data_loader
from BQ_Sprint2 import bq1, bq2, bq3, bq4, bq5, bq6 
from BQ_Sprint3 import bq6_S3, bq4_S3,bq5_S3, bq3_S3, bq7_S3, bq2_S3
from BQ_Sprint4 import bq3_S4, bq2_S4
from firebase_config import db
from google.cloud import firestore 


def pipeline():

    # Cargar archivos
    data=data_loader.load_all_collections()
    

    # ---- Sprint 2 ----

    # Responder pregunta 1
    df_bq1 = bq1.answer_bq1(data)
    exporter_csv.save_df_csv(df_bq1, "bq1-S2Answer")

    # Responder pregunta 3
    df_bq3=bq3.answer_events_by_category(data)
    exporter_csv.save_df_csv(df_bq3, "bq3-S2Answer")

    # Responder pregunta 4
    df_bq4=bq4.answer_attendance_rate(data)
    exporter_csv.save_df_csv(df_bq4,"bq4-S2Answer")

    # Responder pregunta 5
    df_bq5=bq5.answer_bq5(data)
    exporter_csv.save_df_csv(df_bq5,"bq5-S2Answer")

    # Responder pregunta 6
    df_bq6=bq6.answer_bq6(data)
    exporter_csv.save_df_csv(df_bq6,"bq6-S2Answer")

    # ---- Sprint 3 ----
    # Responder pregunta 2
    df_bq2_S3=bq2_S3.answer_maps_clicks_usage(data)
    exporter_csv.save_df_csv(df_bq2_S3, "bq2-S3Answer")

    # Responder pregunta 3
    df_bq3_S3=bq3_S3.answer_search_event_usage(data)
    exporter_csv.save_df_csv(df_bq3_S3, "bq3-S3Answer")

    # REsponder pregunta 4
    df_bq4_S3=bq4_S3.process_home_interactions(data)
    exporter_csv.save_df_csv(df_bq4_S3,"bq4_S3Answer")
    
    # Responder pregunta 5
    df_bq5_S3_summary, df_bq5_S3_clicks_per_day =bq5_S3.process_chatbot_clicks(data)
    exporter_csv.save_df_csv(df_bq5_S3_summary, "bq5-S3Answer")
    exporter_csv.save_df_csv(df_bq5_S3_clicks_per_day, "bq5-S3Answer_clicks_per_day")

    # Responder pregunta 6
    df_bq6_S3=bq6_S3.topSkills(data)
    exporter_csv.save_df_csv(df_bq6_S3, "bq6-S3Answer")
    
    # Responder pregunta 7
    df_bq7_S3, df_bq7_S3_clicks_per_day = bq7_S3.process_event_detail_clicks(data)
    exporter_csv.save_df_csv(df_bq7_S3, "bq7-S3Answer")
    exporter_csv.save_df_csv(df_bq7_S3_clicks_per_day, "bq7-S3Answer_clicks_per_day")
    
    # ---- Sprint 4 ----
    # Responder pregunta 3
    df_bq3_S4_summary, df_bq3_S4_registration_clicks, df_bq3_S4_eventDetail_clicks = bq3_S4.process_attendees_clicks(data)
    exporter_csv.save_df_csv(df_bq3_S4_summary, "bq3-S4Summary")
    exporter_csv.save_df_csv(df_bq3_S4_registration_clicks, "bq3_S4_registration_clicks")
    exporter_csv.save_df_csv(df_bq3_S4_eventDetail_clicks, "bq3_S4_eventDetail_clicks")

    # Sprint 4

    # Responder pregunta 2
    df_bq2 = bq2_S4.answer_event_stats_usage(data)
    exporter_csv.save_df_csv(df_bq2, "bq2-S4Answer")
    
def pipeline_recommendation_bq2():
    data = data_loader.load_all_collections()
    for profile in data["profiles"]:
        user_ref = profile["user_ref"]
        user_id = user_ref.id if isinstance(user_ref, firestore.DocumentReference) else user_ref
        try:
            recommended_events = bq2.recommend_events_for_user(user_id, data)

            if recommended_events:
                doc_ref = db.collection("users").document(user_id)
                if doc_ref.get().exists:
                    doc_ref.update({"recommended_events": recommended_events})
                    print(f"Recommendations saved for user {user_id}.")
                else:
                    print(f"No document found for user {user_id}. Skipping update.")
            else:
                print(f"No recommendations found for user {user_id}.")
        except Exception as e:
            print(f"Error while processing user {user_id}: {e}")

if __name__ == "__main__":
    pipeline()
    pipeline_recommendation_bq2()