import os
import face_recognition
import pickle

# Path to your custom dataset
dataset_path = "D:\\Face_Attendance_Project\\dataset"

known_encodings = []
known_names = []

for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_folder):
        continue

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
            else:
                print(f"[SKIPPED] No face detected in: {image_path}")
        except Exception as e:
            print(f"[ERROR] Failed to process {image_path}: {e}")

# Save encodings
with open("encodings.pkl", "wb") as f:
    pickle.dump((known_encodings, known_names), f)

print("✅ Custom dataset preprocessing complete. Encodings saved to encodings.pkl.")
