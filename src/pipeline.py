import data_loader
import exporter_csv
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import data_loader
from src.BQ import bq5, bq4

def pipeline():

    # Cargar archivos
    data=data_loader.load_all_collections()

    # Responder pregunta 5
    df_bq5=bq5.answer_bq5(data)
    exporter_csv.save_df_csv(df_bq5,"bq5Answer")

    # Responder pregunta 4
    df_bq4=bq4.answer_attendance_rate(data)
    exporter_csv.save_df_csv(df_bq4,"bq4Answer")

if __name__ == "__main__":
    pipeline()