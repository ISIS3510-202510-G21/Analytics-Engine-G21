from src.firebase_config import db

def obtain_data_from_firestore(collection):
    try:
        docs = db.collection(collection).stream()
        datos = [doc.to_dict() for doc in docs]
        return datos
    except Exception as e:
        return {"error": str(e)}
