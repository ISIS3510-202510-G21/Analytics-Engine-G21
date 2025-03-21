from firebase_config import db  


firestore_data = {}

def load_all_collections():
    """
    Obtiene todas las colecciones de Firestore y las almacena en el diccionario `firestore_data`.
    """
    try:
        collections = db.collections()  

        for collection in collections:
            collection_name = collection.id  
            docs = collection.stream()  
            firestore_data[collection_name] = [
                {**doc.to_dict(), "id": doc.id} for doc in docs  
            ]

        print ("All collections have been charged in firestore_data")
        return firestore_data

    except Exception as e:
        print (f"error at getting firestore data: {e}")

