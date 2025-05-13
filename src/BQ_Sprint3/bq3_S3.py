import pandas as pd

def answer_search_event_usage(firestore_data):
    # Verificar que 'search_clicks' esté en los datos y sea una lista
    if "search_clicks" not in firestore_data or not isinstance(firestore_data["search_clicks"], list):
        return pd.DataFrame({"Error": ["La clave 'search_clicks' no existe o no es una lista"]})

    # Crear DataFrame de clics
    df_clicks = pd.DataFrame(firestore_data["search_clicks"])

    # Verificar que existen las columnas necesarias
    required_columns = {"userId", "clickType"}
    if not required_columns.issubset(df_clicks.columns):
        return pd.DataFrame({"Error": ["Faltan columnas necesarias en los datos"]})

    # Contar ocurrencias por usuario y tipo de clic
    df_counts = (
        df_clicks.groupby(["userId", "clickType"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Renombrar columnas para claridad (opcional)
    df_counts.columns.name = None
    df_counts = df_counts.rename(columns={
        "search_click": "search_clicks",
        "clear_click": "clear_clicks",
        "filter_click": "filter_clicks",
        "date_click": "date_clicks"
    })

    return df_counts
