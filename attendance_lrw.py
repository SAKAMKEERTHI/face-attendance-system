import cv2
import face_recognition
import pickle
from datetime import datetime

# Load encodings from your custom dataset
with open("encodings.pkl", "rb") as f:
    known_encodings, known_names = pickle.load(f)

# Dictionary to store attendance
attendance_log = {}

# Start webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces and encode them
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        if True in matches:
            best_match_index = face_distances.argmin()
            name = known_names[best_match_index]

            # Mark attendance if not already logged
            if name not in attendance_log:
                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                attendance_log[name] = time_now
                print(f"[INFO] Face detected: {name}")
                print(f"[INFO] Attendance marked at: {time_now}")

            # Draw bounding box and label
            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        else:
            continue  # Skip unknowns silently

    cv2.imshow("Face Attendance - Custom", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save attendance log
with open("attendance.csv", "w") as f:
    f.write("Name,Time\n")
    for name, time in attendance_log.items():
        f.write(f"{name},{time}\n")

video_capture.release()
cv2.destroyAllWindows()
print("✅ Attendance saved to attendance.csv")
