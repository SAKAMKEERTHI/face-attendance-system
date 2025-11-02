import cv2
import face_recognition
import pickle
import csv
from datetime import datetime

# Load encodings as tuple
with open("encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

# ✅ Use DirectShow backend to fix camera issue
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
logged_names = set()

while True:
    ret, frame = video.read()
    if not ret:
        print("⚠️ Failed to grab frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        name = "Unknown"

        if face_distances.size > 0:
            best_match_index = face_distances.argmin()
            if face_distances[best_match_index] < 0.8:  # relaxed threshold
                name = known_names[best_match_index]
            else:
                continue  # Skip unknowns silently
        else:
            continue  # Skip if no distances

        if name not in logged_names:
            logged_names.add(name)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("attendance.csv", "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([name, now])
            print(f"✅ Logged: {name} at {now}")

        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
