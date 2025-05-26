import pandas as pd

def process_attendees_clicks(data):
    # Procesar DataFrame
    df = pd.DataFrame(data['attendees_clicks'])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    # Clics por día
    clicks_per_day = df.groupby("date").size().reset_index(name="clicks")
    
    # Clics por dia por pantalla
    clicks_per_day_screen = df.groupby(["date", "screen"]).size().reset_index(name="clicks")
    
    # Clics por dia en la pantalla 
    registration_clicks = clicks_per_day_screen[clicks_per_day_screen['screen'] == 'registration']
    eventDetail_clicks = clicks_per_day_screen[clicks_per_day_screen['screen'] == 'eventDetail']
    

    # Estadísticas resumidas
    summary = {
        "total_clicks": len(df),
        "active_days": clicks_per_day.shape[0],
        "average_clicks_per_active_day": round(clicks_per_day["clicks"].mean(), 2),
        "days_without_clicks": ((df["date"].max() - df["date"].min()).days + 1) - clicks_per_day.shape[0]
    }

    # Convertir a DataFrame
    summary_df = pd.DataFrame([summary])
    
    # Agregar clics por pantalla al resumen
    for screen in clicks_per_day_screen['screen'].unique():
        screen_clicks = clicks_per_day_screen[clicks_per_day_screen['screen'] == screen]['clicks'].sum()
        average_clicks = clicks_per_day_screen[clicks_per_day_screen['screen'] == screen]['clicks'].mean()
        summary_df[f"average_clicks_{screen}"] = round(average_clicks, 2)
        summary_df[f"clicks_{screen}"] = screen_clicks

    return summary_df, registration_clicks, eventDetail_clicks
