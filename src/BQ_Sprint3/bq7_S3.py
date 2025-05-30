import pandas as pd

# How often is the Event Detail screen accessed?

def process_event_detail_clicks(data):
    df = pd.DataFrame(data['eventdetail_clicks'])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date

    clicks_per_day = df.groupby("date").size().reset_index(name="clicks")

    summary = {
        "total_clicks": len(df),
        "active_days": clicks_per_day.shape[0],
        "average_clicks_per_active_day": round(clicks_per_day["clicks"].mean(), 2),
        "days_without_clicks": ((df["date"].max() - df["date"].min()).days + 1) - clicks_per_day.shape[0]
    }

    summary_df = pd.DataFrame([summary])

    return summary_df, clicks_per_day
