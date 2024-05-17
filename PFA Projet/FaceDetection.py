
import sqlite3
import cv2
import face_recognition
import numpy as np
import json
from face_recognition import face_distance
from tkinter import ttk
from datetime import datetime
def detecter_visages(image, cascade):
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(frame_rgb)
    face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    if len(face_encodings) > 0:
        face_encoding = face_encodings[2]
        face_encoding_str = json.dumps(face_encoding.tolist())
        conn = sqlite3.connect('gestion_des_employes.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees")
        rows = cursor.fetchall()
        database_encodings = [np.array(json.loads(row[8])) for row in rows]
        database_names = [row[2] for row in rows]
        if len(database_encodings) > 0:
            face_distances = face_distance(database_encodings, np.array(json.loads(face_encoding_str)))
            matches = [distance <= 0.6 for distance in face_distances]
            if True in matches:
                match_index = matches.index(True)
                name = database_names[match_index]
            else:
                name = "Inconnu"
        else:
            name = "Inconnu"
    else:
        name = "Inconnu"
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    visages = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in visages:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(image, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return image
def reconnaissance_facial():
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    cascade = cv2.CascadeClassifier(cascade_path)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erreur: la webcam ne peut pas être ouverte.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur: Impossible de lire l'image de la webcam.")
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = detecter_visages(frame, cascade)
        cv2.imshow('Reconnaissance faciale', frame)
        key = cv2.waitKey(30)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()