import pandas as pd
import os

def save_df_csv (df,filename):
    if df is None or df.empty:
        print ("no data to save in the csv")
    base_dir = os.path.join(os.path.dirname(__file__), "csv_output")
    filepath = os.path.join(base_dir, filename)
    os.makedirs(base_dir, exist_ok=True)
    if not filename.endswith(".csv"):
        filename += ".csv"
        filepath = os.path.join(base_dir, filename)

    df.to_csv(filepath, index=False, encoding="utf-8-sig")

    print(f" Datos guardados en '{filepath}'.")