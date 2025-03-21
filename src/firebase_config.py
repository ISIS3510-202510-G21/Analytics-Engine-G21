import firebase_admin
from firebase_admin import credentials, firestore

# Cargar la clave de servicio de Firebase
cred = credentials.Certificate("pon aqui el json")
firebase_admin.initialize_app(cred)

# Conectar con Firestore
db = firestore.client()
