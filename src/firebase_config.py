import firebase_admin
from firebase_admin import credentials, firestore

# Cargar la clave de servicio de Firebase
cred = credentials.Certificate("growhub-50aa2-firebase-adminsdk-fbsvc-56658259f1.json")
firebase_admin.initialize_app(cred)

# Conectar con Firestore
db = firestore.client()
