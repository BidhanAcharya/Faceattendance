import cv2
import numpy as np
import os
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase and download data
cred = credentials.Certificate("path to your json file")
firebase_admin.initialize_app(cred, {
    
    "databaseURL": "https://yourfirebasename-9726a-default-rtdb.firebaseio.com/"
})

# Fetch student data from Firebase
ref = db.reference('students')
student_data = ref.get()  # Retrieve all student data from Firebase as a dictionary

# Load the background image
background = cv2.imread('Z:/attendance system/Resources/Background1.png')

# Load the Encodedfile
with open("Encodefile.p", "rb") as file:
    encodeListKnownWithID = pickle.load(file)
encodeListKnown, studentIDS = encodeListKnownWithID
# print("Loaded student IDs:", studentIDS)

# Define coordinates and dimensions for the red rectangle (camera feed)
x, y = 105, 150       # Top-left corner of the red rectangle (approximate)
width, height = 800, 500  # Width and height of the rectangle (approximate)

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

# Get today's date for attendance storage
today_date = datetime.now().strftime('%Y-%m-%d')
attendance_ref = db.reference(f'attendance/{today_date}')  # Node for today's attendance
attendance_today = attendance_ref.get() or {}   # Retrieve today's attendance data

while True:
    # Capture frame-by-frame from the webcam
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if not ret:
        break

    faceCurFrame = face_recognition.face_locations(frame)
    encodeCurFrame = face_recognition.face_encodings(frame, faceCurFrame)
    
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        if True in matches:
            # Find the best match index
            matchIndex = np.argmin(faceDis)
            
            # If a match is found, retrieve the corresponding student ID and details
            student_id = studentIDS[matchIndex]
            # print("matchIndex",matchIndex)
            # print("studentIDS",studentIDS)
            # print("student_id",student_id)
            # print(f"Match found for student ID: {student_id}")
            student_info = student_data.get(student_id)

            # Check if attendance for this student has already been marked today
            if student_info['name'] not in [entry['name'] for entry in attendance_today.values()]:
                # Mark attendance in Firebase only if not already marked
                attendance_ref.push({"name": student_info['name'], "time": datetime.now().strftime('%H:%M:%S')})
                print(f"Attendance recorded for {student_info['name']}")

                # Update local record of today's attendance to prevent duplicates in this session
                attendance_today = attendance_ref.get()

            # Display "Attendance Done" message and student info
            cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 255, 0), 2)
            cv2.putText(frame, f"Name: {student_info['name']}", (faceLoc[3], faceLoc[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Email: {student_info['email']}", (faceLoc[3], faceLoc[2] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Course: {student_info['student']}", (faceLoc[3], faceLoc[2] + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Attendance Done {today_date}", (faceLoc[3], faceLoc[2] + 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        else:
            # No match found - display not registered message
            cv2.rectangle(frame, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (0, 0, 255), 2)
            cv2.putText(frame, "Sorry, you are not registered.", (faceLoc[3], faceLoc[2] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, "Please contact the admin.", (faceLoc[3], faceLoc[2] + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Resize the camera feed to fit the red rectangle
    resized_frame = cv2.resize(frame, (width, height))
    

    # Create a copy of the background to overlay the camera feed on it
    overlay_image = background.copy()

    # Overlay the resized camera frame onto the background image at the red rectangle's position
    overlay_image[y:y+height, x:x+width] = resized_frame

    # Display the final output with the background and camera overlay
    cv2.imshow('Overlay Camera on Background', overlay_image)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
