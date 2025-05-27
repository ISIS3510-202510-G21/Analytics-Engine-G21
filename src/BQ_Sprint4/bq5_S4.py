from collections import Counter
import pandas as pd

def topSkills(data, top_n=20):
    """
    Devuelve las TOP habilidades más comunes entre los usuarios.

    Entradas:
    - data: diccionario con las colecciones Firestore pre-cargadas (users, skills).
    - top_n: cuántas habilidades mostrar.

    Salida:
    - Lista de diccionarios con claves: skill_id, name, count.
    """
    try:
        # Convertir colecciones a DataFrame
        df_users = pd.DataFrame(data.get("users", []))
        df_skills = pd.DataFrame(data.get("skills", []))

        # Contar habilidades
        skill_counter = Counter()
        for skills in df_users.get("skills", []):
            if isinstance(skills, list):
                skill_counter.update(skills)

        # Resolver nombres de habilidades por ID
        id_to_name = {
            row["id"]: row.get("name", "Unknown")
            for _, row in df_skills.iterrows()
        }

        # Crear resultado ordenado
        top_skills = [
            {
                "skill_id": skill_id,
                "name": id_to_name.get(skill_id, "Unknown"),
                "count": count,
            }
            for skill_id, count in skill_counter.most_common(top_n)
        ]

        return pd.DataFrame(top_skills)

    except Exception as e:
        print(f"Error in topSkills: {e}")
        return pd.DataFrame([])
