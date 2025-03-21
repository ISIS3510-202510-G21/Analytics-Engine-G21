import pandas as pd
import numpy as np

def answer_bq1(firestore_data):
    df_events = pd.DataFrame(firestore_data["events"])

    #validaciones básicas
    if "attendees" not in df_events.columns or "cost" not in df_events.columns:
        print("Missing necessary columns in events collection.")
        return pd.DataFrame()

    #cost sea numérico
    df_events["cost"] = pd.to_numeric(df_events["cost"], errors="coerce")
    df_events = df_events.dropna(subset=["cost"])

    #contar asistentes
    df_events["attendees_count"] = df_events["attendees"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )

    #clasificar por rangos de precio
    bins = [0, 1, 10000, 30000, 70000, 120000, 200000, float("inf")]
    labels = [
        "Free",
        "Low (1 - 10k)",
        "Economy (10k - 30k)",
        "Medium (30k - 70k)",
        "High (70k - 120k)",
        "Premium (120k - 200k)",
        "Ultra Premium (200k+)"
    ]
    df_events["price_range"] = pd.cut(df_events["cost"], bins=bins, labels=labels, include_lowest=True)

    #agrupar y calcular asistencia promedio
    df_price_attendance = df_events.groupby("price_range")["attendees_count"].mean().reset_index()
    df_price_attendance.rename(columns={"attendees_count": "avg_attendees"}, inplace=True)
    df_price_attendance = df_price_attendance.sort_values(by="avg_attendees", ascending=False)
    
    #reemplazar vacíos con 0
    df_price_attendance["avg_attendees"] = df_price_attendance["avg_attendees"].fillna(0)


    #redondear
    df_price_attendance["avg_attendees"] = np.floor(df_price_attendance["avg_attendees"]).astype(int)

    return df_price_attendance

