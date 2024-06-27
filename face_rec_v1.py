import face_recognition
import numpy as np
import cv2
import pandas as pd
import argparse
from datetime import datetime
from face_encoding import known_face_encodings, known_face_names

# Command line argument for subject name
parser = argparse.ArgumentParser(description="Face Recognition Attendance System")
parser.add_argument('subject', type=str, help='Name of the subject')
args = parser.parse_args()
subject_name = args.subject

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Initialize attendance DataFrame
attendance_file = "attendance.csv"
columns = ["Student Name", "Date", "Subject", "Status"]
try:
    attendance_df = pd.read_csv(attendance_file)
except FileNotFoundError:
    attendance_df = pd.DataFrame(columns=columns)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

        # Record attendance
        if name != "Unknown":
            date_str = datetime.now().strftime("%Y-%m-%d")
            new_entry = {"Student Name": name, "Date": date_str, "Subject": subject_name, "Status": "Present"}
            if not ((attendance_df['Student Name'] == name) &
                    (attendance_df['Date'] == date_str) &
                    (attendance_df['Subject'] == subject_name)).any():
                attendance_df = attendance_df._append(new_entry, ignore_index=True)
                attendance_df.to_csv(attendance_file, index=False)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
