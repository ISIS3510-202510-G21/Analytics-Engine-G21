import firebase_admin
from firebase_admin import credentials, firestore

# Cargar la clave de servicio de Firebase
cred = credentials.Certificate("aqui poner la ruta de la clave de servicio de Firebase")
firebase_admin.initialize_app(cred)

# Conectar con Firestore
db = firestore.client()
