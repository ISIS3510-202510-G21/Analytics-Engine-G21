import pandas as pd

# BQ4: What is the percentage of users that attend events they register for?

def answer_attendance_rate(firestore_data):
    # Verificar que 'events' esté en los datos
    if "events" not in firestore_data or not isinstance(firestore_data["events"], list):
        return pd.DataFrame({"Error": ["La clave 'events' no existe o no es una lista"]})

    # Crear DataFrame de eventos
    df_events = pd.DataFrame(firestore_data["events"])

    # Verificar que existen las columnas necesarias
    required_columns = {"attendees", "users_registered"}
    if not required_columns.issubset(df_events.columns):
        return pd.DataFrame({"Error": ["Faltan columnas necesarias en los datos"]})

    # Manejo de valores nulos y transformación de tipos
    df_events["users_registered"] = pd.to_numeric(df_events["users_registered"], errors="coerce").fillna(0).astype(int)
    
    # Contar asistentes solo si 'attendees' es una lista
    df_events["attended_count"] = df_events["attendees"].apply(lambda x: len(x) if isinstance(x, list) else 0)

    # Filtrar eventos con registros válidos (>0)
    df_valid_events = df_events[df_events["users_registered"] > 0].copy()

    # Calcular el porcentaje de asistencia
    df_valid_events["attendance_rate"] = (df_valid_events["attended_count"] / df_valid_events["users_registered"]) * 100

    # Dejar solo las columnas necesarias
    df_valid_events = df_valid_events[["name", "users_registered", "attended_count", "attendance_rate"]]

    # Retornar DataFrame con los resultados detallados
    return df_valid_events
