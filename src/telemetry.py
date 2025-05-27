from firebase_config import db

# Datos de telemetría extraídos de la aplicación
telemetry_data = [
    {"trace": "Location", "samples": 30, "duration": 10330},
    {"trace": "Follow Screens", "samples": 4, "duration": 4320},
    {"trace": "Map List Loading", "samples": 5, "duration": 3680},
    {"trace": "Chatbot Status", "samples": 2, "duration": 1360},
    {"trace": "_app_start", "samples": 3, "duration": 1180},
    {"trace": "Profile Screen", "samples": 3, "duration": 1120},
    {"trace": "Send Message in Chatbot", "samples": 2, "duration": 747},
    {"trace": "Toggle Follow/Unfollow", "samples": 2, "duration": 637},
    {"trace": "Home Events", "samples": 12, "duration": 7},
]

# Subir a Firestore
collection_ref = db.collection("telemetry")

for item in telemetry_data:
    doc_ref = collection_ref.document()
    doc_ref.set(item)

print("✅ Telemetry data has been loaded successfully to Firestore.")