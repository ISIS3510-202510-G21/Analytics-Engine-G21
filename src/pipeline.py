import data_loader
import exporter_csv
import pandas
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import data_loader
from src.BQ import bq1, bq2, bq4_Number_2 as bq3, bq4, bq5, bq6
from firebase_config import db
from google.cloud import firestore 


def pipeline():

    # Cargar archivos
    data=data_loader.load_all_collections()
    
    # Responder pregunta 1
    df_bq1 = bq1.answer_bq1(data)
    exporter_csv.save_df_csv(df_bq1, "bq1Answer")

    # Responder pregunta 5
    df_bq5=bq5.answer_bq5(data)
    exporter_csv.save_df_csv(df_bq5,"bq5Answer")

    # Responder pregunta 4
    df_bq4=bq4.answer_attendance_rate(data)
    exporter_csv.save_df_csv(df_bq4,"bq4Answer")

    # Responder pregunta 6
    df_bq6=bq6.answer_bq6(data)
    exporter_csv.save_df_csv(df_bq6,"bq6Answer")
    
    # Responder pregunta 4 Numero 2
    df_bq4_2=bq3.answer_events_by_category(data)
    exporter_csv.save_df_csv(df_bq4_2, "bq3Answer")
    
    
def pipeline_recommendation_bq2():
    # Cargar datos de Firestore
    data = data_loader.load_all_collections()
    # Recorrer todos los perfiles de usuarios en Firestore
    for profile in data["profiles"]:
        user_ref = profile["user_ref"]
        user_id = user_ref.id if isinstance(user_ref, firestore.DocumentReference) else user_ref
        # Generar recomendaciones para el usuario
        recommended_events = bq2.recommend_events_for_user(user_id, data)
        if recommended_events:
            db.collection("users").document(user_id).update({"recommended_events": recommended_events})
            print(f"Recommendations saved for user {user_id}.")
        else:
            print(f"No recommendations found for user {user_id}.")



if __name__ == "__main__":
    pipeline()
    pipeline_recommendation_bq2()






