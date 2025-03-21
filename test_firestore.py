import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from firebase_config import db

def test_conexion():
    try:
        # Intentar obtener documentos de una colección de prueba
        docs = db.collection("users").limit(2).stream()
        for doc in docs:
            print(f"Documento encontrado: {doc.id} => {doc.to_dict()}")
        print("Conexión exitosa a Firestore.")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    test_conexion()
