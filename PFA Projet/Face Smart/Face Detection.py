import face_recognition
import cv2
import sqlite3
from datetime import datetime

conn = sqlite3.connect('votre_base_de_donnees.db')
cursor = conn.cursor()
cursor.execute("SELECT Code, Image FROM Employees")
known_faces = cursor.fetchall()
known_encodings = []
known_codes = []
for code, image_data in known_faces:
    face_image = face_recognition.load_image_file(image_data)
    encoding = face_recognition.face_encodings(face_image)[0]
    known_encodings.append(encoding)
    known_codes.append(code)
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        if any(matches):
            match_index = matches.index(True)
            matched_code = known_codes[match_index]
            heure_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO WorkSchedule(EmployeeCode, StartTime) VALUES (?, ?)", (matched_code, heure_actuelle))
            conn.commit()
            print(f"Visage avec le code {matched_code} reconnu. Heure enregistrée dans la base de données.")
cap.release()
conn.close()
