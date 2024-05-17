import face_recognition
import cv2
import sqlite3
from datetime import datetime

# Connectez-vous à la base de données SQLite
conn = sqlite3.connect('votre_base_de_donnees.db')
cursor = conn.cursor()

# Créez la table Employees si elle n'existe pas déjà
cursor.execute('''CREATE TABLE IF NOT EXISTS Employees
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                heure TEXT NOT NULL)''')

# Charger une image avec un visage connu
known_image = face_recognition.load_image_file("chemin_vers_image_connu.jpg")
known_encoding = face_recognition.face_encodings(known_image)[0]

# Capturez la vidéo de la webcam
cap = cv2.VideoCapture(0)

while True:
    # Lire le frame de la webcam
    ret, frame = cap.read()

    # Convertir le frame en niveaux de gris pour la détection de visage
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages dans le frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Comparer les visages détectés avec le visage connu
    for face_encoding in face_encodings:
        # Comparez le visage avec le visage connu
        match = face_recognition.compare_faces([known_encoding], face_encoding)

        if match[0]:
            # Visage reconnu, enregistrez l'heure actuelle dans la base de données
            heure_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO Employees (name, heure) VALUES (?, ?)", ("Nom de l'employé", heure_actuelle))
            conn.commit()
            print("Visage reconnu. Heure enregistrée dans la base de données.")

    # Afficher le frame avec les vis
