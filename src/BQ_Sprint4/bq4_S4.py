import pandas as pd


def process_followers_following_logs(data):
    df = pd.DataFrame(data['followers_following_logs'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date

    views_per_day = df.groupby("date").size().reset_index(name="views")

    views_per_day_by_type = df.groupby(["date", "type"]).size().reset_index(name="views")

    summary = {
        "total_views": len(df),
        "total_followers_views": len(df[df["type"] == "followers"]),
        "total_following_views": len(df[df["type"] == "following"]),
        "active_days": views_per_day.shape[0],
        "average_views_per_active_day": round(views_per_day["views"].mean(), 2),
        "days_without_views": ((df["date"].max() - df["date"].min()).days + 1) - views_per_day.shape[0],
    }

    summary_df = pd.DataFrame([summary])

    return summary_df, views_per_day, views_per_day_by_type

