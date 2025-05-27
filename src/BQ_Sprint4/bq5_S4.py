import pandas as pd

def clicks_by_category(data):
    # Validar existencia de colecciones necesarias
    if "eventdetail_clicks" not in data or "categories" not in data:
        return pd.DataFrame({"Error": ["Faltan datos de 'eventdetail_clicks' o 'categories'."]})

    # Crear DataFrames
    clicks_df = pd.DataFrame(data["eventdetail_clicks"])
    categories_df = pd.DataFrame(data["categories"])

    # Verificar que existan las columnas necesarias
    if "category_name" not in clicks_df.columns or "name" not in categories_df.columns:
        return pd.DataFrame({"Error": ["Faltan columnas necesarias ('category_name' o 'name')."]})

    # Contar clics por nombre de categoría
    clicks_count = clicks_df["category_name"].value_counts().reset_index()
    clicks_count.columns = ["category_name", "event_detail_clicks"]

    # Crear DataFrame base con todas las categorías (por nombre)
    all_categories = categories_df[["name"]].drop_duplicates().rename(columns={"name": "category_name"})

    # Unir para incluir categorías con 0 clics
    result_df = all_categories.merge(clicks_count, on="category_name", how="left")
    result_df["event_detail_clicks"] = result_df["event_detail_clicks"].fillna(0).astype(int)
    
    # Ordenar: primero las que sí tienen clics (> 0), luego las de 0, en orden ascendente
    result_df = result_df.sort_values(by=["event_detail_clicks", "category_name"], ascending=[False, True]).reset_index(drop=True)

    return result_df


